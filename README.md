# 🏪 Healthy Nanostore Project

<div align="center">

![MIT LiftLab](https://img.shields.io/badge/MIT-LiftLab%202025-red?style=for-the-badge)
![Tec de Monterrey](https://img.shields.io/badge/Tec%20de%20Monterrey-Campus%20SLP-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Computational Simulation of Innovation Diffusion for Healthy Products in Mexican Nanostores**

[Live Demo](https://healthy-nanostore.github.io) · [Documentation](./docs) · [ML Models](./src/ml)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The Problem](#-the-problem)
- [Our Solution](#-our-solution)
- [Innovation Diffusion Model](#-innovation-diffusion-model)
- [Machine Learning Models](#-machine-learning-models)
- [Data Sources](#-data-sources)
- [Installation](#-installation)
- [Team](#-team)

---

## 🎯 Overview

Mexico faces a public health crisis with **18% diabetes prevalence** and **70% overweight/obesity** rates among adults. Meanwhile, **1.1 million nanostores (tienditas)** serve as the primary food access point for vulnerable communities, accounting for **31% of the food retail market**.

This project simulates the **diffusion of healthy product innovations** through nanostore networks using Agent-Based Modeling (ABM) and the Bass Diffusion Model, providing evidence-based projections for public health policy interventions.

### 🏆 MIT LiftLab National Competition 2025
> Campus Winner - Tecnológico de Monterrey, San Luis Potosí

---

## 🚨 The Problem

### Health Crisis in Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Diabetes Prevalence | 18% | ENSANUT 2023 |
| Overweight/Obesity | 70% | ENSANUT 2023 |
| Diabetes Deaths (2020) | 148,437 | SINAVE |
| Daily F&V Consumption | 2.1 portions | ENSANUT 2023 |
| Recommended F&V | 5 portions | WHO |

### Nanostore Ecosystem

| Metric | Value | Source |
|--------|-------|--------|
| Total Nanostores | 1,100,824 | DENUE 2024 |
| Market Share | 31% | Data México |
| Informal Credit ("Fiado") | 16% | IDB |
| States Covered | 32 | National |

---

## 💡 Our Solution

### Innovation Diffusion Simulation

We simulate how healthy products spread through nanostore networks using:

1. **Bass Diffusion Model** - Mathematical framework for innovation adoption
2. **Agent-Based Modeling** - Individual consumer and store behavior simulation
3. **Network Effects** - Social influence on purchasing decisions
4. **Geospatial Analysis** - DENUE data integration for realistic store distribution

---

## 📊 Innovation Diffusion Model

### Theoretical Framework

Based on Rogers' Diffusion of Innovations (1962) and Bass Model (1969), adapted for Mexican nanostore context.

### Mathematical Model

```
Adoption Rate = p(M - N) + q(N/M)(M - N)

Where:
  p = 0.03   # Innovation coefficient (external influence)
  q = 0.38   # Imitation coefficient (social influence)
  M = 1,100,824  # Market potential (total nanostores)
  N = Current adopters
```

### Key Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **p (Innovation)** | 0.03 | 3% adopt from external influence (ads, promoters) |
| **q (Imitation)** | 0.38 | 38% adopt from social influence (neighbors, family) |
| **Price Elasticity** | -0.59 | 10% price reduction → 5.9% more purchases |

### Adopter Categories (Rogers)

| Type | % of Population | Characteristics |
|------|-----------------|-----------------|
| Innovators | 2.5% | Health-conscious, low price sensitivity |
| Early Adopters | 13.5% | Opinion leaders, moderate social influence |
| Early Majority | 34% | Pragmatic, wait for social proof |
| Late Majority | 34% | Skeptical, high price sensitivity |
| Laggards | 16% | Traditional, resist change |

### Expected Outcomes

| Scenario | Time to 16% | Time to 50% | 10-Year Adoption |
|----------|-------------|-------------|------------------|
| Baseline | 4.2 years | 7.1 years | 68% |
| Health Promoters (+100% p) | 2.8 years | 5.9 years | 79% |
| Social Campaign (+32% q) | 3.1 years | 5.4 years | 82% |
| Combined | 2.1 years | 4.2 years | 91% |

---

## 🤖 Machine Learning Models

### Model Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      ML PIPELINE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │  DENUE  │───▶│ Feature │───▶│  Bass   │───▶│ Health  │      │
│  │  Data   │    │Engineer │    │  Model  │    │ Impact  │      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │              │              │              │            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐      │
│  │ ENSANUT │───▶│  ABM    │───▶│Adoption │───▶│Diabetes │      │
│  │  Data   │    │ Agents  │    │ Curves  │    │Reduction│      │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘      │
│       │                                                         │
│  ┌─────────┐                                                    │
│  │ Survey  │───▶ Parameter Calibration                         │
│  │  Data   │    (104 responses)                                │
│  └─────────┘                                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Models Included

| Model | File | Purpose |
|-------|------|---------|
| Bass Diffusion | `bass_diffusion.py` | Innovation adoption curves |
| Consumer ABM | `consumer_abm.py` | Agent-based consumer behavior |
| Survey Analysis | `survey_analysis.py` | Primary data processing |

---

## 📁 Data Sources

### Official Mexican Datasets

| Dataset | Source | Records | Usage |
|---------|--------|---------|-------|
| **DENUE 2024** | INEGI | 1,100,824 nanostores | Store locations, density |
| **ENSANUT 2023** | INSP | National | Health prevalence, consumption |
| **ENIGH 2022** | INEGI | National | Spending patterns by income |
| **CONAPO 2020** | CONAPO | Municipal | Marginalization index |

### Primary Data

| Dataset | Source | Records | Usage |
|---------|--------|---------|-------|
| **Eating Habits Survey** | Team collected | 104 responses | Behavior parameter calibration |

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Git

### Quick Start

```bash
# Clone repository
git clone https://github.com/healthy-nanostore/mit-liftlab-2025.git
cd healthy-nanostore-mit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Bass Diffusion simulation
python src/ml/bass_diffusion.py

# Analyze survey data
python src/ml/survey_analysis.py src/data/survey_responses.csv

# Run Agent-Based Model
python src/ml/consumer_abm.py
```

---

## 📂 Project Structure

```
healthy-nanostore-mit/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── docs/
│   └── methodology.md
└── src/
    ├── ml/
    │   ├── bass_diffusion.py
    │   ├── consumer_abm.py
    │   └── survey_analysis.py
    └── data/
        └── survey_responses.csv
```

---

## 👥 Team

<table>
<tr>
<td align="center">
<b>Fernanda Ita</b><br>
<sub>Deep Research</sub><br>
<sub>Applied Research · Critical Analysis</sub>
</td>
<td align="center">
<b>Alexis Marcos</b><br>
<sub>Data Collection</sub><br>
<sub>Survey Design · Field Work</sub>
</td>
<td align="center">
<b>Carlos Torres</b><br>
<sub>Data Scientist</sub><br>
<sub>Machine Learning · Full Stack</sub>
</td>
</tr>
</table>

**Institution**: Tecnológico de Monterrey, Campus San Luis Potosí

**Program**: Mechatronics Engineering

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FEMSA** - Competition sponsor
- **INEGI** - DENUE open data
- **INSP** - ENSANUT data

---

<div align="center">

**Made with ❤️ for Mexican communities**

MIT LiftLab National Competition 2025

</div>
