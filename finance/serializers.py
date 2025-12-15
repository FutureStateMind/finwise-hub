from rest_framework import serializers
from .models import BankAccount, Renewal, Investment


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'account_name', 'account_type', 'bank_name', 'account_number', 
                  'balance', 'currency', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RenewalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renewal
        fields = ['id', 'service_name', 'description', 'amount', 'currency', 'frequency',
                  'next_renewal_date', 'is_active', 'auto_renewal', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    profit_loss_percentage = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Investment
        fields = ['id', 'investment_name', 'investment_type', 'risk_level', 'initial_amount',
                  'current_value', 'currency', 'purchase_date', 'description', 'notes',
                  'profit_loss', 'profit_loss_percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'profit_loss', 'profit_loss_percentage']
