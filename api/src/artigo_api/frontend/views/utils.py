import grpc

from collections import defaultdict
from rest_framework.views import APIView
from frontend.utils import media_url_to_image, channel

from artigo_search import index_pb2, index_pb2_grpc
from artigo_search.utils import meta_from_proto


class RPCView(APIView):
    channel = channel()


class ResourceViewHelper(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.GetRequest()

        if params.get('id'):
            grpc_request.ids.extend([params['id']])
        elif params.get('ids'):
            grpc_request.ids.extend(params['ids'])

        return grpc_request

    def rpc_get(self, params, multiple=True):
        grpc_request = self.parse_request(params)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.get(grpc_request)

            entries = {}

            for x in response.entries:
                entry = {
                    'resource_id': x.id,
                    'meta': meta_from_proto(x.meta),
                }

                if x.hash_id:
                    entry['path'] = media_url_to_image(x.hash_id)

                if x.source.id:
                    entry['source'] = {
                        'name': x.source.name,
                        'url': x.source.url,
                        'is_public': x.source.is_public,
                    }

                entries[x.id] = entry

            if multiple:
                return entries

            return list(entries.values())[0]
        except grpc.RpcError as error:
            return {}


class AggregateViewHelper(RPCView):
    def parse_request(self, params):
        grpc_request = index_pb2.SearchRequest()

        if params.get('query'):
            query = params['query']

            if isinstance(query, str):
                query = {'all-text': query}
            elif isinstance(query, list):
                query_dict = defaultdict(list)

                for q in query:
                    if not isinstance(q, dict):
                        q = {'value': q}

                    field = q.get('name', 'all-text')
                    query_dict[field].append(q)

                query = query_dict

            if isinstance(query, dict):
                for field, queries in query.items():
                    if isinstance(queries, str):
                        queries = queries.split()
                    elif not isinstance(queries, (set, list)):
                        queries = [queries]

                    for q in queries:
                        if not isinstance(q, dict):
                            q = {'value': q}

                        if q['value'].startswith('+'):
                            q['flag'] = 'must'
                            q['value'] = q['value'][1:]
                        elif q['value'].startswith('-'):
                            q['flag'] = 'not'
                            q['value'] = q['value'][1:]

                        term = grpc_request.terms.add()
                        term.text.query = q['value']

                        if field in ['tags', 'source']:
                            term.text.field = field
                        elif field in ['all-text', '']:
                            term.text.field = 'all-text'
                        else:
                            term.text.field = f'meta.{field}'

                        if q.get('flag') == 'must':
                            term.text.flag = index_pb2.TextSearchTerm.MUST
                        elif q.get('flag') == 'not':
                            term.text.flag = index_pb2.TextSearchTerm.NOT
                        else:
                            term.text.flag = index_pb2.TextSearchTerm.SHOULD

        if params.get('aggregate'):
            aggregate = params['aggregate']

            for field in aggregate.get('fields', []):
                grpc_request.aggregate.fields.extend([field])

            if isinstance(aggregate.get('size'), int):
                grpc_request.aggregate.size = aggregate['size']
            else:
                grpc_request.aggregate.size = 250

            grpc_request.aggregate.use_query = aggregate.get('use_query', True)
            grpc_request.aggregate.significant = aggregate.get('significant', False)

        return grpc_request

    def rpc_post(self, params):
        grpc_request = self.parse_request(params)
        stub = index_pb2_grpc.IndexStub(self.channel)

        try:
            response = stub.aggregate(grpc_request)

            aggregations = []

            for x in response.aggregations:
                values = {
                    'field': x.field,
                    'entries': [],
                }

                for entry in x.entries:
                    values['entries'].append({
                        'name': entry.key,
                        'count': entry.int_val,
                    })

                aggregations.append(values)

            return {
                'aggregations': aggregations,
            }
        except grpc.RpcError as error:
            return []
