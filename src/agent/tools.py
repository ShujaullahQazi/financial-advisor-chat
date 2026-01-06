"""
Financial calculation tools for the advisor agent.
"""

from typing import Dict


class FinancialTools:
    """Collection of financial calculation tools."""

    @staticmethod
    def calculate_compound_interest(
        principal: float, rate: float, time: float, compounds_per_year: int = 12
    ) -> Dict:
        """
        Calculate compound interest.

        Args:
            principal: Initial investment amount
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            time: Time period in years
            compounds_per_year: Number of times interest compounds per year

        Returns:
            Dictionary with final_amount, interest_earned, and formula
        """
        amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
        return {
            "final_amount": round(amount, 2),
            "interest_earned": round(amount - principal, 2),
            "formula": f"A = P(1 + r/n)^(nt) = {principal}(1 + {rate}/{compounds_per_year})^({compounds_per_year * time})",
        }

    @staticmethod
    def calculate_loan_payment(principal: float, rate: float, years: int) -> Dict:
        """
        Calculate monthly loan payment.

        Args:
            principal: Loan amount
            rate: Annual interest rate (as percentage, e.g., 5 for 5%)
            years: Loan term in years

        Returns:
            Dictionary with monthly_payment, total_payment, and total_interest
        """
        monthly_rate = rate / 12 / 100
        num_payments = years * 12

        if monthly_rate == 0:
            monthly_payment = principal / num_payments
        else:
            monthly_payment = (
                principal
                * (monthly_rate * (1 + monthly_rate) ** num_payments)
                / ((1 + monthly_rate) ** num_payments - 1)
            )

        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(monthly_payment * num_payments, 2),
            "total_interest": round(monthly_payment * num_payments - principal, 2),
        }

    @staticmethod
    def calculate_retirement_savings(
        monthly_contribution: float, years: int, annual_return: float, current_savings: float = 0
    ) -> Dict:
        """
        Calculate retirement savings projection.

        Args:
            monthly_contribution: Monthly savings amount
            years: Number of years until retirement
            annual_return: Expected annual return (as percentage)
            current_savings: Current retirement savings balance

        Returns:
            Dictionary with total_savings, contributions, and interest_earned
        """
        monthly_return = annual_return / 12 / 100
        num_months = years * 12

        if monthly_return == 0:
            total_savings = current_savings + (monthly_contribution * num_months)
        else:
            total_savings = (
                current_savings * (1 + monthly_return) ** num_months
                + monthly_contribution * ((1 + monthly_return) ** num_months - 1) / monthly_return
            )

        return {
            "total_savings": round(total_savings, 2),
            "contributions": round(monthly_contribution * num_months, 2),
            "interest_earned": round(
                total_savings - (current_savings + monthly_contribution * num_months), 2
            ),
        }

    @staticmethod
    def calculate_emergency_fund(monthly_expenses: float, months_coverage: float = 6) -> Dict:
        """
        Calculate recommended emergency fund size.

        Args:
            monthly_expenses: Monthly expense amount
            months_coverage: Number of months to cover (default: 6)

        Returns:
            Dictionary with recommended_amount and explanation
        """
        recommended_amount = monthly_expenses * months_coverage
        return {
            "recommended_amount": round(recommended_amount, 2),
            "monthly_expenses": monthly_expenses,
            "months_coverage": months_coverage,
            "explanation": f"Emergency fund should cover {months_coverage} months of expenses",
        }
