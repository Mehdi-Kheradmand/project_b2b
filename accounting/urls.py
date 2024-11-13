from django.urls import path
from .views import TransactionView, CreditRequestView,\
    CreditRequestProcessView, RechargeRequestView, RechargeHistoryView


urlpatterns = [
    path('credit-request/', CreditRequestView.as_view(), name="credit_request"),
    path('credit-requests/<cr_id>/process/', CreditRequestProcessView.as_view(), name="credit_process"),

    path('transactions/', TransactionView.as_view()),

    path('recharge-request/', RechargeRequestView.as_view(), name="recharge_request"),
    path('recharge-history/', RechargeHistoryView.as_view()),
]

app_name = "accounting"
