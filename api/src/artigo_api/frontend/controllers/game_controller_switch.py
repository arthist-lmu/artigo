from django.core.cache import cache
from .game_roi_controller import GameROIController
from .game_tagging_controller import GameTaggingController


def switch(request):
    plugins = cache.get('plugins', {})
    params = request.query_params

    game_type = params.get('game_type', 'tagging')

    if game_type == 'tagging':
        game_controller = GameTaggingController(
            resource_plugin_manager=plugins.get('resource'),
            opponent_plugin_manager=plugins.get('opponent'),
            taboo_plugin_manager=plugins.get('taboo'),
            suggester_plugin_manager=plugins.get('suggester'),
            score_plugin_manager=plugins.get('score'),
        )
    elif game_type == 'roi':
        game_controller = GameROIController(
            resource_plugin_manager=plugins.get('resource'),
            opponent_plugin_manager=plugins.get('opponent'),
            score_plugin_manager=plugins.get('score'),
        )
    else:
        return {'type': 'error', 'message': 'unknown_game_type'}

    return game_controller(params, request.user)
