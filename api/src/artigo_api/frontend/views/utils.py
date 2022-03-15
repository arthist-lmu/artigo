from rest_framework.views import APIView
from frontend.utils import channel


class RPCView(APIView):
    channel = channel()
