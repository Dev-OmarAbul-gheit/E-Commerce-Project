from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User, Collection
from .serializers import SignUpSerializer, SignInSerializer, UserSerializer, CollectionSerializer


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
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer