from rest_framework import serializers

from .models import MemeTemplate, Meme


class MemeTemplateSerializer(serializers.ModelSerializer):
    high_res = serializers.ImageField(use_url=True)
    low_res = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = MemeTemplate
        fields = ["id", "high_res", "low_res", "name"]


class MemeSerializer(serializers.ModelSerializer):
    low_res = serializers.ImageField(required=False)
    example = serializers.BooleanField(read_only=True, default=False, required=False)

    class Meta:
        model = Meme
        fields = ["low_res", "high_res", "bottom_text", "top_text", "example", "private"]


class GenerateMemeSerializer(serializers.Serializer):
    top_text = serializers.CharField(max_length=200)
    bottom_text = serializers.CharField(max_length=200)
    private = serializers.BooleanField()
