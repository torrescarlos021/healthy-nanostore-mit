"""
Consumer Agent-Based Model
Healthy Nanostore Project - MIT LiftLab 2025

Simulates consumer behavior and healthy product adoption using Mesa ABM.

Agents:
    - Consumers: Different adopter types (innovators, early adopters, etc.)
    - Nanostores: Track inventory and sales
"""

import numpy as np
import random
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

# Note: Mesa is required for full simulation
# pip install mesa
# For now, we provide a simplified standalone version


class AdopterType(Enum):
    """Rogers' adopter categories."""
    INNOVATOR = "innovator"           # 2.5%
    EARLY_ADOPTER = "early_adopter"   # 13.5%
    EARLY_MAJORITY = "early_majority" # 34%
    LATE_MAJORITY = "late_majority"   # 34%
    LAGGARD = "laggard"               # 16%


@dataclass
class AdopterProfile:
    """Behavioral profile for each adopter type."""
    adopter_type: AdopterType
    innovation_sensitivity: float  # Response to external influence
    imitation_sensitivity: float   # Response to social influence
    price_sensitivity: float
    health_awareness: float
    
    @classmethod
    def get_profile(cls, adopter_type: AdopterType) -> 'AdopterProfile':
        """Get predefined profile for adopter type."""
        profiles = {
            AdopterType.INNOVATOR: cls(
                AdopterType.INNOVATOR, 0.8, 0.2, 0.3, 0.9
            ),
            AdopterType.EARLY_ADOPTER: cls(
                AdopterType.EARLY_ADOPTER, 0.6, 0.5, 0.4, 0.7
            ),
            AdopterType.EARLY_MAJORITY: cls(
                AdopterType.EARLY_MAJORITY, 0.3, 0.7, 0.6, 0.5
            ),
            AdopterType.LATE_MAJORITY: cls(
                AdopterType.LATE_MAJORITY, 0.1, 0.8, 0.8, 0.3
            ),
            AdopterType.LAGGARD: cls(
                AdopterType.LAGGARD, 0.05, 0.4, 0.9, 0.2
            )
        }
        return profiles[adopter_type]


class Consumer:
    """Consumer agent in the simulation."""
    
    def __init__(self, consumer_id: int, profile: AdopterProfile, income: float = 8000):
        self.id = consumer_id
        self.profile = profile
        self.income = income
        self.adopted = False
        self.adoption_step = None
        self.purchases = []
    
    def consider_adoption(self, p: float, q: float, adoption_rate: float) -> bool:
        """
        Decide whether to adopt healthy products.
        
        Uses Bass model framework:
        P(adopt) = p * innovation_sensitivity + q * adoption_rate * imitation_sensitivity
        """
        if self.adopted:
            return True
        
        innovation_effect = p * self.profile.innovation_sensitivity
        imitation_effect = q * adoption_rate * self.profile.imitation_sensitivity
        health_factor = self.profile.health_awareness
        
        prob_adopt = (innovation_effect + imitation_effect) * health_factor
        
        if random.random() < prob_adopt:
            self.adopted = True
            return True
        
        return False
    
    def make_purchase(self) -> str:
        """Decide what to purchase (healthy vs processed)."""
        base_prob = self.profile.health_awareness
        
        if self.adopted:
            base_prob = min(0.95, base_prob + 0.4)
        
        price_factor = 1 - (self.profile.price_sensitivity * 0.3)
        
        return "healthy" if random.random() < (base_prob * price_factor) else "processed"


class Nanostore:
    """Nanostore agent in the simulation."""
    
    PRICES = {"healthy": 50, "processed": 30}
    
    def __init__(self, store_id: int):
        self.id = store_id
        self.inventory = {"healthy": 20, "processed": 40}
        self.sales = {"healthy": 0, "processed": 0}
        self.revenue = 0
    
    def sell(self, product_type: str) -> bool:
        """Process a sale."""
        if self.inventory[product_type] <= 0:
            return False
        
        self.inventory[product_type] -= 1
        self.sales[product_type] += 1
        self.revenue += self.PRICES[product_type]
        return True
    
    def restock(self):
        """Restock inventory."""
        for product in ["healthy", "processed"]:
            if self.inventory[product] < 10:
                self.inventory[product] += 20
    
    @property
    def healthy_ratio(self) -> float:
        """Ratio of healthy to total sales."""
        total = sum(self.sales.values())
        return self.sales["healthy"] / total if total > 0 else 0


class SimplifiedABM:
    """
    Simplified Agent-Based Model for nanostore simulation.
    
    This is a standalone version. For full spatial simulation, use Mesa.
    
    Example:
        >>> model = SimplifiedABM(num_consumers=500, num_stores=10)
        >>> model.run(steps=100)
        >>> print(model.get_results())
    """
    
    # Adopter distribution (Rogers)
    ADOPTER_DIST = {
        AdopterType.INNOVATOR: 0.025,
        AdopterType.EARLY_ADOPTER: 0.135,
        AdopterType.EARLY_MAJORITY: 0.34,
        AdopterType.LATE_MAJORITY: 0.34,
        AdopterType.LAGGARD: 0.16
    }
    
    def __init__(
        self,
        num_consumers: int = 500,
        num_stores: int = 10,
        p: float = 0.03,
        q: float = 0.38,
        seed: int = 42
    ):
        random.seed(seed)
        np.random.seed(seed)
        
        self.p = p
        self.q = q
        self.num_consumers = num_consumers
        self.step_count = 0
        
        # Create stores
        self.stores = [Nanostore(i) for i in range(num_stores)]
        
        # Create consumers with appropriate distribution
        self.consumers = []
        consumer_id = 0
        
        for adopter_type, proportion in self.ADOPTER_DIST.items():
            count = int(num_consumers * proportion)
            profile = AdopterProfile.get_profile(adopter_type)
            
            for _ in range(count):
                income = np.random.lognormal(mean=8.9, sigma=0.5)
                income = max(3000, min(income, 30000))
                
                self.consumers.append(Consumer(consumer_id, profile, income))
                consumer_id += 1
        
        # History tracking
        self.history = {
            "adoption_rate": [],
            "healthy_ratio": [],
            "total_revenue": []
        }
    
    def get_adoption_rate(self) -> float:
        """Current adoption rate."""
        adopters = sum(1 for c in self.consumers if c.adopted)
        return adopters / len(self.consumers)
    
    def step(self):
        """Execute one simulation step."""
        adoption_rate = self.get_adoption_rate()
        
        for consumer in self.consumers:
            # Consider adoption
            consumer.consider_adoption(self.p, self.q, adoption_rate)
            
            # Make purchase
            product = consumer.make_purchase()
            store = random.choice(self.stores)
            store.sell(product)
        
        # Restock stores
        for store in self.stores:
            store.restock()
        
        # Record history
        self.history["adoption_rate"].append(self.get_adoption_rate())
        self.history["healthy_ratio"].append(
            np.mean([s.healthy_ratio for s in self.stores])
        )
        self.history["total_revenue"].append(
            sum(s.revenue for s in self.stores)
        )
        
        self.step_count += 1
    
    def run(self, steps: int = 100):
        """Run simulation for specified steps."""
        for _ in range(steps):
            self.step()
    
    def get_results(self) -> Dict:
        """Get simulation results."""
        return {
            "steps_completed": self.step_count,
            "final_adoption_rate": self.get_adoption_rate(),
            "final_healthy_ratio": np.mean([s.healthy_ratio for s in self.stores]),
            "total_revenue": sum(s.revenue for s in self.stores),
            "total_adopters": sum(1 for c in self.consumers if c.adopted),
            "adoption_by_type": {
                t.value: sum(1 for c in self.consumers 
                            if c.profile.adopter_type == t and c.adopted)
                for t in AdopterType
            }
        }


if __name__ == "__main__":
    print("=" * 60)
    print("CONSUMER ABM - Healthy Nanostore Project")
    print("=" * 60)
    
    # Create and run model
    print("\nInitializing model...")
    model = SimplifiedABM(
        num_consumers=500,
        num_stores=10,
        p=0.03,
        q=0.38
    )
    
    print(f"  Consumers: {len(model.consumers)}")
    print(f"  Stores: {len(model.stores)}")
    print(f"  p: {model.p}, q: {model.q}")
    
    print("\nRunning simulation (100 steps)...")
    model.run(steps=100)
    
    # Results
    results = model.get_results()
    
    print(f"\nResults:")
    print(f"  Final adoption rate: {results['final_adoption_rate']:.1%}")
    print(f"  Final healthy ratio: {results['final_healthy_ratio']:.1%}")
    print(f"  Total revenue: ${results['total_revenue']:,.0f} MXN")
    
    print(f"\nAdoption by type:")
    for adopter_type, count in results['adoption_by_type'].items():
        print(f"  {adopter_type}: {count}")
    
    print("\n" + "=" * 60)
