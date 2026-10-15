from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import JobSeekerProfile, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    password_confirmation = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirmation",
        )
        read_only_fields = ("id",)

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_confirmation")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        read_only_fields = (
            "id",
            "username",
            "role",
        )


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = (
            "id",
            "user",
            "phone",
            "city",
            "bio",
            "created_at",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
        )

