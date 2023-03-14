from rest_framework import mixins, viewsets

from .models import MemeTemplate
from .serializers import ImageSerializer


class ImageView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = MemeTemplate.objects.all()
    serializer_class = ImageSerializer

    class Meta:
        model = MemeTemplate
