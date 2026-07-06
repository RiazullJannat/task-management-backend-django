from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import customUser as User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source='display_name', required=True) 

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        display_name = validated_data.pop('display_name', '')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            display_name=display_name
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = getattr(user, 'display_name', '')
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "accessToken": serializer.validated_data['access'],
                    "refreshToken": serializer.validated_data['refresh']
                }
            }, status=200)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=400)