from frontend.models import *
from frontend.utils import to_int, to_float

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

        for name in query.get('suggester_types', []):
            suggester_type, _ = SuggesterType.objects \
                .get_or_create(name=name)

            gameround.suggester_types.add(suggester_type)

        for name in query.get('score_types', []):
            score_type, _ = ScoreType.objects \
                .get_or_create(name=name)

            gameround.score_types.add(score_type)

        return gameround

    @staticmethod
    def parse_query(query):
        game_options = {
            'language': query.get('language', 'de'),
            'round_duration': to_int(query.get('round_duration'), 60),
        }

        resource_type = 'RandomTaggingResource'
        resource_options = {
            'rounds': to_int(query.get('rounds'), 5),
            'lt_percentile': to_float(query.get('lt_percentile'), 1.0),
            'max_last_played': to_int(query.get('max_last_played'), 6 * 30),
        }

        if query.get('resource_type'):
            if query['resource_type'] == 'random_resource':
                resource_type = 'RandomTaggingResource'

        opponent_type = None
        opponent_options = {}

        if query.get('opponent_type'):
            if query['opponent_type'] == 'mean_gameround_opponent':
                opponent_type = 'MeanGameroundTaggingOpponent'
            elif query['opponent_type'] == 'random_gameround_opponent':
                opponent_type = 'RandomGameroundTaggingOpponent'

        taboo_type = None
        taboo_options = {
            'max_tags': to_int(query.get('taboo_max_tags'), 5),
        }

        if query.get('taboo_type'):
            if query['taboo_type'] == 'most_annotated_taboo':
                taboo_type = 'MostAnnotatedTaboo'

        suggester_types = set()

        if query.getlist('suggester_types[]'):
            if 'cooccurrence_suggester' in query['suggester_types[]']:
                suggester_types.add('CooccurrenceSuggester')

        score_types = set()

        if query.getlist('score_types[]'):
            if 'annotation_validated_score' in query.getlist('score_types[]'):
                score_types.add('AnnotationValidatedScore')

            if 'opponent_validated_score' in query.getlist('score_types[]'):
                score_types.add('OpponentValidatedScore')

        result = {
            'game_type': 'Tagging',
            'game_options': game_options,
            'resource_type': resource_type,
            'resource_options': resource_options,
            'opponent_type': opponent_type,
            'opponent_options': opponent_options,
            'taboo_type': taboo_type,
            'taboo_options': taboo_options,
            'suggester_types': list(suggester_types),
            'score_types': list(score_types),
        }

        return result
