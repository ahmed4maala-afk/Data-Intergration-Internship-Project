# Data-Intergration-Internship-Project
PRYZM Solutions Internship
# PRYZM Solutions - Data Quality Assessment & Intake Specification Proposal

## Project Overview
This repository contains the project submission for the **Data Integration & Onboarding Intern** position at PRYZM Solutions. The project addresses the critical challenge of integrating heterogeneous data from new clients by performing a comprehensive data quality assessment and proposing a robust, standardized data intake specification.

## Key Components
- **Data Quality Assessment:** In-depth analysis of the UCI Online Retail II dataset (1.07M+ records) to identify systemic data quality issues including completeness, accuracy, and consistency.
- **Intake Specification Proposal:** A detailed framework for standardized data handover, defining required fields, data types, and strict validation rules.
- **Automated Validation Framework:** Implementation of pre-ingestion checks (Null Rate Guard, Schema Enforcement) to automate manual engineering workflows.
- **Business Impact Analysis:** Quantification of financial risks associated with poor data quality, tailored for PRYZM's industrial and pharmaceutical domains.
- **GDPR & Compliance:** Integration of data privacy principles (Pseudonymization and Data Minimization) essential for handling sensitive European client data.
- **Advanced Data Architecture:** Conceptual implementation of **Human-in-the-loop** workflows and **Data Lineage** for full auditability and transparency.

## Repository Structure
- `01_analysis.py`: Python script for data processing, statistical analysis, and visualization generation.
- `02_generate_pdf.py`: Python script for dynamic generation of the professional PDF report using the `ReportLab` engine.
- `PRYZM_DataQuality_AhmedMaala.pdf`: The final 5-page comprehensive report submitted for the application.
- `outputs/`: Directory containing generated charts and statistical summaries.

## Technical Stack
- **Language:** Python 3.11
- **Libraries:** Pandas (Data Manipulation), Matplotlib/Seaborn (Visualization), ReportLab (PDF Orchestration).

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/ahmedmaala-afk/Data-Intergration-Internship-Project.git
