from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import IsAuthenticatedAndSuperUser
from .models import Transaction, CreditRequest, RechargeRequest
from .serializers import TransactionSerializer, CreditRequestSerializer, \
    CreditRequestProcessSerializer, RechargeRequestSerializer, RechargeHistorySerializer
from .tasks import recharge_task, credit_approve_task
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


# region ******************** Transaction ********************
class TransactionPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TransactionView(APIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().select_related('seller', 'phone')
    pagination_class = TransactionPagination

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        # all transactions
        transactions = self.queryset

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset=transactions, request=request)
        if page is not None:
            serializer = self.serializer_class(instance=page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Serialize the entire data if pagination is not used
        serializer = self.serializer_class(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# endregion


# region ******************** Credit ********************
class CreditRequestView(APIView):
    serializer_class = CreditRequestSerializer
    queryset = CreditRequest.objects.all().select_related('seller')

    def get_permissions(self):
        if self.request.method == 'get':
            return [IsAuthenticatedAndSuperUser()]
        return [IsAuthenticated()]

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request) -> Response:
        # Retrieve pending credit requests
        pending_requests = CreditRequest.objects.filter(status='pending')
        serializer = self.serializer_class(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreditRequestProcessView(APIView):
    permission_classes = [IsAuthenticatedAndSuperUser]
    serializer_class = CreditRequestProcessSerializer
    queryset = CreditRequest.objects.all()

    def patch(self, request: Request, cr_id: int) -> Response:
        # get CreditRequest
        try:
            credit_request = self.queryset.get(id=cr_id, status='pending')
        except CreditRequest.DoesNotExist:
            return Response(
                {'detail': 'Credit request not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            # validate status
            received_status = serializer.validated_data.get('status')
            previous_status = credit_request.status
            if previous_status == 'approved':
                return Response(data={'detail': "Credit request is already approved."}, status=status.HTTP_409_CONFLICT)

            # request process
            if received_status == 'approved':
                # add task
                credit_approve_task.delay(admin_id=request.user.id, credit_request_id=credit_request.id)
                return Response(
                    data={'detail': "Credit request to Approve received , will be processed soon"},
                    status=status.HTTP_200_OK)
            else:
                # Update the credit request (rejected)
                serializer = self.serializer_class(instance=credit_request, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(processed_at=timezone.now(), processed_by=request.user)

            return Response(CreditRequestSerializer(credit_request).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# endregion


# region ******************** Recharges ********************

class RechargeRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RechargeRequestSerializer

    def post(self, request: Request) -> Response:
        # Create a new recharge request
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Save the recharge request
            recharge_request: RechargeRequest = serializer.save(seller=request.user)
            recharge_task.delay(recharge_request.id)  # Add task
            logger.error("recharge task added")
            return Response(
                data={'detail': "Recharge request created, will be processed soon"},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RechargeHistoryPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RechargeHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RechargeHistorySerializer
    queryset = RechargeRequest.objects.all().select_related('seller', 'phone')
    pagination_class = RechargeHistoryPagination

    def get(self, request: Request) -> Response:
        # Get all recharge history for the authenticated user
        recharges = RechargeRequest.objects.filter(seller=request.user)

        # set paginator
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset=recharges, request=request)

        if page is not None:
            serializer = self.serializer_class(instance=page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(recharges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# endregion
