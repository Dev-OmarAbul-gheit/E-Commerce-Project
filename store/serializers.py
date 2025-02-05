from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from . import models


class SignUpSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = models.User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    
class UserToken(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def create_user_token(self, user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return {
            "refresh": str(refresh),
            "access": str(access),
        }


class SignInSerializer(UserToken, serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        if user := authenticate(email=email, password=password):
            return self.create_user_token(user)
        raise serializers.ValidationError("Invalid email or password!!")
    

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Collection
        fields = ['id', 'name', 'description', 'products_count']

    def get_products_count(self, collection):
        return collection.products.count()


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return models.ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = models.ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'collection', 'images']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'user_id', 'first_name', 'last_name', 'email', 'phone', 'address']