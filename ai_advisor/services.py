from finance.models import Investment, BankAccount, Renewal
from accounts.models import UserProfile
from decimal import Decimal


class FinancialAdvisorService:
    """Service for analyzing user's financial data and providing AI-powered recommendations"""
    
    def __init__(self, user):
        self.user = user
        self.profile = UserProfile.objects.filter(user=user).first()
        self.investments = Investment.objects.filter(user=user)
        self.bank_accounts = BankAccount.objects.filter(user=user)
        self.renewals = Renewal.objects.filter(user=user, is_active=True)
    
    def analyze_investments(self):
        """Analyze user's investment portfolio"""
        if not self.investments.exists():
            return {
                'total_invested': 0,
                'current_value': 0,
                'total_profit_loss': 0,
                'profit_loss_percentage': 0,
                'diversification': {},
                'risk_profile': {}
            }
        
        total_invested = sum(inv.initial_amount for inv in self.investments)
        current_value = sum(inv.current_value for inv in self.investments)
        total_profit_loss = current_value - total_invested
        profit_loss_percentage = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        # Calculate diversification by investment type
        diversification = {}
        for inv in self.investments:
            inv_type = inv.get_investment_type_display()
            if inv_type not in diversification:
                diversification[inv_type] = {
                    'count': 0,
                    'total_value': 0,
                    'percentage': 0
                }
            diversification[inv_type]['count'] += 1
            diversification[inv_type]['total_value'] += float(inv.current_value)
        
        # Calculate percentages
        for inv_type in diversification:
            diversification[inv_type]['percentage'] = (
                diversification[inv_type]['total_value'] / float(current_value) * 100
            ) if current_value > 0 else 0
        
        # Calculate risk profile
        risk_profile = {}
        for inv in self.investments:
            risk = inv.get_risk_level_display()
            if risk not in risk_profile:
                risk_profile[risk] = {
                    'count': 0,
                    'total_value': 0,
                    'percentage': 0
                }
            risk_profile[risk]['count'] += 1
            risk_profile[risk]['total_value'] += float(inv.current_value)
        
        # Calculate risk percentages
        for risk in risk_profile:
            risk_profile[risk]['percentage'] = (
                risk_profile[risk]['total_value'] / float(current_value) * 100
            ) if current_value > 0 else 0
        
        return {
            'total_invested': float(total_invested),
            'current_value': float(current_value),
            'total_profit_loss': float(total_profit_loss),
            'profit_loss_percentage': float(profit_loss_percentage),
            'diversification': diversification,
            'risk_profile': risk_profile
        }
    
    def analyze_cash_flow(self):
        """Analyze user's cash flow and liquidity"""
        total_balance = sum(acc.balance for acc in self.bank_accounts)
        monthly_renewals = sum(
            ren.amount for ren in self.renewals 
            if ren.frequency in ['monthly', 'yearly', 'quarterly']
        )
        
        # Estimate monthly expenses from renewals
        monthly_expenses = 0
        for renewal in self.renewals:
            if renewal.frequency == 'monthly':
                monthly_expenses += float(renewal.amount)
            elif renewal.frequency == 'yearly':
                monthly_expenses += float(renewal.amount) / 12
            elif renewal.frequency == 'quarterly':
                monthly_expenses += float(renewal.amount) / 3
            elif renewal.frequency == 'weekly':
                monthly_expenses += float(renewal.amount) * 4
        
        emergency_fund_months = (float(total_balance) / monthly_expenses) if monthly_expenses > 0 else 0
        
        return {
            'total_cash': float(total_balance),
            'monthly_expenses': monthly_expenses,
            'emergency_fund_months': emergency_fund_months,
            'active_subscriptions': self.renewals.count()
        }
    
    def generate_recommendations(self):
        """Generate personalized financial recommendations"""
        recommendations = []
        tasks = []
        
        investment_analysis = self.analyze_investments()
        cash_flow = self.analyze_cash_flow()
        
        # Investment recommendations
        if not self.investments.exists():
            recommendations.append({
                'category': 'Investment',
                'priority': 'High',
                'message': 'You have no investments recorded. Start building your investment portfolio to work towards financial freedom.',
                'action': 'Start investing in diversified assets'
            })
            tasks.append('Research and open an investment account')
            tasks.append('Start with low-risk investments like index funds or bonds')
        else:
            # Check diversification
            diversification = investment_analysis['diversification']
            if len(diversification) < 3:
                recommendations.append({
                    'category': 'Investment',
                    'priority': 'Medium',
                    'message': f'Your portfolio is concentrated in {len(diversification)} asset type(s). Consider diversifying across more asset classes to reduce risk.',
                    'action': 'Diversify your investment portfolio'
                })
                tasks.append('Research different asset classes (stocks, bonds, real estate, etc.)')
                tasks.append('Allocate investments across at least 3-5 different asset types')
            
            # Check for single asset concentration
            for asset_type, data in diversification.items():
                if data['percentage'] > 60:
                    recommendations.append({
                        'category': 'Investment',
                        'priority': 'High',
                        'message': f'{asset_type} represents {data["percentage"]:.1f}% of your portfolio. This is risky. Aim for no single asset type to exceed 40%.',
                        'action': f'Reduce {asset_type} allocation'
                    })
                    tasks.append(f'Rebalance portfolio by reducing {asset_type} allocation to under 40%')
            
            # Check risk profile
            risk_profile = investment_analysis['risk_profile']
            if 'High Risk' in risk_profile and risk_profile['High Risk']['percentage'] > 50:
                recommendations.append({
                    'category': 'Investment',
                    'priority': 'High',
                    'message': f'High-risk investments make up {risk_profile["High Risk"]["percentage"]:.1f}% of your portfolio. Consider balancing with lower-risk assets.',
                    'action': 'Balance risk in your portfolio'
                })
                tasks.append('Add low to medium risk investments to balance portfolio')
            
            # Check portfolio performance
            if investment_analysis['profit_loss_percentage'] < -10:
                recommendations.append({
                    'category': 'Investment',
                    'priority': 'High',
                    'message': f'Your portfolio is down {abs(investment_analysis["profit_loss_percentage"]):.1f}%. Review underperforming investments and consider rebalancing.',
                    'action': 'Review and rebalance portfolio'
                })
                tasks.append('Analyze individual investment performance')
                tasks.append('Consider exiting consistently underperforming investments')
        
        # Emergency fund recommendations
        if cash_flow['emergency_fund_months'] < 3:
            recommendations.append({
                'category': 'Emergency Fund',
                'priority': 'High',
                'message': f'Your emergency fund covers only {cash_flow["emergency_fund_months"]:.1f} months. Aim for 3-6 months of expenses.',
                'action': 'Build emergency fund'
            })
            tasks.append('Set up automatic transfers to savings account')
            tasks.append(f'Target to save ${cash_flow["monthly_expenses"] * 3:.2f} for 3-month emergency fund')
        elif cash_flow['emergency_fund_months'] >= 3 and cash_flow['emergency_fund_months'] < 6:
            recommendations.append({
                'category': 'Emergency Fund',
                'priority': 'Medium',
                'message': f'Your emergency fund covers {cash_flow["emergency_fund_months"]:.1f} months. Good progress! Aim for 6 months.',
                'action': 'Continue building emergency fund'
            })
        
        # Subscription/Renewal recommendations
        if cash_flow['active_subscriptions'] > 0:
            recommendations.append({
                'category': 'Expenses',
                'priority': 'Medium',
                'message': f'You have {cash_flow["active_subscriptions"]} active subscriptions costing ${cash_flow["monthly_expenses"]:.2f}/month. Review and cancel unused services.',
                'action': 'Audit subscriptions'
            })
            tasks.append('Review all active subscriptions and cancel unused ones')
        
        # Income vs Expenses
        if self.profile and self.profile.annual_income:
            monthly_income = float(self.profile.annual_income) / 12
            savings_rate = ((monthly_income - cash_flow['monthly_expenses']) / monthly_income * 100) if monthly_income > 0 else 0
            
            if savings_rate < 20:
                recommendations.append({
                    'category': 'Savings',
                    'priority': 'High',
                    'message': f'Your savings rate is {savings_rate:.1f}%. Financial experts recommend saving at least 20% of income.',
                    'action': 'Increase savings rate'
                })
                tasks.append('Create a budget to identify areas to cut expenses')
                tasks.append('Set up automatic savings of at least 20% of income')
            elif savings_rate >= 20:
                recommendations.append({
                    'category': 'Savings',
                    'priority': 'Low',
                    'message': f'Great job! Your savings rate is {savings_rate:.1f}%. Keep it up!',
                    'action': 'Maintain current savings discipline'
                })
        
        # General financial freedom recommendation
        if not recommendations:
            recommendations.append({
                'category': 'General',
                'priority': 'Low',
                'message': 'Your finances look healthy! Continue monitoring and adjusting as needed.',
                'action': 'Regular financial review'
            })
            tasks.append('Review financial status quarterly')
        else:
            tasks.append('Set specific financial goals with timelines')
            tasks.append('Track progress monthly and adjust strategy as needed')
        
        return {
            'recommendations': recommendations,
            'tasks': tasks,
            'summary': {
                'total_recommendations': len(recommendations),
                'high_priority': sum(1 for r in recommendations if r['priority'] == 'High'),
                'medium_priority': sum(1 for r in recommendations if r['priority'] == 'Medium'),
                'low_priority': sum(1 for r in recommendations if r['priority'] == 'Low'),
            }
        }
    
    def get_full_analysis(self):
        """Get complete financial analysis"""
        return {
            'investment_analysis': self.analyze_investments(),
            'cash_flow_analysis': self.analyze_cash_flow(),
            'recommendations': self.generate_recommendations()
        }
