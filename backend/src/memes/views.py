from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MemeTemplate
from .serializers import MemeTemplateSerializer, GenerateMemeSerializer


class ImageView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    class Meta:
        model = MemeTemplate

    queryset = MemeTemplate.objects.all()

    serializers = {
        'generate': GenerateMemeSerializer,
        'list': MemeTemplateSerializer,
        'retrieve': MemeTemplateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.serializers.get(self.action)
        return serializer

    @action(methods=["post"], detail=True)
    def generate(self, request, pk):
        ser = self.serializer_class
        print(ser)

        meme_template = get_object_or_404(MemeTemplate, pk=pk)
        file = meme_template.high_res.file
        return Response({"asd": "asd"})
