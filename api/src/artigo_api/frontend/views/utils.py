import grpc

from django.conf import settings
from rest_framework.views import APIView
from frontend.utils import RetryOnRpcErrorClientInterceptor, ExponentialBackoff


class RPCView(APIView):
    interceptors = (
        RetryOnRpcErrorClientInterceptor(
            max_attempts=4,
            sleeping_policy=ExponentialBackoff(
                init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
            ),
            status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
        ),
    )

    channel = grpc.intercept_channel(
        grpc.insecure_channel(
            f'{settings.GRPC_HOST}:{settings.GRPC_PORT}',
            options=[
                ('grpc.max_send_message_length', 50 * 1024 * 1024),
                ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ],
        ),
        *interceptors,
    )
