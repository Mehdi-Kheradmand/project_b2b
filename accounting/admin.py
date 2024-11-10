from django.contrib import admin
from .models import Transaction, CreditRequest, RechargeRequest


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['seller', 'phone', 'amount', 'transaction_type', 'created_at', 'description']
    search_fields = ['seller__username', 'phone__number', 'transaction_type', 'description']
    list_filter = ['transaction_type', 'created_at']
    ordering = ['-created_at']


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ['seller', 'amount', 'status', 'created_at', 'processed_at', 'processed_by']
    search_fields = ['seller__username', 'status', 'description']
    list_filter = ['status', 'created_at']
    ordering = ['-created_at']


@admin.register(RechargeRequest)
class RechargeRequestAdmin(admin.ModelAdmin):
    list_display = ['seller', 'phone', 'amount', 'status', 'created_at', 'processed_at']
    search_fields = ['seller__username', 'phone__number', 'status', 'description']
    list_filter = ['status', 'created_at']
    ordering = ['-created_at']
