from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from drf_spectacular.views import (
    SpectacularAPIView as SchemaView,
    SpectacularRedocView as RedocView,
    SpectacularSwaggerView as SwaggerView,
)


class CustomSchemaView(SchemaView):
    pass


@method_decorator(xframe_options_exempt, name='dispatch')
class CustomRedocView(RedocView):
    pass


@method_decorator(xframe_options_exempt, name='dispatch')
class CustomSwaggerView(SwaggerView):
    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        pass
