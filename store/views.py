from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import User, Collection, Product, ProductImage, Customer, Cart, CartItem, Order, OrderItem
from .serializers import (SignUpSerializer, SignInSerializer,
                          UserSerializer, CollectionSerializer,
                          ProductSerializer, ProductImageSerializer,
                          CustomerSerializer, CartSerializer,
                          RetrieveCartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer,
                          RetrieveOrderSerializer, CreateOrderSerializer,
                          AdminUpdateOrderSerializer, UserCancelOrderSerializer)


class SignUpViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class  = SignUpSerializer


class SignInViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignInSerializer


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.method == "GET":
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('products').all()
    serializer_class = CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer

    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error' : 'That product can not be deleted yet as it is included in some orders!'})
        return super().destroy(request, pk)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return ProductImage.objects.filter(product_id=product_id)
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False,  methods= ['GET', 'PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet
                ):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart = self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return RetrieveCartItemSerializer
        
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context= {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = RetrieveOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id=customer_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            if self.request.user.is_staff:
                return AdminUpdateOrderSerializer
            return UserCancelOrderSerializer
        return RetrieveOrderSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]