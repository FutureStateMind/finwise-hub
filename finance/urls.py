from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bank-accounts', views.BankAccountViewSet, basename='bankaccount')
router.register(r'renewals', views.RenewalViewSet, basename='renewal')
router.register(r'investments', views.InvestmentViewSet, basename='investment')

urlpatterns = [
    path('', include(router.urls)),
]
