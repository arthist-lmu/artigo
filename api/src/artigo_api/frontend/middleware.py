import logging

from django.db import connection
from django.conf import settings
from pygments import highlight, lexers
from pygments_pprint_sql import SqlFilter
from pygments.formatters import TerminalFormatter as Formatter

logger = logging.getLogger(__name__)


class QueryPrintMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if settings.DEBUG and response.status_code == 200:
            queries = connection.queries
            n_queries = len(queries)

            total_time = 0

            for query in queries:
                query_time = query.get('time')

                if query_time is None:
                    query_time = query.get('duration', 0) / 1000

                total_time += float(query_time)

            logger.debug(f'{n_queries} queries in {total_time}s.')

            if n_queries > 0:
                self.print_queries(request, queries)

        return response

    def print_queries(self, request, queries):
        lexer = lexers.MySqlLexer()
        lexer.add_filter(SqlFilter())

        for query in queries:
            logger.debug(highlight(query['sql'], lexer, Formatter()))
