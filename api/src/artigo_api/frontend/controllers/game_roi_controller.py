from frontend.models import *
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
