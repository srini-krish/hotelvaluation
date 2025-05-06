# Hotel Valuation Platform

## Overview
This repository contains a hotel valuation platform prototype designed for small and boutique hotels (2-100 rooms). The application provides multiple valuation methods, sensitivity analysis, and an intuitive interface for hotel owners and investors.

## Features
- Income Approach (NOI-based Cap Rate) valuation
- ADR Multiplier Model valuation
- Cash-on-Cash return calculations
- Interactive sensitivity analysis
- Downloadable reports
- Responsive web interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Clone this repository
   ```bash
   git clone https://github.com/pragnakalpdev28/hotel_valuation_demo_app.git
   cd hotel_valuation_demo_app
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Streamlit application
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in your terminal (typically http://localhost:8501)

## Using the Application

### Base Assumptions
The application comes pre-loaded with data for the Maple Grove Inn. You can adjust these values using the sidebar controls:

- Hotel name and location
- Room count
- Average Daily Rate (ADR)
- Occupancy rate
- Annual revenue and expenses
- Cap rate
- ADR multiplier
- Equity investment

### Valuation Results
The main dashboard displays key valuation metrics:
- Net Operating Income (NOI)
- Income Approach Value
- ADR Multiplier Value
- Cash-on-Cash returns

### Sensitivity Analysis
Expand the "Sensitivity Analysis" section to:
1. Adjust ranges for ADR, occupancy, and cap rate
2. View calculated valuations across all combinations
3. Download the complete sensitivity analysis as a CSV file
