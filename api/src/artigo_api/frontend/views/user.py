import logging
import traceback

from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET', 'POST'], exclude=True)
class UserView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        try:
            user = request.user

            return Response({
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            })
        except Exception as e:
            logger.error(traceback.format_exc())

        raise APIException('unknown_error')

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }

        return Response(content)
