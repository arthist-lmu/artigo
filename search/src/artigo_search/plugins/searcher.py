import uuid
import logging

from .. import index_pb2

logger = logging.getLogger(__name__)


class Searcher:
    def __init__(self, backbone, aggregator=None):
        self.backbone = backbone
        self.aggregator = aggregator

    def __call__(self, query, limit=100, offset=0):
        query = self.parse_query(query)

        body = self.backbone.build_body(query)
        result = self.backbone.search(body, limit, offset)

        if self.aggregator and query.get('aggregate'):
            if query['aggregate'].get('use_query', False):
                aggregations = self.aggregator(
                    query=body,
                    fields=query['aggregate']['fields'],
                    size=query['aggregate']['size'],
                )
            else:
                aggregations = self.aggregator(
                    query=None,
                    fields=query['aggregate']['fields'],
                    size=query['aggregate']['size'],
                )

            result['aggregations'] = aggregations

        return result

    def parse_query(self, query):
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
                'fields': list(query.aggregate.fields),
                'size': query.aggregate.size,
                'use_query': query.aggregate.use_query,
            }

        return result
