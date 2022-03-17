import logging
import traceback

from datetime import timedelta
from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from frontend.models import *

logger = logging.getLogger(__name__)


class TagController:
    def __init__(
        self,
        filter_plugin_manager=None,
        score_plugin_manager=None,
    ):
        super().__init__()

        self.filter_plugin_manager = filter_plugin_manager
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

            if params.get('session_id'):
                gameround = gameround.filter(gamesession_id=params['session_id'])

            if gameround.count() > 1:
                return {'type': 'error', 'message': 'multiple_valid_gamerounds'}

            gameround = gameround.latest('created')
        except ObjectDoesNotExist:
            return {'type': 'error', 'message': 'outdated_gameround'}
        except Exception as error:
            logger.error(traceback.format_exc())

            return {'type': 'error', 'message': 'invalid_resource'}

        query = self.parse_query(params, gameround)
        logger.info(f'[Game Controller] Query: {query}')

        result = {}

        if params.get('tag'):
            if isinstance(params['tag'], str):
                result['tags'] = [params['tag']]
            elif isinstance(params['tag'], (list, set)):
                result['tags'] = list(params['tag'])

        if query.get('filter_types'):
            try:
                result['tags'] = list(
                    self.filter_plugin_manager.run(
                        result['tags'],
                        gameround,
                        query['game_options'],
                        query['filter_types'],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_filters'}

        if query.get('score_types'):
            try:
                result['tags'] = list(
                    self.score_plugin_manager.run(
                        result['tags'],
                        gameround,
                        query['game_options'],
                        query['score_types'],
                    ),
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_scores'}

        if result.get('tags'):
            bulk_list = []

            for tag in result['tags']:
                if isinstance(tag, str):
                    tag = {
                        'name': tag,
                        'score': 0,
                    }

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

        return {'type': 'ok', **result}

    @staticmethod
    def parse_query(query, gameround):
        gameround = model_to_dict(gameround)

        game_options = {
            'resource_id': query.get('resource_id'),
            'language': query.get('language', 'de'),
        }

        filter_types = set(['AlreadyAnnotatedFilter'])

        if gameround.get('taboo_type'):
            filter_types.add('TabooFilter')

        score_types = set()

        for score_type in gameround.get('score_types', []):
            score_types.add(score_type.name)

        result = {
            'game_options': game_options,
            'filter_types': list(filter_types),
            'score_types': list(score_types),
        }

        return result
