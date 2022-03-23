import uuid
import logging
import faulthandler

from collections import defaultdict
from opensearch_dsl import Search, Q
from artigo_search import index_pb2

logger = logging.getLogger(__name__)


class Searcher:
    def __init__(self, backbone):
        self.backbone = backbone

    def __call__(self, query, limit=100, offset=0):
        faulthandler.enable()
        PYTHONFAULTHANDLER = 1

        result = {}

        query = self.parse_query(query)
        body = self.build_body(query, True)

        if limit > 0:
            result = self.backbone.search(body, limit, offset)

        if query.get('aggregate'):
            result['aggregations'] = self.backbone.aggregate(
                body, **query['aggregate'], limit=0, offset=0,
            )

        return result

    @staticmethod
    def parse_query(query):
        text_search = []
        range_search = []

        for term in query.terms:
            term_type = term.WhichOneof('term')

            if term_type == 'text':
                text = term.text

                if text.flag == index_pb2.TextSearchTerm.MUST:
                    flag = 'must'
                elif text.flag == index_pb2.TextSearchTerm.NOT:
                    flag = 'not'
                else:
                    flag = 'should'

                text_search.append({
                    'field': text.field.lower(),
                    'query': text.query,
                    'flag': flag,
                })
            elif term_type == 'number':
                number = term.number

                query_type = number.WhichOneof('query')

                if query_type == 'string_query':
                    try:
                        query = int(number.string_query)
                    except:
                        try:
                            query = float(number.string_query)
                        except:
                            continue
                elif query_type == 'int_query':
                    query = number.int_query
                elif query_type == 'float_query':
                    query = number.float_query

                if number.relation == index_pb2.NumberSearchTerm.GREATER:
                    relation = 'gt'
                elif number.relation == index_pb2.NumberSearchTerm.GREATER_EQ:
                    relation = 'gte'
                elif number.relation == index_pb2.NumberSearchTerm.LESS_EQ:
                    relation = 'lte'
                elif number.relation == index_pb2.NumberSearchTerm.LESS:
                    relation = 'lt'
                else:
                    relation = 'eq'

                if number.flag == index_pb2.NumberSearchTerm.MUST:
                    flag = 'must'
                elif number.flag == index_pb2.NumberSearchTerm.NOT:
                    flag = 'not'
                else:
                    flag = 'should'

                range_search.append({
                    'field': number.field.lower(),
                    'query': query,
                    'relation': relation,
                    'flag': flag,
                })

        if query.sorting == index_pb2.SearchRequest.SORTING_RANDOM:
            sorting = 'random'
        else:
            sorting = None

        if query.seed is not None and str(query.seed):
            seed = str(query.seed)
        else:
            seed = uuid.uuid4().hex

        result = {
            'text_search': text_search,
            'range_search': range_search,
            'sorting': sorting,
            'seed': seed,
        }

        if len(query.aggregate.fields) and query.aggregate.size > 0:
            result['aggregate'] = {
                'use_query': query.aggregate.use_query,
                'fields': list(query.aggregate.fields),
                'size': query.aggregate.size,
                'significant': query.aggregate.significant,
            }

        return result

    @staticmethod
    def build_body(query, convert=True):
        terms = defaultdict(list)

        for x in query.get('text_search', []):
            term = None

            if x.get('field', 'all-text') == 'all-text':
                term = Q(
                    'multi_match',
                    fields=['all_text'],
                    query=x['query'],
                )
            else:
                field_path = [y for y in x['field'].split('.') if y]

                if len(field_path) == 1:
                    if field_path[0] == 'meta':
                        term = Q(
                            'multi_match',
                            fields=['all_metadata'],
                            query=x['query'],
                        )
                    elif field_path[0] == 'tags':
                        term = Q(
                            'nested',
                            path='tags',
                            query=Q(
                                'bool',
                                must=[
                                    Q('match', tags__name=x['query']),
                                    Q('range', tags__count={'gte': 1}),
                                ],
                            ),
                        )
                    elif field_path[0] == 'source':
                        term = Q(
                            'nested',
                            path='source',
                            query=Q(
                                'bool',
                                must=[
                                    Q('match', source__name=x['query']),
                                ],
                            ),
                        )
                elif len(field_path) == 2:
                    if field_path[0] == 'meta':
                        term = Q(
                            'nested',
                            path='metadata',
                            query=Q(
                                'bool',
                                must=[
                                    Q('match', metadata__name=field_path[1]),
                                    Q('match', metadata__value_str=x['query']),
                                ],
                            ),
                        )

            if term is None:
                continue

            if x.get('flag'):
                if x['flag'] == 'must':
                    terms['must'].append(term)
                elif x['flag'] == 'should':
                    terms['should'].append(term)
                else:
                    terms['must_not'].append(term)
            else:
                terms['should'].append(term)

        for x in query.get('range_search', []):
            term = None

            if not x.get('field'):
                continue
            else:
                field_path = [y for y in x['field'].split('.') if y]

                if len(field_path) == 2:
                    if field_path[0] == 'meta':
                        if x['relation'] == 'eq':
                            value_match = Q(
                                'term',
                                metadata__value_int=x['query'],
                            )
                        else:
                            value_match = Q(
                                'range',
                                metadata__value_int={x['relation']: x['query']},
                            )

                        term = Q(
                            'nested',
                            path='metadata',
                            query=Q(
                                'bool',
                                must=[
                                    Q('match', metadata__name=field_path[1]),
                                    value_match,
                                ],
                            ),
                        )

            if term is None:
                continue

            if x.get('flag'):
                if x['flag'] == 'must':
                    terms['must'].append(term)
                elif x['flag'] == 'should':
                    terms['should'].append(term)
                else:
                    terms['must_not'].append(term)
            else:
                terms['should'].append(term)

        if query.get('sorting'):
            if query['sorting'].lower() == 'random':
                seed = query.get('seed', uuid.uuid4().hex)

                terms['should'].append(
                    Q(
                        'function_score',
                        functions=[{
                            'random_score': {
                                'field': 'path.keyword',
                                'seed': seed,
                            },
                        }],
                    )
                )

        logger.info(f'[Server] Query {terms}')

        search = Search().query(
            Q(
                'bool',
                must=terms.get('must', []),
                should=terms.get('should', []),
                must_not=terms.get('must_not', []),
            ),
        )

        if convert:
            return search.to_dict()

        return search
