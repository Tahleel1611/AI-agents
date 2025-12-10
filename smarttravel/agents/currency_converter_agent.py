"""Currency Converter Agent - Handles multi-currency conversions for international travel

Specialized agent for converting currencies, calculating exchange rates,
and providing budget estimates in multiple currencies for international trips.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class Currency(Enum):
    """Major world currencies"""
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound
    JPY = "JPY"  # Japanese Yen
    INR = "INR"  # Indian Rupee
    AUD = "AUD"  # Australian Dollar
    CAD = "CAD"  # Canadian Dollar
    CHF = "CHF"  # Swiss Franc
    CNY = "CNY"  # Chinese Yuan
    AED = "AED"  # UAE Dirham
    SGD = "SGD"  # Singapore Dollar
    MYR = "MYR"  # Malaysian Ringgit
    THB = "THB"  # Thai Baht
    KRW = "KRW"  # South Korean Won


@dataclass
class ExchangeRate:
    """Exchange rate information"""
    from_currency: str
    to_currency: str
    rate: float
    last_updated: datetime = field(default_factory=datetime.now)
    
    def convert(self, amount: float) -> float:
        """Convert amount using this exchange rate"""
        return amount * self.rate


@dataclass
class CurrencyConversion:
    """Result of a currency conversion"""
    original_amount: float
    original_currency: str
    converted_amount: float
    converted_currency: str
    exchange_rate: float
    conversion_date: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.original_amount:.2f} {self.original_currency} = {self.converted_amount:.2f} {self.converted_currency}"


@dataclass
class MultiBudgetBreakdown:
    """Budget breakdown in multiple currencies"""
    base_amount: float
    base_currency: str
    conversions: Dict[str, float] = field(default_factory=dict)
    exchange_rates: Dict[str, float] = field(default_factory=dict)
    
    def add_conversion(self, currency: str, amount: float, rate: float):
        """Add a currency conversion to the breakdown"""
        self.conversions[currency] = amount
        self.exchange_rates[currency] = rate


class CurrencyConverterAgent:
    """Agent specialized in currency conversion and multi-currency budgeting
    
    Provides real-time exchange rates, currency conversions, and helps travelers
    understand costs in different currencies for international trips.
    """
    
    # Approximate exchange rates (to INR) - In production, use live API
    EXCHANGE_RATES = {
        "USD": 83.12,  # 1 USD = 83.12 INR
        "EUR": 90.45,  # 1 EUR = 90.45 INR
        "GBP": 105.32,  # 1 GBP = 105.32 INR
        "JPY": 0.56,   # 1 JPY = 0.56 INR
        "INR": 1.00,   # 1 INR = 1 INR
        "AUD": 54.23,  # 1 AUD = 54.23 INR
        "CAD": 61.45,  # 1 CAD = 61.45 INR
        "CHF": 95.67,  # 1 CHF = 95.67 INR
        "CNY": 11.54,  # 1 CNY = 11.54 INR
        "AED": 22.63,  # 1 AED = 22.63 INR
        "SGD": 61.89,  # 1 SGD = 61.89 INR
        "MYR": 18.67,  # 1 MYR = 18.67 INR
        "THB": 2.35,   # 1 THB = 2.35 INR
        "KRW": 0.063,  # 1 KRW = 0.063 INR
    }
    
    # Popular tourist destinations and their currencies
    DESTINATION_CURRENCIES = {
        "USA": "USD",
        "United States": "USD",
        "Europe": "EUR",
        "UK": "GBP",
        "United Kingdom": "GBP",
        "London": "GBP",
        "Japan": "JPY",
        "Tokyo": "JPY",
        "India": "INR",
        "Australia": "AUD",
        "Canada": "CAD",
        "Switzerland": "CHF",
        "China": "CNY",
        "Dubai": "AED",
        "UAE": "AED",
        "Singapore": "SGD",
        "Malaysia": "MYR",
        "Thailand": "THB",
        "Bangkok": "THB",
        "South Korea": "KRW",
        "Seoul": "KRW",
    }
    
    def __init__(self, config=None):
        """Initialize the Currency Converter Agent
        
        Args:
            config: Configuration object with settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("CurrencyConverterAgent initialized")
    
    def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> CurrencyConversion:
        """Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., 'USD')
            to_currency: Target currency code (e.g., 'INR')
        
        Returns:
            CurrencyConversion with conversion details
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        logger.info(f"Converting {amount} {from_currency} to {to_currency}")
        
        # Get exchange rates to INR
        from_rate = self.EXCHANGE_RATES.get(from_currency, 1.0)
        to_rate = self.EXCHANGE_RATES.get(to_currency, 1.0)
        
        # Convert: amount -> INR -> target currency
        amount_in_inr = amount * from_rate
        converted_amount = amount_in_inr / to_rate
        
        # Exchange rate (direct from source to target)
        exchange_rate = from_rate / to_rate
        
        return CurrencyConversion(
            original_amount=amount,
            original_currency=from_currency,
            converted_amount=converted_amount,
            converted_currency=to_currency,
            exchange_rate=exchange_rate
        )
    
    def get_destination_currency(self, destination: str) -> Optional[str]:
        """Get the primary currency for a destination
        
        Args:
            destination: Destination name or country
        
        Returns:
            Currency code or None if not found
        """
        # Check exact matches first
        if destination in self.DESTINATION_CURRENCIES:
            return self.DESTINATION_CURRENCIES[destination]
        
        # Check case-insensitive partial matches
        destination_lower = destination.lower()
        for location, currency in self.DESTINATION_CURRENCIES.items():
            if location.lower() in destination_lower or destination_lower in location.lower():
                return currency
        
        return None
    
    def convert_budget_to_destination(
        self,
        budget: float,
        budget_currency: str,
        destination: str
    ) -> Optional[CurrencyConversion]:
        """Convert budget to destination's local currency
        
        Args:
            budget: Budget amount
            budget_currency: Currency of the budget
            destination: Destination name
        
        Returns:
            CurrencyConversion or None if destination currency unknown
        """
        dest_currency = self.get_destination_currency(destination)
        
        if not dest_currency:
            logger.warning(f"Could not determine currency for destination: {destination}")
            return None
        
        return self.convert(budget, budget_currency, dest_currency)
    
    def get_multi_currency_breakdown(
        self,
        amount: float,
        base_currency: str,
        target_currencies: List[str]
    ) -> MultiBudgetBreakdown:
        """Get budget breakdown in multiple currencies
        
        Args:
            amount: Base amount
            base_currency: Base currency code
            target_currencies: List of target currency codes
        
        Returns:
            MultiBudgetBreakdown with conversions
        """
        breakdown = MultiBudgetBreakdown(
            base_amount=amount,
            base_currency=base_currency.upper()
        )
        
        for currency in target_currencies:
            if currency.upper() == base_currency.upper():
                continue
            
            conversion = self.convert(amount, base_currency, currency)
            breakdown.add_conversion(
                currency.upper(),
                conversion.converted_amount,
                conversion.exchange_rate
            )
        
        return breakdown
    
    def estimate_daily_costs(
        self,
        destination: str,
        budget_tier: str = "mid_range"
    ) -> Dict[str, Any]:
        """Estimate daily costs in destination currency
        
        Args:
            destination: Destination name
            budget_tier: 'budget', 'mid_range', or 'luxury'
        
        Returns:
            Dictionary with estimated daily costs
        """
        dest_currency = self.get_destination_currency(destination) or "USD"
        
        # Base estimates in USD (can be converted)
        estimates = {
            "budget": {
                "accommodation": 30,
                "food": 20,
                "transportation": 10,
                "activities": 15,
                "total": 75
            },
            "mid_range": {
                "accommodation": 80,
                "food": 50,
                "transportation": 25,
                "activities": 45,
                "total": 200
            },
            "luxury": {
                "accommodation": 200,
                "food": 100,
                "transportation": 50,
                "activities": 100,
                "total": 450
            }
        }
        
        base_estimate = estimates.get(budget_tier, estimates["mid_range"])
        
        # Convert to destination currency
        converted_estimate = {}
        for category, usd_amount in base_estimate.items():
            conversion = self.convert(usd_amount, "USD", dest_currency)
            converted_estimate[category] = {
                "amount": round(conversion.converted_amount, 2),
                "currency": dest_currency
            }
        
        return {
            "destination": destination,
            "budget_tier": budget_tier,
            "daily_costs": converted_estimate,
            "currency": dest_currency
        }
    
    def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str
    ) -> ExchangeRate:
        """Get current exchange rate between two currencies
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
        
        Returns:
            ExchangeRate object
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        from_rate = self.EXCHANGE_RATES.get(from_currency, 1.0)
        to_rate = self.EXCHANGE_RATES.get(to_currency, 1.0)
        
        rate = from_rate / to_rate
        
        return ExchangeRate(
            from_currency=from_currency,
            to_currency=to_currency,
            rate=rate
        )
    
    def get_currency_tips(self, destination: str) -> List[str]:
        """Get currency-related tips for a destination
        
        Args:
            destination: Destination name
        
        Returns:
            List of helpful currency tips
        """
        dest_currency = self.get_destination_currency(destination)
        
        general_tips = [
            "Notify your bank before traveling internationally",
            "Use credit cards with no foreign transaction fees",
            "Avoid airport currency exchanges (poor rates)",
            "Use ATMs for better exchange rates than currency counters",
            "Keep some cash for small vendors who don't accept cards"
        ]
        
        if dest_currency:
            general_tips.insert(0, f"The local currency in {destination} is {dest_currency}")
        
        return general_tips
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "CurrencyConverterAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat(),
            "supported_currencies": len(self.EXCHANGE_RATES),
            "features": [
                "currency_conversion",
                "multi_currency_budgeting",
                "exchange_rates",
                "destination_currency_detection",
                "daily_cost_estimation"
            ]
        }
