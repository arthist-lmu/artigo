import logging
import traceback

from collections import defaultdict
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
                params['tag'] = [params['tag']]

            result['tags'] = defaultdict(dict)

            for tag in params['tag']:
                result['tags'][tag.lower()]['valid'] = True

        if query.get('filter_types'):
            try:
                result['tags'] = dict(
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
                result['tags'] = dict(
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
            result['tags'] = [
                {'name': name, **values}
                for name, values in result['tags'].items()
            ]

            bulk_list = []

            for tag in result['tags']:
                if not tag.get('valid'):
                    continue

                tagging = UserTagging(
                    user=user,
                    gameround=gameround,
                    resource=gameround.resource,
                    created=timezone.now(),
                    suggested=tag.get('suggested', False),
                )

                if tag.get('score'):
                    tagging.score = tag['score']

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

            UserTagging.objects.bulk_create(bulk_list)

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
