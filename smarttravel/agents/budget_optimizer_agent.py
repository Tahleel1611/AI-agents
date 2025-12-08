"""Budget Optimizer Agent - Maximizes value within budget constraints

Specialized agent for optimizing travel expenses and finding the best value
options for flights, accommodations, and activities within user's budget.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class PriorityCategory(Enum):
    """Budget allocation priorities"""
    ACCOMMODATION = "accommodation"
    TRANSPORTATION = "transportation"
    FOOD = "food"
    ACTIVITIES = "activities"
    EMERGENCY = "emergency"


class BudgetTier(Enum):
    """Travel budget tiers"""
    BUDGET = "budget"  # Economy options
    MID_RANGE = "mid_range"  # Balanced value
    LUXURY = "luxury"  # Premium options


@dataclass
class BudgetBreakdown:
    """Recommended budget allocation"""
    total_budget: float
    accommodation: float = 0.0
    transportation: float = 0.0
    food: float = 0.0
    activities: float = 0.0
    emergency_fund: float = 0.0
    remaining: float = 0.0
    
    def __post_init__(self):
        """Calculate remaining after allocations"""
        allocated = (
            self.accommodation + 
            self.transportation + 
            self.food + 
            self.activities + 
            self.emergency_fund
        )
        self.remaining = self.total_budget - allocated


@dataclass
class OptimizedOption:
    """A budget-optimized travel option"""
    category: str
    name: str
    price: float
    value_score: float  # Price-to-quality ratio
    savings: float  # Amount saved vs average
    features: List[str] = field(default_factory=list)
    tier: BudgetTier = BudgetTier.MID_RANGE


@dataclass  
class BudgetOptimizationResult:
    """Complete budget optimization results"""
    breakdown: BudgetBreakdown
    optimized_options: List[OptimizedOption] = field(default_factory=list)
    money_saving_tips: List[str] = field(default_factory=list)
    estimated_total: float = 0.0
    potential_savings: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)


class BudgetOptimizerAgent:
    """Agent specialized in budget optimization and value maximization
    
    Analyzes travel options to find the best value within budget constraints,
    provides money-saving recommendations, and optimizes spending allocation.
    """
    
    # Default budget allocation percentages
    DEFAULT_ALLOCATION = {
        PriorityCategory.ACCOMMODATION: 0.35,
        PriorityCategory.TRANSPORTATION: 0.25,
        PriorityCategory.FOOD: 0.20,
        PriorityCategory.ACTIVITIES: 0.15,
        PriorityCategory.EMERGENCY: 0.05,
    }
    
    def __init__(self, config=None):
        """Initialize the Budget Optimizer Agent
        
        Args:
            config: Configuration object with settings
        """
        self.config = config
        self.initialized_at = datetime.now()
        logger.info("BudgetOptimizerAgent initialized")
    
    def optimize_budget(
        self,
        total_budget: float,
        duration_days: int,
        priorities: Optional[Dict[PriorityCategory, float]] = None
    ) -> BudgetBreakdown:
        """Create optimized budget breakdown
        
        Args:
            total_budget: Total available budget
            duration_days: Trip duration in days
            priorities: Custom priority weights (optional)
        
        Returns:
            BudgetBreakdown with recommended allocation
        """
        logger.info(f"Optimizing budget: ${total_budget} for {duration_days} days")
        
        # Use custom priorities or defaults
        allocation_weights = priorities if priorities else self.DEFAULT_ALLOCATION
        
        # Calculate per-category budgets
        accommodation = total_budget * allocation_weights.get(
            PriorityCategory.ACCOMMODATION, 0.35
        )
        transportation = total_budget * allocation_weights.get(
            PriorityCategory.TRANSPORTATION, 0.25
        )
        food = total_budget * allocation_weights.get(
            PriorityCategory.FOOD, 0.20
        )
        activities = total_budget * allocation_weights.get(
            PriorityCategory.ACTIVITIES, 0.15
        )
        emergency = total_budget * allocation_weights.get(
            PriorityCategory.EMERGENCY, 0.05
        )
        
        return BudgetBreakdown(
            total_budget=total_budget,
            accommodation=accommodation,
            transportation=transportation,
            food=food,
            activities=activities,
            emergency_fund=emergency
        )
    
    def find_best_value_options(
        self,
        options: List[Dict[str, Any]],
        budget: float,
        category: str
    ) -> List[OptimizedOption]:
        """Find best value options within budget
        
        Args:
            options: List of available options with price and features
            budget: Maximum budget for this category
            category: Category name (flights, hotels, etc.)
        
        Returns:
            List of OptimizedOption sorted by value score
        """
        optimized = []
        
        # Calculate average price for comparison
        if options:
            avg_price = sum(opt.get("price", 0) for opt in options) / len(options)
        else:
            avg_price = budget
        
        for option in options:
            price = option.get("price", 0)
            
            # Skip if over budget
            if price > budget:
                continue
            
            # Calculate value score (higher is better)
            # Based on price vs features
            features = option.get("features", [])
            rating = option.get("rating", 3.0)
            
            # Simple value formula: (rating * features) / price
            value_score = (rating * (len(features) + 1)) / (price if price > 0 else 1)
            
            # Calculate savings
            savings = avg_price - price
            
            # Determine tier
            tier = self._determine_tier(price, avg_price)
            
            optimized.append(OptimizedOption(
                category=category,
                name=option.get("name", "Unknown"),
                price=price,
                value_score=value_score,
                savings=max(0, savings),
                features=features,
                tier=tier
            ))
        
        # Sort by value score (best value first)
        optimized.sort(key=lambda x: x.value_score, reverse=True)
        
        return optimized
    
    def generate_money_saving_tips(
        self,
        destination: str,
        duration_days: int,
        budget_tier: BudgetTier = BudgetTier.MID_RANGE
    ) -> List[str]:
        """Generate personalized money-saving tips
        
        Args:
            destination: Travel destination
            duration_days: Trip duration
            budget_tier: User's budget tier
        
        Returns:
            List of money-saving tips
        """
        tips = []
        
        # General tips
        tips.append("Book flights and accommodation in advance for better rates")
        tips.append("Travel during off-peak season for significant savings")
        tips.append("Use public transportation instead of taxis or rideshares")
        
        if budget_tier == BudgetTier.BUDGET:
            tips.extend([
                "Consider hostels or budget hotels for accommodation",
                "Cook some meals instead of dining out for every meal",
                "Look for free walking tours and attractions",
                "Buy groceries from local markets instead of tourist areas"
            ])
        elif budget_tier == BudgetTier.MID_RANGE:
            tips.extend([
                "Mix budget and mid-range accommodation for balance",
                "Have lunch at restaurants instead of dinner for lower prices",
                "Book combination tickets for multiple attractions",
                "Use hotel loyalty programs for perks and discounts"
            ])
        
        # Duration-based tips
        if duration_days >= 7:
            tips.append("Consider weekly rental rates for accommodation")
            tips.append("Buy a multi-day transit pass for unlimited travel")
        
        return tips
    
    def calculate_trip_cost(
        self,
        breakdown: BudgetBreakdown,
        selected_options: Dict[str, float]
    ) -> Tuple[float, float]:
        """Calculate actual trip cost and potential savings
        
        Args:
            breakdown: Recommended budget breakdown
            selected_options: Actual costs per category
        
        Returns:
            Tuple of (total_cost, potential_savings)
        """
        total_cost = sum(selected_options.values())
        
        # Calculate how much under/over budget
        potential_savings = breakdown.total_budget - total_cost
        
        return total_cost, potential_savings
    
    def optimize_itinerary(
        self,
        total_budget: float,
        duration_days: int,
        destination: str,
        available_options: Dict[str, List[Dict]]
    ) -> BudgetOptimizationResult:
        """Create complete budget-optimized itinerary
        
        Args:
            total_budget: Total travel budget
            duration_days: Trip duration
            destination: Destination city/country
            available_options: Dict of available options per category
        
        Returns:
            Complete BudgetOptimizationResult
        """
        logger.info(f"Creating optimized itinerary for {destination}")
        
        # Create budget breakdown
        breakdown = self.optimize_budget(total_budget, duration_days)
        
        # Find best value options for each category
        optimized_options = []
        
        for category, budget_amount in [
            ("accommodation", breakdown.accommodation),
            ("transportation", breakdown.transportation),
            ("activities", breakdown.activities)
        ]:
            if category in available_options:
                best_options = self.find_best_value_options(
                    available_options[category],
                    budget_amount,
                    category
                )
                optimized_options.extend(best_options[:3])  # Top 3 per category
        
        # Generate money-saving tips
        tier = self._estimate_budget_tier(total_budget, duration_days)
        tips = self.generate_money_saving_tips(destination, duration_days, tier)
        
        # Calculate estimates
        estimated_total = sum(opt.price for opt in optimized_options)
        potential_savings = total_budget - estimated_total
        
        return BudgetOptimizationResult(
            breakdown=breakdown,
            optimized_options=optimized_options,
            money_saving_tips=tips,
            estimated_total=estimated_total,
            potential_savings=potential_savings
        )
    
    def _determine_tier(self, price: float, avg_price: float) -> BudgetTier:
        """Determine budget tier based on price comparison"""
        if price < avg_price * 0.7:
            return BudgetTier.BUDGET
        elif price > avg_price * 1.3:
            return BudgetTier.LUXURY
        else:
            return BudgetTier.MID_RANGE
    
    def _estimate_budget_tier(
        self, 
        total_budget: float, 
        duration_days: int
    ) -> BudgetTier:
        """Estimate budget tier based on daily budget"""
        daily_budget = total_budget / duration_days if duration_days > 0 else 0
        
        if daily_budget < 100:
            return BudgetTier.BUDGET
        elif daily_budget > 300:
            return BudgetTier.LUXURY
        else:
            return BudgetTier.MID_RANGE
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": "BudgetOptimizerAgent",
            "status": "active",
            "initialized_at": self.initialized_at.isoformat(),
            "features": [
                "budget_optimization",
                "value_analysis",
                "savings_tips",
                "cost_estimation"
            ]
        
