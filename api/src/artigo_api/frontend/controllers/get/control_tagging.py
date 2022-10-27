from frontend.models import (
    OpponentTagging,
    InputTagging,
    TabooTagging,
)
from .controller import GameController


class GameTaggingController(GameController):
    _type = 'tagging'

    @staticmethod
    def fill_gameround(gameround, data):
        if data.get('opponent_tags'):
            bulk_list = []

            for tag in data['opponent_tags']:
                bulk_list.append(
                    OpponentTagging(
                        gameround=gameround,
                        resource=gameround.resource,
                        tag_id=tag.pop('id'),
                        created_after=tag['created_after'],
                    )
                )

            OpponentTagging.objects.bulk_create(bulk_list)

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
                    TabooTagging(
                        gameround=gameround,
                        resource=gameround.resource,
                        tag_id=tag.pop('id'),
                    )
                )

            TabooTagging.objects.bulk_create(bulk_list)
