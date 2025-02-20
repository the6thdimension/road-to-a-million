#!/usr/bin/env python3
# coding: utf-8
"""
Road to $1,000,000 Financial Projection Tool

This script helps users estimate the time required to accumulate $1,000,000
based on their current income, expenses, and age.
"""

import time
import logging
from typing import Tuple, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_validated_input(prompt: str, input_type: type = int) -> int:
    """
    Get validated input from user with error handling.
    
    Args:
        prompt (str): Input prompt message
        input_type (type): Expected input type (default: int)
    
    Returns:
        Validated input of specified type
    """
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def get_age() -> int:
    """
    Prompt user for their current age.
    
    Returns:
        User's age as an integer
    """
    return get_validated_input("How old are you? -- ")

def get_simplified_input(prompt: str, valid_options: Dict[str, str]) -> str:
    """
    Get simplified single-letter input from user.
    
    Args:
        prompt (str): Input prompt message
        valid_options (Dict[str, str]): Dictionary of valid options {short_form: full_form}
    
    Returns:
        str: Full form of selected option
    """
    options_str = '/'.join(valid_options.keys())
    while True:
        user_input = input(f"{prompt} ({options_str}): ").lower()
        if user_input in valid_options:
            return valid_options[user_input]
        print(f"Invalid input. Please enter one of: {options_str}")

def get_detailed_expenses() -> Dict[str, float]:
    """
    Get detailed monthly expenses breakdown.
    
    Returns:
        Dictionary containing expense categories and amounts
    """
    expense_categories = {
        'Housing': [
            ('rent_or_mortgage', 'Rent/Mortgage payment'),
            ('property_tax', 'Property tax (if homeowner)'),
            ('home_insurance', 'Home/Rental insurance')
        ],
        'Utilities': [
            ('electric', 'Electricity'),
            ('gas', 'Gas'),
            ('water', 'Water'),
            ('internet', 'Internet'),
            ('phone', 'Phone')
        ],
        'Transportation': [
            ('car_payment', 'Car payment'),
            ('car_insurance', 'Car insurance'),
            ('fuel', 'Fuel'),
            ('maintenance', 'Car maintenance')
        ],
        'Subscriptions': [
            ('streaming', 'Streaming services (Netflix, etc.)'),
            ('gym', 'Gym membership'),
            ('other_subs', 'Other subscriptions')
        ],
        'Living': [
            ('groceries', 'Groceries'),
            ('dining_out', 'Dining out'),
            ('healthcare', 'Healthcare/Medical'),
            ('misc', 'Miscellaneous expenses')
        ]
    }
    
    expenses = {}
    total_by_category = {}
    
    print("\n--- Monthly Expenses Breakdown ---")
    for category, items in expense_categories.items():
        print(f"\n{category}:")
        category_total = 0
        for key, desc in items:
            amount = get_validated_input(f"{desc}: $", float)
            expenses[key] = amount
            category_total += amount
        total_by_category[category] = category_total
    
    # Get housing status and calculate rent projection
    housing_status = get_simplified_input("Do you rent or own", {'r': 'rent', 'o': 'own'})
    if housing_status == 'rent':
        years = get_validated_input("How many years have you been renting? ", int)
        monthly_rent = expenses.get('rent_or_mortgage', 0)
        total_rent_paid = monthly_rent * 12 * years
        expenses['total_rent_paid'] = total_rent_paid
        expenses['years_renting'] = years
    
    expenses['housing_status'] = housing_status
    expenses['category_totals'] = total_by_category
    expenses['total_monthly'] = sum(total_by_category.values())
    
    return expenses

def get_job_info() -> Tuple[float, float, str]:
    """
    Get user's income information with flexible input for hourly or salary workers.
    
    Returns:
        Tuple of (income rate, hours/work days, income type)
    """
    while True:
        income_type = input("Are you paid hourly or salary? (hourly/salary): ").lower()
        
        if income_type not in ['hourly', 'salary']:
            print("Invalid input. Please enter 'hourly' or 'salary'.")
            continue
        
        if income_type == 'hourly':
            wage = get_validated_input('What is your hourly rate? -- ', float)
            hours = get_validated_input('How many hours a day do you work? -- ')
            return wage, hours, income_type
        
        else:  # salary
            annual_income = get_validated_input('What is your annual salary? -- ', float)
            # For salary, we'll use the annual income directly
            return annual_income, 0, income_type

def calculate_federal_tax(annual_gross_income: float, filing_status: str = 'single') -> Dict[str, float]:
    """
    Calculate federal income tax based on 2024 tax brackets.
    
    Args:
        annual_gross_income (float): Total annual income before taxes
        filing_status (str): Tax filing status (single, married, head_of_household)
    
    Returns:
        Dictionary containing tax amount and effective tax rate
    """
    # 2024 Standard Deduction
    standard_deductions = {
        'single': 14_600,
        'married': 29_200,
        'head_of_household': 21_900
    }
    
    # 2024 Tax Brackets for Single Filers
    tax_brackets_single = [
        (0, 11_600, 0.10),
        (11_600, 47_150, 0.12),
        (47_150, 100_525, 0.22),
        (100_525, 191_950, 0.24),
        (191_950, 243_725, 0.32),
        (243_725, 609_350, 0.35),
        (609_350, float('inf'), 0.37)
    ]
    
    # Validate filing status
    if filing_status not in standard_deductions:
        logger.warning(f"Invalid filing status '{filing_status}'. Defaulting to 'single'.")
        filing_status = 'single'
    
    # Subtract standard deduction
    taxable_income = max(annual_gross_income - standard_deductions[filing_status], 0)
    
    # Calculate tax
    total_tax = 0
    remaining_income = taxable_income
    
    for lower, upper, rate in tax_brackets_single:
        if remaining_income <= 0:
            break
            
        bracket_income = min(remaining_income, upper - lower)
        total_tax += bracket_income * rate
        remaining_income -= bracket_income
    
    # Calculate effective tax rate
    effective_tax_rate = (total_tax / annual_gross_income * 100) if annual_gross_income > 0 else 0
    
    return {
        'tax_amount': total_tax,
        'effective_tax_rate': effective_tax_rate,
        'taxable_income': taxable_income
    }

def calculate_finance(income_rate: float, hours: float, expenses: Dict[str, float], income_type: str, filing_status: str = 'single') -> Dict[str, float]:
    """
    Calculate yearly financial breakdown after expenses and taxes.
    
    Args:
        income_rate (float): Hourly rate or annual salary
        hours (float): Hours worked per day (only used for hourly)
        expenses (Dict[str, float]): Monthly expenses
        income_type (str): Type of income (hourly or salary)
        filing_status (str): Tax filing status
    
    Returns:
        Dictionary with detailed financial breakdown
    """
    if income_type == 'hourly':
        weekly_gross = income_rate * hours * 5
        annual_gross = weekly_gross * 52
    else:  # salary
        annual_gross = income_rate
    
    # Calculate federal taxes
    federal_tax_result = calculate_federal_tax(annual_gross, filing_status)
    federal_tax = federal_tax_result['tax_amount']
    
    # Calculate Social Security and Medicare taxes (approximate)
    social_security_tax = min(annual_gross * 0.062, 160_200 * 0.062)  # 6.2% up to wage base
    medicare_tax = annual_gross * 0.0145  # 1.45%
    total_payroll_taxes = social_security_tax + medicare_tax
    
    # Total taxes
    total_taxes = federal_tax + total_payroll_taxes
    
    # Calculate net income after taxes and expenses
    monthly_gross = annual_gross / 12
    monthly_expenses = expenses['total_monthly']
    monthly_tax = total_taxes / 12
    monthly_net = max(monthly_gross - monthly_expenses - monthly_tax, 0)
    
    # Yearly calculations
    yearly_net = monthly_net * 12
    
    return {
        'annual_gross': annual_gross,
        'federal_income_tax': federal_tax,
        'social_security_tax': social_security_tax,
        'medicare_tax': medicare_tax,
        'total_taxes': total_taxes,
        'monthly_expenses': monthly_expenses,
        'monthly_net_income': monthly_net,
        'yearly_net_income': yearly_net,
        'effective_tax_rate': federal_tax_result['effective_tax_rate']
    }

def project_financial_freedom(age: int, yearly_savings: float) -> int:
    """
    Project the years needed to reach $1,000,000.
    
    Args:
        age (int): Current age
        yearly_savings (float): Annual savings
    
    Returns:
        Number of years to reach $1,000,000
    """
    gross = 0
    years_to_goal = 0
    
    while gross < 1_000_000:
        age += 1
        gross += yearly_savings
        years_to_goal += 1
        
        print(f'At {age} years old, you will have collected ${gross:.2f} dollars.')
    
    return years_to_goal

def display_intro() -> None:
    """Display introduction and instructions."""
    print('=' * 60)
    print(' !!! ROAD TO $1,000,000 CASH !!! ')
    print('=' * 60)
    print("""
Created by Joshua McMahon (The 6th Dimension)

Purpose: Estimate your journey to $1,000,000
Motivation: Challenge traditional employment limits
Inspiration: Chase your dreams, take risks, be innovative!
""")
    print('Instructions: Enter whole numbers or decimal values')
    print('=' * 60)

def main() -> None:
    """Main program execution flow."""
    try:
        display_intro()
        
        age = get_age()
        income_rate, hours, income_type = get_job_info()
        expenses = get_detailed_expenses()
        
        # Get filing status with simplified input
        filing_status = get_simplified_input(
            "What is your tax filing status",
            {'s': 'single', 'm': 'married', 'h': 'head_of_household'}
        )
        
        # Get financial breakdown
        financial_breakdown = calculate_finance(income_rate, hours, expenses, income_type, filing_status)
        
        # Projection to $1,000,000
        years_to_goal = project_financial_freedom(age, financial_breakdown['yearly_net_income'])
        
        # Detailed financial output
        print("\n=== Financial Breakdown ===")
        print(f"Annual Gross Income: ${financial_breakdown['annual_gross']:,.2f}")
        
        print("\n--- Tax Information ---")
        print(f"Federal Income Tax: ${financial_breakdown['federal_income_tax']:,.2f}")
        print(f"Social Security Tax: ${financial_breakdown['social_security_tax']:,.2f}")
        print(f"Medicare Tax: ${financial_breakdown['medicare_tax']:,.2f}")
        print(f"Total Taxes: ${financial_breakdown['total_taxes']:,.2f}")
        print(f"Effective Tax Rate: {financial_breakdown['effective_tax_rate']:.1f}%")
        
        print("\n--- Monthly Expenses by Category ---")
        for category, total in expenses['category_totals'].items():
            print(f"{category}: ${total:,.2f}")
        print(f"Total Monthly Expenses: ${expenses['total_monthly']:,.2f}")
        
        # Show rent information if applicable
        if expenses['housing_status'] == 'rent':
            total_rent = expenses['total_rent_paid']
            years_renting = expenses['years_renting']
            print(f"\n--- Rent Analysis ---")
            print(f"Total rent paid over {years_renting} years: ${total_rent:,.2f}")
            print(f"Average yearly rent: ${(total_rent / years_renting):,.2f}")
        
        print("\n--- Monthly Income ---")
        print(f"Gross Monthly Income: ${financial_breakdown['annual_gross']/12:,.2f}")
        print(f"Net Monthly Income: ${financial_breakdown['monthly_net_income']:,.2f}")
        
        print("\n--- Annual Summary ---")
        print(f"Yearly Net Income: ${financial_breakdown['yearly_net_income']:,.2f}")
        
        # Income type specific description
        income_description = f"{income_type.capitalize()} income" if income_type == 'salary' else f"Hourly rate of ${income_rate:.2f}"
        print(f"\nBased on your {income_description}, it will take approximately {years_to_goal} years to reach $1,000,000.")
        
        print('\nEncouragement: Test different scenarios. Close the gap to your dreams!')
        print('Connect: GitHub/Instagram: @the6thdimension')
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def retry_prompt() -> bool:
    """
    Prompt user to retry or exit the application with simplified input.
    
    Returns:
        Boolean indicating whether to restart
    """
    response = get_simplified_input(
        "Would you like to try again",
        {'y': 'yes', 'n': 'no', 'q': 'quit'}
    )
    if response == 'yes':
        return True
    print('May prosperity and good health be with you!')
    return False

if __name__ == "__main__":
    while True:
        main()
        if not retry_prompt():
            break
