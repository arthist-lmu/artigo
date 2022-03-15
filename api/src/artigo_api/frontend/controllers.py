import grpc
import logging
import traceback

from collections import defaultdict
from datetime import timedelta
from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from frontend.utils import to_int, to_float, channel, media_url_to_image
from frontend.models import *

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto

logger = logging.getLogger(__name__)


class GameController:
    def __init__(
        self,
        resource_plugin_manager=None,
        opponent_plugin_manager=None,
        taboo_plugin_manager=None,
    ):
        super().__init__()

        self.resource_plugin_manager = resource_plugin_manager
        self.opponent_plugin_manager = opponent_plugin_manager
        self.taboo_plugin_manager = taboo_plugin_manager

    def __call__(self, params, user):
        if len(params) == 0:
            # TODO: more checks if multiple gamesessions could be valid
            gamesession = Gamesession.objects.filter(user=user) \
                .latest('created')
        elif params.get('gamesession_id'):
            try:
                gamesession = Gamesession.objects.get(id=params['gamesession_id'])
            except ObjectDoesNotExist:
                return {'type': 'error', 'message': 'invalid_gamesession'}
        else:
            result = self.create_game(params, user)
            if result['type'] == 'error': return result

            gamesession = result['gamesession']

        data = cache.get(f'gamesession_{gamesession.id}')

        if data is None:
            return {'type': 'error', 'message': 'outdated_gamesession'}

        gamerounds = Gameround.objects.filter(gamesession=gamesession).count()

        if gamerounds == gamesession.rounds:
            cache.delete(f'gamesession_{gamesession.id}')

            return {'type': 'error', 'message': 'finished_gamesession'}

        try:
            gameround_data = list(data['game'].values())[gamerounds]

            gameround = Gameround(
                gamesession=gamesession,
                resource_id=gameround_data['resource_id'],
            )

            if data['query']['opponent_type'] is not None:
                opponent_type, _ = OpponentType.objects \
                    .get_or_create(name=data['query']['opponent_type'])
                opponent_type.save()

                gameround.opponent_type = opponent_type

            if data['query']['taboo_type'] is not None:
                taboo_type, _ = TabooType.objects \
                    .get_or_create(name=data['query']['taboo_type'])
                taboo_type.save()

                gameround.taboo_type = taboo_type

            gameround.save()

            if gameround_data.get('opponent_tags'):
                bulk_list = []

                for tag in gameround_data['opponent_tags']:
                    bulk_list.append(
                        OpponentTagging(
                            gameround=gameround,
                            resource=gameround.resource,
                            tag_id=tag.pop('id'),
                            created_after=tag['created_after'],
                        )
                    )

                OpponentTagging.objects.bulk_create(bulk_list)

            if gameround_data.get('taboo_tags'):
                bulk_list = []

                for tag in gameround_data['taboo_tags']:
                    bulk_list.append(
                        TabooTagging(
                            gameround=gameround,
                            resource=gameround.resource,
                            tag_id=tag.pop('id'),
                        )
                    )

                TabooTagging.objects.bulk_create(bulk_list)

            for score_type_name in data['query']['score_types']:
                score_type, _ = ScoreType.objects \
                    .get_or_create(name=score_type_name)
                score_type.save()

                gameround.score_types.add(score_type)
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'unknown_error'}

        logger.info(f'[Game Controller] Gameround: {gameround_data}')

        return {
            'type': 'ok',
            'round_id': gamerounds + 1,
            'rounds': gamesession.rounds,
            'gameround': gameround_data,
        }

    def create_game(self, params, user):
        query = self.parse_query(params)
        logger.info(f'[Game Controller] Query: {query}')

        try:
            resource_ids = list(
                self.resource_plugin_manager.run(
                    {'user_id': user.id},
                    [query['resource_type']],
                    configs=[
                        {
                            'type': query['resource_type'],
                            'params': query['resource_options'],
                        },
                    ],
                ),
            )
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_game_options'}

        if resource_ids is None or len(resource_ids) == 0:
            return {'type': 'error', 'message': 'invalid_resources'}

        result = {}

        if query['opponent_type'] is not None:
            try:
                result['opponent'] = list(
                    self.opponent_plugin_manager.run(
                        resource_ids,
                        query['game_options'],
                        [query['opponent_type']],
                        configs=[
                            {
                                'type': query['opponent_type'],
                                'params': query['opponent_options'],
                            },
                        ],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_opponents'}

        if query['taboo_type'] is not None:
            try:
                result['taboo'] = list(
                    self.taboo_plugin_manager.run(
                        resource_ids,
                        query['game_options'],
                        [query['taboo_type']],
                        configs=[
                            {
                                'type': query['taboo_type'],
                                'params': query['taboo_options'],
                            },
                        ],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_taboos'}

        game = self.merge_to_game(result, resource_ids)
        # logger.info(f'[Game Controller] Game: {game}')

        try:
            gametype, _ = Gametype.objects.get_or_create(name='Tagging')
            gametype.save()

            gamesession = Gamesession(
                rounds=query['resource_options']['rounds'],
                round_duration=query['game_options']['round_duration'],
                user=user,
                gametype=gametype,
            )
            gamesession.save()
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_game_options'}

        timeout = None

        if query['game_options']['round_duration'] > 0:
            timeout = 60 * 60 * 24

        cache.set(
            f'gamesession_{gamesession.id}',
            {'query': query, 'game': game},
            timeout=timeout,
        )

        return {'type': 'ok', 'gamesession': gamesession}

    @staticmethod
    def parse_query(query):
        game_options = {
            'language': query.get('language', 'de'),
            'round_duration': to_int(query.get('round_duration'), 60),
        }

        resource_type = 'RandomResource'
        resource_options = {
            'rounds': to_int(query.get('rounds'), 5),
            'lt_percentile': to_float(query.get('lt_percentile'), 1.0),
            'max_last_played': to_int(query.get('max_last_played'), 6 * 30),
        }

        if query.get('resource_type'):
            if query['resource_type'] == 'random_resource':
                resource_type = 'RandomResource'

        opponent_type = None
        opponent_options = {}

        if query.get('opponent_type'):
            if query['opponent_type'] == 'mean_gameround_opponent':
                opponent_type = 'MeanGameroundOpponent'
            elif query['opponent_type'] == 'random_gameround_opponent':
                opponent_type = 'RandomGameroundOpponent'

        taboo_type = None
        taboo_options = {
            'max_tags': to_int(query.get('taboo_max_tags'), 5)
        }

        if query.get('taboo_type'):
            if query['taboo_type'] == 'most_annotated_taboo':
                taboo_type = 'MostAnnotatedTaboo'

        score_types = set(['AnnotationValidatedScore'])
        score_options = {}

        if query.getlist('score_types[]'):
            if 'annotation_validated_score' in query['score_types[]']:
                score_types.add('AnnotationValidatedScore')

            if 'opponent_validated_score' in query['score_types[]']:
                score_types.add('OpponentValidatedScore')

        result = {
            'game_options': game_options,
            'resource_type': resource_type,
            'resource_options': resource_options,
            'opponent_type': opponent_type,
            'opponent_options': opponent_options,
            'taboo_type': taboo_type,
            'taboo_options': taboo_options,
            'score_types': list(score_types),
            'score_options': score_options,
        }

        return result

    def merge_to_game(self, result, resource_ids):
        resources = self.get_resources(resource_ids)

        game = defaultdict(dict)

        for key, values in result.items():
            for value in values:
                resource_id = str(value.pop('resource_id', ''))

                if len(resource_id) == 0:
                    continue

                for field, v in value.items():
                    game[resource_id][f'{key}_{field}'] = v

                game[resource_id].update(resources[resource_id])

        return dict(game)

    @staticmethod
    def get_resources(resource_ids):
        def parse_request(params):
            grpc_request = index_pb2.GetRequest()

            if params.get('ids'):
                grpc_request.ids.extend(params['ids'])

            return grpc_request

        def rpc_get(params):
            grpc_request = parse_request(params)
            stub = index_pb2_grpc.IndexStub(channel())

            try:
                response = stub.get(grpc_request)

                entries = {}

                for x in response.entries:
                    entry = {
                        'resource_id': x.id,
                        'meta': meta_from_proto(x.meta),
                    }

                    if x.hash_id:
                        entry['path'] = media_url_to_image(x.hash_id)

                    if x.source.id:
                        entry['source'] = {
                            'name': x.source.name,
                            'url': x.source.url,
                            'is_public': x.source.is_public,
                        }

                    entries[x.id] = entry

                return entries
            except grpc.RpcError as error:
                return {}

        params = {'ids': map(str, resource_ids)}

        return rpc_get(params)


class TagController:
    def __init__(
        self,
        score_plugin_manager=None,
    ):
        super().__init__()

        self.score_plugin_manager = score_plugin_manager

    def __call__(self, params, user):
        try:
            gameround = Gameround.objects.filter(resource_id=params['resource_id']) \
                .filter(
                    Q (gamesession__round_duration=0) | Q(
                        created__gte=timezone.now() - timedelta(seconds=5) \
                            - timedelta(seconds=1) * F('gamesession__round_duration')
                    )
                )

            if gameround.count() > 1:
                gameround = gameround.filter(gamesession_id=params['gamesession_id'])

            gameround = gameround.latest('created')
        except ObjectDoesNotExist:
            return {'type': 'error', 'message': 'outdated_gameround'}
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_resource'}

        data = cache.get(f'gamesession_{gameround.gamesession.id}')

        if data is None:
            return {'type': 'error', 'message': 'outdated_gamesession'}

        try:
            gameround_data = data['game'][str(gameround.resource.id)]
        except:
            return {'type': 'error', 'message': 'invalid_resource'}

        query = self.parse_query(params)
        logger.info(f'[Game Controller] Query: {query}')

        result = {}

        if data['query'].get('score_types'):
            try:
                result['tags'] = list(
                    self.score_plugin_manager.run(
                        params.get('tag_name'),
                        gameround,
                        query['game_options'],
                        data['query']['score_types'],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_scores'}

        if gameround_data.get('taboo_tags'):
            taboo_tags = set(x['name'].lower() for x in gameround_data['taboo_tags'])

            for tag in result['tags']:
                if tag['name'].lower() in taboo_tags:
                    tag['valid'] = False
                    tag['score'] = 0

        if result.get('tags'):
            invalid_tags = Tagging.objects.filter(
                    gameround=gameround,
                    resource=gameround.resource,
                ) \
                .values_list('tag__name', flat=True)

            invalid_tags = set(x.lower() for x in invalid_tags)

            bulk_list = []

            for tag in result['tags']:
                if tag['name'] in invalid_tags:
                    tag['valid'] = False
                    tag['score'] = 0

                if not tag.get('valid', True):
                    continue

                tag['valid'] = True

                tagging = Tagging(
                    user=user,
                    gameround=gameround,
                    resource=gameround.resource,
                    score=tag['score'],
                    created=timezone.now(),
                )

                tag_obj = Tag.objects.filter(
                    name__iexact=tag['name'],
                    language=query['game_options']['language'],
                ).first()

                if tag_obj is None:
                    tag_obj = Tag.objects.create(
                        name=tag['name'],
                        language=query['game_options']['language'],
                    )

                tagging.tag = tag_obj
                bulk_list.append(tagging)

            Tagging.objects.bulk_create(bulk_list)

        return {
            'type': 'ok',
            'tags': result.get('tags', []),
        }

    @staticmethod
    def parse_query(query):
        game_options = {
            'resource_id': query.get('resource_id'),
            'language': query.get('language', 'de'),
        }

        result = {
            'game_options': game_options,
        }

        return result
