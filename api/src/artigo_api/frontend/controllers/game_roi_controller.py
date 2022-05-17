from frontend.models import *
from frontend.utils import to_int

from .game_controller import GameController


class GameROIController(GameController):
    @staticmethod
    def create_gameround(query, data, gamesession, user):
        gameround = Gameround(
            user=user,
            gamesession=gamesession,
            resource_id=data['resource_id'],
        )

        if query.get('opponent_type') is not None:
            opponent_type, _ = OpponentType.objects \
                .get_or_create(name=query['opponent_type'])
            opponent_type.save()

            gameround.opponent_type = opponent_type

        gameround.save()

        if data.get('opponent_rois'):
            bulk_list = []

            for roi in data['opponent_rois']:
                bulk_list.append(
                    OpponentROI(
                        gameround=gameround,
                        resource=gameround.resource,
                        x=roi.pop('x'),
                        y=roi.pop('y'),
                        width=roi.pop('width'),
                        height=roi.pop('height'),
                        created_after=roi['created_after'],
                    )
                )

            OpponentROI.objects.bulk_create(bulk_list)

        return gameround

    @staticmethod
    def parse_query(query):
        game_options = {
            'language': query.get('language', 'de'),
            'round_duration': to_int(query.get('round_duration'), 60),
        }

        resource_type = 'RandomROIResource'
        resource_options = {
            'rounds': to_int(query.get('rounds'), 5),
            'max_last_played': to_int(query.get('max_last_played'), 6 * 30),
        }

        if query.get('resource_type'):
            if query['resource_type'] == 'random_resource':
                resource_type = 'RandomROIResource'

        opponent_type = None
        opponent_options = {}

        if query.get('opponent_type'):
            if query['opponent_type'] == 'mean_gameround_opponent':
                opponent_type = 'MeanGameroundROIOpponent'
            elif query['opponent_type'] == 'random_gameround_opponent':
                opponent_type = 'RandomGameroundROIOpponent'

        result = {
            'game_type': 'ROI',
            'game_options': game_options,
            'resource_type': resource_type,
            'resource_options': resource_options,
            'opponent_type': opponent_type,
            'opponent_options': opponent_options,
        }

        return result
