from frontend.models import *
from .game_controller import GameController


class GameTaggingController(GameController):
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

        if query.get('taboo_type') is not None:
            taboo_type, _ = TabooType.objects \
                .get_or_create(name=query['taboo_type'])
            taboo_type.save()

            gameround.taboo_type = taboo_type

        gameround.save()

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

        for name in query.get('suggester_type', []):
            suggester_type, _ = SuggesterType.objects \
                .get_or_create(name=name)

            gameround.suggester_types.add(suggester_type)

        for name in query.get('score_type', []):
            score_type, _ = ScoreType.objects \
                .get_or_create(name=name)

            gameround.score_types.add(score_type)

        return gameround
