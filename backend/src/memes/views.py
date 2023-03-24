from uuid import uuid4

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MemeTemplate
from .serializers import MemeTemplateSerializer, MemeSerializer, MemeTemplateRetrieveSerializer
from .utils import Memer


class ImageView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    class Meta:
        model = MemeTemplate

    queryset = MemeTemplate.objects.all()

    serializers = {
        'generate': MemeSerializer,
        'list': MemeTemplateSerializer,
        'retrieve': MemeTemplateRetrieveSerializer,
    }

    def get_serializer_class(self):
        serializer = self.serializers.get(self.action)
        return serializer

    @action(methods=["post"], detail=True)
    def generate(self, request, pk):
        '''
        Will generate new meme
        '''
        ser: MemeSerializer = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        bottom_text = ser.validated_data["bottom_text"]
        top_text = ser.validated_data["top_text"]
        # getting file
        meme_template = get_object_or_404(MemeTemplate, pk=pk)
        file = meme_template.high_res.file
        # creating meme
        with Memer(file) as memer:
            memer.generate_meme(bottom_text, top_text)
            image = memer.get_image()
        file_image = ContentFile(image, f"{uuid4().hex}.png")
        if ser.is_valid():
            ser.save(template=meme_template, high_res=file_image, )
            return Response(ser.data)
        else:
            return Response(ser.errors)
