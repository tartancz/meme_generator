from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import MemeTemplate, Meme


class MemeTemplateSerializer(serializers.ModelSerializer):
    high_res = serializers.ImageField(use_url=True)
    low_res = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = MemeTemplate
        fields = ["id", "high_res", "low_res", "name"]

    def validate_high_res(self, field):
        if field.image.width < 500:
            raise ValidationError("Image must have width bigger or equal 500px")
        return field


class MemeSerializer(serializers.ModelSerializer):
    top_text = serializers.CharField(max_length=100, allow_blank=True)
    bottom_text = serializers.CharField(max_length=100, allow_blank=True)
    example = serializers.BooleanField(read_only=True, default=False)
    private = serializers.BooleanField(default=False)

    class Meta:
        model = Meme
        fields = ["low_res", "high_res", "top_text", "bottom_text", "example", "private", "template"]
        read_only_fields = ["low_res", "high_res", "template"]

    def validate(self, attrs: dict):
        if not attrs.get("bottom_text") and not attrs.get("top_text"):
            raise ValidationError("One of the fields 'bottom_text, top_text' is required")
        return attrs

class MemeTemplateRetrieveSerializer(serializers.ModelSerializer):
    memes = MemeSerializer(many=True, read_only=True, source='public_memes')

    class Meta:
        model = MemeTemplate
        fields = ["id", "high_res", "low_res", "name", "memes"]
        

