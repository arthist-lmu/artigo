import logging
import traceback

from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        if not request.user.is_authenticated:
            raise APIException('User is not authenticated.')

        try:
            user = request.user

            return Response({
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            })
        except Exception as e:
            logger.error(traceback.format_exc())
    

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({})

"""
class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data['params'].get('name')
        password = request.data['params'].get('password')

        if not username:
            raise APIException('Username is not provided.')

        if not password:
            raise APIException('Password is not provided.')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            return Response({
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            })

        raise APIException('Unknown user.')
"""
"""
class LogoutView(APIView):
    def post(self, request, format=None):
        auth.logout(request)

        return Response()


class RegisterView(APIView):
    def post(self, request, format=None):
        username = request.data['params'].get('name')
        password = request.data['params'].get('password')
        email = request.data['params'].get('email')

        if not username:
            raise APIException('Username is not provided.')

        if not password:
            raise APIException('Password is not provided.')

        if not email:
            raise APIException('Email is not provided.')

        if auth.models.User.objects.filter(username=username).count() > 0:
            raise APIException('Username already taken.')

        user = auth.models.User.objects.create_user(username, email, password)
        user.save()
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            return Response({
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            })

        raise APIException('Unknown user.')
"""