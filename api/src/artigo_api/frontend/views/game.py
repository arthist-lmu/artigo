import json
import logging
import traceback

from rest_framework.views import APIView


class GameView(APIView):
    def get(self, request, format=None):
        resource = None

        if request.query_params.get('random'):
            seed = datetime.now().strftime('%Y%m%d')
            resource_id = Resource.objects.random(seed).id

        raise NotFound(detail='Unknown resource', code=404)

    def post(self, request, format=None):
        resource = None

        resource_id = request.query_params.get('id')
        lang = request.query_params.get('lang', 'en')

        if request.query_params.get('random'):
            seed = datetime.now().strftime('%Y%m%d')
            resource_id = Resource.objects.random(seed).id

        if resource_id:
            resource = get_resource_by_id(resource_id, lang)

        if resource:
            return Response(resource)

        raise NotFound(detail='Unknown resource', code=404)

       # return user stats
