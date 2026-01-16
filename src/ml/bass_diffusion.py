"""
Bass Innovation Diffusion Model
Healthy Nanostore Project - MIT LiftLab 2025

Simulates healthy product adoption in Mexican nanostores using the Bass Model.

Theory:
    The Bass Model (1969) describes innovation adoption through two mechanisms:
    - p (innovation): adoption from external influence (ads, promoters)
    - q (imitation): adoption from social influence (neighbors, family)

Formula:
    dN/dt = (p + q*N/M) * (M - N)
    
    Where:
        N = current adopters
        M = market potential
        p = innovation coefficient
        q = imitation coefficient
"""

import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Dict, Tuple
import json


@dataclass
class DiffusionParams:
    """Parameters for Bass Diffusion Model."""
    p: float = 0.03      # Innovation coefficient (external influence)
    q: float = 0.38      # Imitation coefficient (social influence)  
    M: int = 1_100_824   # Market potential (DENUE 2024 nanostores)


@dataclass
class SimulationResult:
    """Results from diffusion simulation."""
    time: np.ndarray
    adopters: np.ndarray
    adoption_pct: np.ndarray
    time_to_16pct: float  # Critical mass
    time_to_50pct: float  # Majority
    final_adoption: float


class BassDiffusionModel:
    """
    Bass Diffusion Model for nanostore healthy product adoption.
    
    Example:
        >>> model = BassDiffusionModel()
        >>> result = model.simulate(years=10)
        >>> print(f"10-year adoption: {result.final_adoption:.1f}%")
    """
    
    # Intervention effects (multipliers)
    INTERVENTIONS = {
        "health_promoters": {"p_mult": 2.0, "q_mult": 1.0},   # +100% p
        "social_campaign": {"p_mult": 1.0, "q_mult": 1.32},   # +32% q
        "price_subsidy": {"p_mult": 1.5, "q_mult": 1.15},
        "nudge_placement": {"p_mult": 1.3, "q_mult": 1.20},
        "combined": {"p_mult": 2.5, "q_mult": 1.50}
    }
    
    def __init__(self, params: DiffusionParams = None):
        self.params = params or DiffusionParams()
    
    def _bass_ode(self, N: float, t: float, p: float, q: float, M: int) -> float:
        """Bass model differential equation."""
        return (p + q * N / M) * (M - N)
    
    def simulate(self, years: int = 10, steps_per_year: int = 12) -> SimulationResult:
        """Run Bass diffusion simulation."""
        t = np.linspace(0, years, years * steps_per_year)
        
        N = odeint(
            self._bass_ode, 
            1,  # Start with 1 adopter
            t, 
            args=(self.params.p, self.params.q, self.params.M)
        ).flatten()
        
        pct = (N / self.params.M) * 100
        
        return SimulationResult(
            time=t,
            adopters=N,
            adoption_pct=pct,
            time_to_16pct=self._time_to_threshold(t, pct, 16),
            time_to_50pct=self._time_to_threshold(t, pct, 50),
            final_adoption=pct[-1]
        )
    
    def _time_to_threshold(self, t: np.ndarray, pct: np.ndarray, threshold: float) -> float:
        """Find time to reach adoption threshold."""
        idx = np.where(pct >= threshold)[0]
        return t[idx[0]] if len(idx) > 0 else float('inf')
    
    def simulate_intervention(self, intervention: str, years: int = 10) -> SimulationResult:
        """Simulate with specific intervention."""
        if intervention not in self.INTERVENTIONS:
            raise ValueError(f"Unknown intervention: {intervention}")
        
        effects = self.INTERVENTIONS[intervention]
        modified_params = DiffusionParams(
            p=min(self.params.p * effects["p_mult"], 0.99),
            q=min(self.params.q * effects["q_mult"], 0.99),
            M=self.params.M
        )
        
        original_params = self.params
        self.params = modified_params
        result = self.simulate(years)
        self.params = original_params
        
        return result
    
    def compare_scenarios(self, years: int = 10) -> Dict[str, SimulationResult]:
        """Compare all intervention scenarios."""
        results = {"baseline": self.simulate(years)}
        
        for intervention in self.INTERVENTIONS:
            results[intervention] = self.simulate_intervention(intervention, years)
        
        return results
    
    def export_results(self, results: Dict[str, SimulationResult], filepath: str):
        """Export results to JSON."""
        data = {}
        for name, result in results.items():
            data[name] = {
                "time_to_16pct": result.time_to_16pct,
                "time_to_50pct": result.time_to_50pct,
                "final_adoption": result.final_adoption
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def calculate_health_impact(adoption_pct: float) -> Dict[str, float]:
    """
    Calculate health impact from adoption level.
    
    Based on: 100g/day F&V increase → 6% diabetes risk reduction
    """
    population = 126_000_000  # Mexico
    affected = population * (adoption_pct / 100) * 0.31  # 31% shop at tienditas
    
    diabetes_prevalence = 0.18
    risk_reduction = 0.06
    
    prevented_cases = population * diabetes_prevalence * 0.05 * risk_reduction * (adoption_pct / 100)
    dalys_averted = prevented_cases * 15  # ~15 DALYs per diabetes case
    
    return {
        "affected_population": int(affected),
        "prevented_diabetes_cases": int(prevented_cases),
        "dalys_averted": int(dalys_averted)
    }


if __name__ == "__main__":
    print("=" * 60)
    print("BASS DIFFUSION MODEL - Healthy Nanostore Project")
    print("=" * 60)
    
    model = BassDiffusionModel()
    
    print(f"\nParameters:")
    print(f"  p (innovation): {model.params.p}")
    print(f"  q (imitation):  {model.params.q}")
    print(f"  M (market):     {model.params.M:,}")
    
    # Baseline
    baseline = model.simulate(years=10)
    print(f"\nBaseline Results:")
    print(f"  Time to 16% (critical mass): {baseline.time_to_16pct:.1f} years")
    print(f"  Time to 50% (majority):      {baseline.time_to_50pct:.1f} years")
    print(f"  10-year adoption:            {baseline.final_adoption:.1f}%")
    
    # Compare scenarios
    print(f"\nScenario Comparison:")
    print("-" * 50)
    results = model.compare_scenarios(years=10)
    
    for name, result in results.items():
        print(f"  {name:20} | 16%: {result.time_to_16pct:4.1f}y | Final: {result.final_adoption:5.1f}%")
    
    # Health impact
    combined = results["combined"]
    impact = calculate_health_impact(combined.final_adoption)
    
    print(f"\nHealth Impact (Combined Intervention):")
    print(f"  Affected population:      {impact['affected_population']:,}")
    print(f"  Prevented diabetes cases: {impact['prevented_diabetes_cases']:,}")
    print(f"  DALYs averted:            {impact['dalys_averted']:,}")
    
    print("\n" + "=" * 60)
