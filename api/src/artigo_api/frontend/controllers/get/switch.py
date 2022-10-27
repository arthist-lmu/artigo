from .control_roi import GameROIController
from .control_tagging import GameTaggingController


def switch(request):
    game_type = request.query_params.get('game_type', 'tagging')

    if game_type == 'tagging':
        game_controller = GameTaggingController()
    elif game_type == 'roi':
        game_controller = GameROIController()
    else:
        return {'type': 'error', 'message': 'unknown_game_type'}

    return game_controller(request.query_params, request.user)
