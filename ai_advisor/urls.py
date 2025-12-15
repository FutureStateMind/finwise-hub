from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.financial_analysis, name='financial-analysis'),
    path('analysis/investments/', views.investment_analysis, name='investment-analysis'),
    path('analysis/cash-flow/', views.cash_flow_analysis, name='cash-flow-analysis'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
