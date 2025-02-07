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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'price']


class RetrieveCartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item: models.CartItem):
        return item.product.price * item.quantity

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, id):
        if not models.Product.objects.filter(pk=id).exists():
            raise serializers.ValidationError('No product with the given id is exist.')
        return id

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            # check for the existance of a product in a cart as a cart item.
            cart_item = models.CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # update the quantity for an existing product
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item

        except models.CartItem.DoesNotExist:
            # add the given product to the cart as a new cart item
            return models.CartItem.objects.create(cart_id=cart_id, **self.validated_data)

    class Meta:
        model = models.CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = RetrieveCartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:models.Cart):
        return sum([(item.quantity * item.product.price) for item in cart.items.all()])

    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']