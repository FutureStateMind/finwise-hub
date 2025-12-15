from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings'),
        ('checking', 'Checking'),
        ('credit', 'Credit Card'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    account_name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    bank_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.account_name} - {self.bank_name}"


class Renewal(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renewals')
    service_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    next_renewal_date = models.DateField()
    is_active = models.BooleanField(default=True)
    auto_renewal = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_renewal_date']

    def __str__(self):
        return f"{self.service_name} - {self.next_renewal_date}"


class Investment(models.Model):
    INVESTMENT_TYPES = [
        ('stocks', 'Stocks'),
        ('bonds', 'Bonds'),
        ('mutual_funds', 'Mutual Funds'),
        ('etf', 'ETF'),
        ('real_estate', 'Real Estate'),
        ('crypto', 'Cryptocurrency'),
        ('commodities', 'Commodities'),
        ('other', 'Other'),
    ]
    
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    investment_name = models.CharField(max_length=200)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    initial_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    purchase_date = models.DateField()
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.investment_name} - {self.investment_type}"
    
    @property
    def profit_loss(self):
        return self.current_value - self.initial_amount
    
    @property
    def profit_loss_percentage(self):
        if self.initial_amount > 0:
            return ((self.current_value - self.initial_amount) / self.initial_amount) * 100
        return 0
