from frontend.models import *
from frontend.serializers import *
from frontend.custom_renderers import *


def create(user_id, gameround, resource, tag, created, score, origin):
    if not isinstance(tag, Tag):
        # create your tag model based on the String passed
        your_new_tag_object = Tag.objects.create(name=tag, language='de')

    # Here your create others rules too for model creation
    # Return your model .create method
        return Tagging.objects.create(user_id=user_id,
                                      gameround=gameround,
                                      resource=resource,
                                      tag=your_new_tag_object,
                                      created=created,
                                      score=score,
                                      origin=origin)
