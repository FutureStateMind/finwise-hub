from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import BankAccount, Renewal, Investment
from .serializers import BankAccountSerializer, RenewalSerializer, InvestmentSerializer


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RenewalViewSet(viewsets.ModelViewSet):
    serializer_class = RenewalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Renewal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvestmentViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
