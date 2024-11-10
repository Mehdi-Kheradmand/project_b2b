from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer

User = get_user_model()


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        """
        View the profile_data of the authenticated user.
        """
        user = request.user  # Access the authenticated user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    # def put(self, request: Request) -> Response:
    #     """
    #     Update the profile of the authenticated user.
    #     """
    #     the_user = request.user  # Access the authenticated user
    #     # partial=False means all fields need to be provided
    #     serializer = self.serializer_class(instance=the_user, data=request.data, partial=False)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def patch(self, request: Request) -> Response:
    #     """
    #     Partially update the profile of the authenticated user.
    #     """
    #     user = request.user  # Access the authenticated user
    #     # partial=True means only provided fields will be updated
    #     serializer = self.serializer_class(user, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
