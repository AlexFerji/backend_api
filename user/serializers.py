from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer

from .models import CustomUser

class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            full_name='{} {}'.format(self.validated_data['first_name'], self.validated_data['last_name']),

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user
