from frontend.models import (
    OpponentROI,
    InputTagging,
    TabooROI,
)
from .controller import GameController


class GameROIController(GameController):
    _type = 'roi'

    @staticmethod
    def fill_gameround(gameround, data):
        if data.get('opponent_tags'):
            bulk_list = []

            for tag in data['opponent_tags']:
                bulk_list.append(
                    OpponentROI(
                        gameround=gameround,
                        resource=gameround.resource,
                        x=tag.pop('x'),
                        y=tag.pop('y'),
                        width=tag.pop('width'),
                        height=tag.pop('height'),
                        created_after=tag['created_after'],
                    )
                )

            OpponentROI.objects.bulk_create(bulk_list)

        if data.get('input_tags'):
            bulk_list = []

            for tag in data['input_tags']:
                bulk_list.append(
                    InputTagging(
                        gameround=gameround,
                        resource=gameround.resource,
                        tag_id=tag.pop('id'),
                    )
                )

            InputTagging.objects.bulk_create(bulk_list)

        if data.get('taboo_tags'):
            bulk_list = []

            for tag in data['taboo_tags']:
                bulk_list.append(
                    TabooROI(
                        gameround=gameround,
                        resource=gameround.resource,
                        tag_id=tag.pop('id'),
                        x=tag.pop('x'),
                        y=tag.pop('y'),
                        width=tag.pop('width'),
                        height=tag.pop('height'),
                    )
                )

            TabooROI.objects.bulk_create(bulk_list)
