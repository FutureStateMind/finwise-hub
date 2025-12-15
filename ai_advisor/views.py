from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import FinancialAdvisorService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def financial_analysis(request):
    """Get comprehensive financial analysis and AI recommendations"""
    advisor = FinancialAdvisorService(request.user)
    analysis = advisor.get_full_analysis()
    return Response(analysis)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def investment_analysis(request):
    """Get investment portfolio analysis"""
    advisor = FinancialAdvisorService(request.user)
    analysis = advisor.analyze_investments()
    return Response(analysis)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cash_flow_analysis(request):
    """Get cash flow and liquidity analysis"""
    advisor = FinancialAdvisorService(request.user)
    analysis = advisor.analyze_cash_flow()
    return Response(analysis)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    """Get personalized financial recommendations"""
    advisor = FinancialAdvisorService(request.user)
    recommendations = advisor.generate_recommendations()
    return Response(recommendations)
