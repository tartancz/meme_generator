from rest_framework import serializers

from .models import MemeTemplate


class ImageSerializer(serializers.ModelSerializer):
    high_res = serializers.ImageField(use_url=True)
    low_res = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = MemeTemplate
        fields = ["high_res", "low_res", "name" ]

