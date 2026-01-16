# Methodology

## Innovation Diffusion Model for Mexican Nanostores

### 1. Theoretical Framework

Our simulation is based on the **Bass Diffusion Model** (1969), which describes how new products get adopted through two mechanisms:

- **External Influence (p)**: Adoption from marketing, health promoters, media
- **Internal Influence (q)**: Adoption from social influence, word-of-mouth

### 2. Mathematical Model

```
dN/dt = (p + q * N/M) * (M - N)

Where:
  N(t) = cumulative adopters at time t
  M = market potential (1,100,824 nanostores)
  p = 0.03 (innovation coefficient)
  q = 0.38 (imitation coefficient)
```

### 3. Parameter Calibration

| Parameter | Value | Source |
|-----------|-------|--------|
| p | 0.03 | Health innovation literature |
| q | 0.38 | Emerging market studies, survey data |
| M | 1,100,824 | INEGI DENUE 2024 |
| Elasticity | -0.59 | F&V price elasticity meta-analysis |

### 4. Adopter Categories (Rogers, 1962)

| Type | % | Characteristics |
|------|---|-----------------|
| Innovators | 2.5% | High health awareness, low price sensitivity |
| Early Adopters | 13.5% | Opinion leaders |
| Early Majority | 34% | Wait for social proof |
| Late Majority | 34% | High price sensitivity |
| Laggards | 16% | Resist change |

### 5. Data Sources

| Dataset | Source | Usage |
|---------|--------|-------|
| DENUE 2024 | INEGI | Nanostore locations |
| ENSANUT 2023 | INSP | Health prevalence |
| Primary Survey | Team | 104 responses, behavior calibration |

### 6. Health Impact

Based on meta-analysis:
- 100g/day F&V increase → 6% diabetes risk reduction
- Price elasticity -0.59 → 10% subsidy = 5.9% more consumption

### 7. Limitations

- DENUE may underrepresent informal tienditas
- Parameters assumed stationary over time
- Geographic heterogeneity not fully captured
