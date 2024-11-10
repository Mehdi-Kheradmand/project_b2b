from django.urls import path
from .views import TransactionView, CreditRequestView,\
    CreditRequestProcessView, RechargeRequestView, RechargeHistoryView


urlpatterns = [
    path('credit-request/', CreditRequestView.as_view()),
    path('credit-requests/<cr_id>/process/', CreditRequestProcessView.as_view()),

    path('transactions/', TransactionView.as_view()),

    path('recharge-request/', RechargeRequestView.as_view()),
    path('recharge-history/', RechargeHistoryView.as_view()),
]
