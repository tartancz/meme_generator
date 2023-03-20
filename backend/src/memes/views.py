from pathlib import Path

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MemeTemplate
from .serializers import MemeTemplateSerializer, GenerateMemeSerializer
from .utils import Memer


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
        '''
        Will generate new meme
        '''

        ser: GenerateMemeSerializer = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        bottom_text = ser.validated_data["bottom_text"]
        top_text = ser.validated_data["top_text"]
        #getting file
        meme_template = get_object_or_404(MemeTemplate, pk=pk)
        file = meme_template.high_res.file
        #creating meme
        with Memer(file) as memer:
            memer.generate_meme(bottom_text, top_text)
            image = memer.get_image()
        with open("pokus.png", 'ab') as bagr:
            bagr.write(image)
        return Response({"asd": "asd"})
