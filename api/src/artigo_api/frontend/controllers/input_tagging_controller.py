import logging
import traceback

from collections import defaultdict
from django.utils import timezone
from frontend.models import Tag, UserTagging
from .input_controller import InputController

logger = logging.getLogger(__name__)


class InputTaggingController(InputController):
    def __call__(self, gameround, params, user):
        query = self.parse_query(gameround, params)
        logger.info(f'[Game Controller] Query: {query}')

        result = {}

        if params.get('tag'):
            if isinstance(params['tag'], str):
                params['tag'] = [params['tag']]

            result['tags'] = defaultdict(dict)

            for tag in params['tag']:
                result['tags'][tag.lower()]['valid'] = True

        if query.get('filter_type'):
            try:
                result['tags'] = dict(
                    self.filter_plugin_manager.run(
                        result['tags'],
                        gameround,
                        query['game_options'],
                        query['filter_type'],
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_filters'}

        if query.get('score_type'):
            try:
                result['tags'] = dict(
                    self.score_plugin_manager.run(
                        result['tags'],
                        gameround,
                        query['game_options'],
                        query['score_type'],
                    )
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
                    score=tag.get('score', 0),
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

            UserTagging.objects.bulk_create(bulk_list)

        return {'type': 'ok', **result}
