from rest_framework import serializers

from gift_finder.models import SelectedGift


class SelectedGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedGift
        fields = (
            "id",
            "created_at",
            "name",
            "price",
            "image_url",
            "link",
            "is_selected",
            "is_bought",
            "is_delivered",
        )
