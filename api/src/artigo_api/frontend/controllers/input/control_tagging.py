import logging
import traceback

from django.utils import timezone
from frontend.models import Tag, UserTagging
from .controller import InputController

logger = logging.getLogger(__name__)


class InputTaggingController(InputController):
    _type = 'tagging'

    def __call__(self, gameround, params, user):
        query = self.parse_query(gameround, params)
        logger.info(f'[Game Controller] Query: {query}')

        result = {'tags': query.get('tags', [])}

        if query.get('suggester_type'):
            try:
                result['tags'] = list(
                    self.plugins['suggester'].run(
                        result['tags'],
                        query['game_options'],
                        query['suggester_type'],
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_suggesters'}

        if query.get('filter_type'):
            try:
                result['tags'] = list(
                    self.plugins['filter'].run(
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
                result['tags'] = list(
                    self.plugins['score'].run(
                        result['tags'],
                        gameround,
                        query['game_options'],
                        query['score_type'],
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_scores'}

        logger.info(result)

        if result.get('tags'):
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
