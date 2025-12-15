from django.contrib import admin
from .models import BankAccount, Renewal, Investment

# Register your models here.

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_name', 'bank_name', 'account_type', 'balance', 'currency', 'user', 'created_at']
    search_fields = ['account_name', 'bank_name', 'user__username']
    list_filter = ['account_type', 'currency', 'created_at']


@admin.register(Renewal)
class RenewalAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'amount', 'frequency', 'next_renewal_date', 'is_active', 'user']
    search_fields = ['service_name', 'user__username']
    list_filter = ['frequency', 'is_active', 'next_renewal_date']


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investment_name', 'investment_type', 'risk_level', 'initial_amount', 
                    'current_value', 'profit_loss', 'user', 'purchase_date']
    search_fields = ['investment_name', 'user__username']
    list_filter = ['investment_type', 'risk_level', 'purchase_date']
    
    def profit_loss(self, obj):
        return f"{obj.profit_loss:.2f}"
    profit_loss.short_description = 'Profit/Loss'
