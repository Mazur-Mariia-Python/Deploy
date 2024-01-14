from rest_framework import serializers
from gift_finder.models import SelectedGift
from .models import CustomUser


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


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}
