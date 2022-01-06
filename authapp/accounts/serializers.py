from rest_framework import serializers
from .models import UserBase


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserBase
        fields = ['username', 'email', 'password', 'confirm_password', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = UserBase(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            address = self.validated_data['address'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Password and Confirm Password must match'})
        user.set_password(password)
        user.save()
        return user    


class EditSerializer(serializers.ModelSerializer):

        class Meta:
            model = UserBase
            fields = ['username', 'email', 'address']