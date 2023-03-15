from rest_framework import mixins, viewsets

from .models import MemeTemplate
from .serializers import MemeTemplateSerializer


class ImageView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer

    class Meta:
        model = MemeTemplate
