from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Phone
from .serializers import PhoneSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class PhonePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PhoneView(APIView):
    serializer_class = PhoneSerializer
    queryset = Phone.objects.all()
    pagination_class = PhonePagination

    def get_permissions(self):
        return [IsAuthenticated()]

    def post(self, request: Request) -> Response:
        requested_user: User = request.user
        serializer_result = self.serializer_class(data=request.data)
        if serializer_result.is_valid():
            serializer_result.save()
            return Response(serializer_result.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer_result.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        phones = self.queryset
        number_filter = request.query_params.get('number', None)
        if number_filter:
            phones = phones.filter(number__icontains=number_filter)

        page = paginator.paginate_queryset(queryset=phones, request=request)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(data=serializer.data)

        serializer = self.serializer_class(phones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
