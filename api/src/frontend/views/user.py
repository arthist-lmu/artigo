import json
import logging
import traceback

from django.contrib import auth
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie


class GetUser(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error'})

        try:
            user = request.user

            return JsonResponse({
                'status': 'ok',
                'data': {
                    'username': user.get_username(),
                    'email': user.email,
                    'date_joined': user.date_joined,
                }
            })
        except Exception as e:
            logging.error(traceback.format_exc())

            return JsonResponse({'status': 'error'})


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'status': 'ok'})


@require_http_methods(['POST'])
def login(request):
    try:
        body = request.body.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        body = request.body

    try:
        data = json.loads(body)
    except Exception as e:
        return JsonResponse({'status': 'error'})

    username = data['params'].get('username')
    password = data['params'].get('password')

    if not username:
        return JsonResponse({'status': 'error'})

    if not password:
        return JsonResponse({'status': 'error'})

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        return JsonResponse({
            'status': 'ok', 
            'data': {
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            }
        })

    return JsonResponse({'status': 'error'})


@require_http_methods(['POST'])
def logout(request):
    auth.logout(request)

    return JsonResponse({'status': 'ok'})


@require_http_methods(['POST'])
def register(request):
    try:
        body = request.body.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        body = request.body

    try:
        data = json.loads(body)
    except Exception as e:
        return JsonResponse({'status': 'error'})

    username = data['params'].get('username')
    password = data['params'].get('password')
    email = data['params'].get('email')

    if not username:
        return JsonResponse({'status': 'error'})

    if not password:
        return JsonResponse({'status': 'error'})

    if not email:
        return JsonResponse({'status': 'error'})

    if auth.models.User.objects.filter(username=username).count() > 0:
        return JsonResponse({'status': 'error'})

    user = auth.models.User.objects.create_user(username, email, password)
    user.save()
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})
