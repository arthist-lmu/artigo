import logging

from frontend.models import UserROI
from .input_controller import InputController

logger = logging.getLogger(__name__)


class InputROIController(InputController):
    def __call__(self, gameround, params, user):
        query = self.parse_query(gameround, params)
        logger.info(f'[Game Controller] Query: {query}')

        result = {}

        if params.get('roi'):
            if isinstance(params['roi'], dict):
                params['roi'] = [params['roi']]

            result['rois'] = [
                {'valid': True, **roi}
                for roi in params['roi']
            ]

        if query.get('filter_type'):
            try:
                result['rois'] = dict(
                    self.filter_plugin_manager.run(
                        result['rois'],
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
                result['rois'] = dict(
                    self.score_plugin_manager.run(
                        result['rois'],
                        gameround,
                        query['game_options'],
                        query['score_type'],
                    )
                )
            except Exception as error:
                logger.error(traceback.format_exc())

                return {'type': 'error', 'message': 'invalid_scores'}

        if result.get('rois'):
            bulk_list = []

            for roi in result['rois']:
                if not roi.get('valid'):
                    continue

                tagging = UserROI(
                    user=user,
                    gameround=gameround,
                    x=roi['x'],
                    y=roi['y'],
                    width=roi['width'],
                    height=roi['height'],
                    resource=gameround.resource,
                    created=timezone.now(),
                )

                if roi.get('score'):
                    tagging.score = roi['score']

                bulk_list.append(tagging)

            UserROI.objects.bulk_create(bulk_list)

        return {'type': 'ok', **result}
