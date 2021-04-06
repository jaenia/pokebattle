from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        return Token.objects.get_or_create(**validated_data)

    def update(self, instance, validated_data):
        return instance
