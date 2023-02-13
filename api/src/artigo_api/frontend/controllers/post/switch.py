import logging
import traceback

from datetime import timedelta
from django.db.models import F, Q
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from frontend.models import Gameround
from .control_roi import InputROIController
from .control_tagging import InputTaggingController

logger = logging.getLogger(__name__)


def switch(request):
    params = request.data['params']

    try:
        if not params.get('resource_id'):
            return {'type': 'error', 'message': 'missing_resource'}

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
        return {'type': 'error', 'message': 'gameround_is_outdated'}
    except Exception as error:
        logger.error(traceback.format_exc())

        return {'type': 'error', 'message': 'resource_is_invalid'}

    game_type = gameround.gamesession.game_type.name

    if game_type == 'tagging':
        input_controller = InputTaggingController()
    elif game_type == 'roi':
        input_controller = InputROIController()
    else:
        return {'type': 'error', 'message': 'unknown_game_type'}

    return input_controller(gameround, params, request.user)
