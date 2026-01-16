"""
Survey Data Analysis
Healthy Nanostore Project - MIT LiftLab 2025

Processes survey data on eating habits and fast food consumption
to calibrate diffusion model parameters.

Data: 104 responses from San Luis Potosí region (December 2025)
"""

import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, List
import json
import sys


class SurveyAnalyzer:
    """
    Analyzer for eating habits survey data.
    
    Extracts behavioral parameters for the Bass diffusion model:
    - Price sensitivity → affects elasticity
    - Health awareness → affects innovation coefficient (p)
    - Social influence → affects imitation coefficient (q)
    """
    
    def __init__(self, filepath: str, delimiter: str = ';'):
        """Load survey data."""
        self.df = pd.read_csv(filepath, delimiter=delimiter, encoding='utf-8-sig')
        self._clean_data()
        self.n_responses = len(self.df)
    
    def _clean_data(self):
        """Clean and preprocess data."""
        self.df = self.df.dropna(axis=1, how='all')
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].astype(str).str.strip()
    
    def get_age_distribution(self) -> Dict[str, int]:
        """Get age group distribution."""
        age_col = 'Edad'
        if age_col in self.df.columns:
            return self.df[age_col].value_counts().to_dict()
        return {}
    
    def get_parent_percentage(self) -> float:
        """Calculate percentage of parents in sample."""
        parent_col = '¿Eres padre/madre?'
        if parent_col in self.df.columns:
            counts = self.df[parent_col].value_counts()
            if 'Si' in counts:
                return counts['Si'] / len(self.df)
        return 0.0
    
    def get_fast_food_frequency(self) -> Dict[str, int]:
        """Extract fast food purchase frequency."""
        ff_cols = [c for c in self.df.columns if 'comida rápida' in c.lower() or 'procesada' in c.lower()]
        
        frequencies = Counter()
        for col in ff_cols:
            for val in self.df[col].dropna():
                if val and val != 'nan':
                    frequencies[val] += 1
        
        return dict(frequencies.most_common())
    
    def get_barriers(self) -> Dict[str, int]:
        """Extract barriers to healthy cooking."""
        barrier_cols = [c for c in self.df.columns if 'no cocinas' in c.lower() or 'desmotiva' in c.lower()]
        
        barriers = Counter()
        for col in barrier_cols:
            for response in self.df[col].dropna():
                if response and response != 'nan':
                    for item in str(response).split(';'):
                        item = item.strip()
                        if item:
                            barriers[item] += 1
        
        return dict(barriers.most_common(10))
    
    def get_willingness_to_change(self) -> float:
        """Calculate willingness to change eating habits."""
        will_cols = [c for c in self.df.columns if 'dispuesto' in c.lower()]
        
        positive = 0
        total = 0
        
        for col in will_cols:
            for response in self.df[col].dropna():
                if response and response != 'nan':
                    total += 1
                    if 'Si' in str(response) or 'Tal vez' in str(response):
                        positive += 1
        
        return positive / total if total > 0 else 0.0
    
    def get_price_sensitivity(self) -> float:
        """Estimate price sensitivity (0-1)."""
        priority_cols = [c for c in self.df.columns if 'priorizar' in c.lower()]
        
        price_mentions = 0
        total = 0
        
        for col in priority_cols:
            for response in self.df[col].dropna():
                if response and response != 'nan':
                    total += 1
                    if 'precio' in str(response).lower():
                        price_mentions += 1
        
        return price_mentions / total if total > 0 else 0.5
    
    def get_health_awareness(self) -> float:
        """Estimate health awareness (0-1)."""
        concern_cols = [c for c in self.df.columns if 'preocupado' in c.lower()]
        
        concerned = 0
        total = 0
        
        for col in concern_cols:
            for response in self.df[col].dropna():
                if response and response != 'nan':
                    total += 1
                    if 'Muy preocupado' in str(response) or 'Algo preocupado' in str(response):
                        concerned += 1
        
        return concerned / total if total > 0 else 0.5
    
    def get_preferred_solutions(self) -> List[str]:
        """Get most requested solutions."""
        sol_cols = [c for c in self.df.columns if 'soluciones' in c.lower()]
        
        solutions = Counter()
        for col in sol_cols:
            for response in self.df[col].dropna():
                if response and response != 'nan':
                    for item in str(response).split(';'):
                        item = item.strip()
                        if item:
                            solutions[item] += 1
        
        return [s for s, _ in solutions.most_common(5)]
    
    def calibrate_model_parameters(self) -> Dict[str, float]:
        """
        Calibrate Bass model parameters from survey data.
        
        Returns calibrated p, q, and elasticity values.
        """
        health_awareness = self.get_health_awareness()
        willingness = self.get_willingness_to_change()
        price_sensitivity = self.get_price_sensitivity()
        parent_pct = self.get_parent_percentage()
        
        # Innovation coefficient (p)
        # Higher health awareness + willingness = higher p
        base_p = 0.03
        p_calibrated = base_p * (1 + health_awareness + willingness) / 2
        p_calibrated = min(max(p_calibrated, 0.01), 0.15)
        
        # Imitation coefficient (q)
        # Higher parent percentage = more community influence
        base_q = 0.38
        q_calibrated = base_q * (1 + parent_pct * 0.3)
        q_calibrated = min(max(q_calibrated, 0.20), 0.60)
        
        # Price elasticity
        base_elasticity = -0.59
        elasticity = base_elasticity * (1 + price_sensitivity * 0.5)
        
        return {
            "p_calibrated": round(p_calibrated, 4),
            "q_calibrated": round(q_calibrated, 4),
            "price_elasticity": round(elasticity, 4),
            "health_awareness": round(health_awareness, 4),
            "willingness_to_change": round(willingness, 4),
            "price_sensitivity": round(price_sensitivity, 4),
            "sample_size": self.n_responses
        }
    
    def generate_report(self) -> str:
        """Generate text report of findings."""
        age = self.get_age_distribution()
        params = self.calibrate_model_parameters()
        barriers = self.get_barriers()
        solutions = self.get_preferred_solutions()
        
        report = f"""
{'='*60}
SURVEY ANALYSIS REPORT
Eating Habits and Fast Food Consumption
Healthy Nanostore Project - MIT LiftLab 2025
{'='*60}

SAMPLE: {self.n_responses} responses
REGION: San Luis Potosí, Mexico
DATE: December 2025

AGE DISTRIBUTION
{'─'*40}
"""
        for age_group, count in sorted(age.items()):
            pct = count / self.n_responses * 100
            report += f"  {age_group}: {count} ({pct:.1f}%)\n"
        
        report += f"""
KEY ATTITUDES
{'─'*40}
  Willingness to change: {params['willingness_to_change']:.1%}
  Health awareness:      {params['health_awareness']:.1%}
  Price sensitivity:     {params['price_sensitivity']:.1%}

TOP BARRIERS TO HEALTHY COOKING
{'─'*40}
"""
        for i, (barrier, count) in enumerate(list(barriers.items())[:5], 1):
            report += f"  {i}. {barrier} ({count} mentions)\n"
        
        report += f"""
PREFERRED SOLUTIONS
{'─'*40}
"""
        for i, solution in enumerate(solutions, 1):
            report += f"  {i}. {solution}\n"
        
        report += f"""
CALIBRATED MODEL PARAMETERS
{'─'*40}
  Innovation coefficient (p): {params['p_calibrated']:.4f}
  Imitation coefficient (q):  {params['q_calibrated']:.4f}
  Price elasticity:           {params['price_elasticity']:.4f}

{'='*60}
"""
        return report
    
    def export_insights(self, filepath: str):
        """Export insights to JSON."""
        data = {
            "metadata": {
                "sample_size": self.n_responses,
                "region": "San Luis Potosí, Mexico"
            },
            "demographics": {
                "age_distribution": self.get_age_distribution(),
                "parent_percentage": self.get_parent_percentage()
            },
            "behaviors": {
                "fast_food_frequency": self.get_fast_food_frequency(),
                "barriers": self.get_barriers()
            },
            "model_parameters": self.calibrate_model_parameters()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("=" * 60)
    print("SURVEY ANALYSIS - Healthy Nanostore Project")
    print("=" * 60)
    
    # Get filepath from argument or use default
    filepath = sys.argv[1] if len(sys.argv) > 1 else "src/data/survey_responses.csv"
    
    try:
        analyzer = SurveyAnalyzer(filepath)
        
        # Generate and print report
        report = analyzer.generate_report()
        print(report)
        
        # Get calibrated parameters
        params = analyzer.calibrate_model_parameters()
        print("Parameters for Bass Model:")
        for key, value in params.items():
            print(f"  {key}: {value}")
        
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        print("Usage: python survey_analysis.py path/to/survey.csv")
