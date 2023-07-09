from rest_framework import generics
from users.models import User
from users.serializers.serializers import UsersSerializers


class UsersListView(generics.ListAPIView):
    serializer_class = UsersSerializers
    queryset = User.objects.all()
