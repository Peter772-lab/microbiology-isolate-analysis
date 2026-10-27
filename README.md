# Microbiology Isolate Analysis

## Project Overview
This project uses Python to analyze bacterial isolate data and antimicrobial susceptibility test results. It was developed as a beginner programming project to apply Python to practical microbiology data analysis.

## Objectives
- Organize bacterial isolate data.
- Calculate mean zones of inhibition from replicate measurements.
- Validate replicate data and identify missing or invalid values.
- Classify results using predefined exercise thresholds.
- Summarize results by Gram-stain group.
- Export processed results to CSV.
- Visualize mean zones of inhibition using a bar chart.

## Technologies Used
- Python
- Matplotlib
- CSV file handling
- Basic data validation and statistical calculations

## Input Data
The example dataset contains five bacterial isolates, their Gram-stain classifications, and three replicate zone-of-inhibition measurements per isolate.

## Outputs
Running the script generates:
- `isolate_analysis_results.csv` — processed isolate data and analysis results.
- `mean_zone_by_isolate.png` — a bar chart comparing mean zones of inhibition.

## How to Run

1. Install Python 3.
2. Install Matplotlib:

   ```bash
   python -m pip install matplotlib
   ```

3. Place `learn.py` and `isolates2.csv` in the same folder.
4. Open a terminal in that folder and run:

   ```bash
   python learn.py
   ```

## Important Scientific Note
The susceptibility thresholds used in this project are simplified rules for programming practice. They are not validated clinical breakpoints and must not be used to guide patient treatment. Clinical interpretation requires the relevant organism, antimicrobial agent, testing method, and current CLSI or EUCAST standards.

## Learning Goals
This project demonstrates foundational Python skills, including lists, dictionaries, loops, functions, conditional statements, file handling, data validation, calculations, CSV export, and plotting.

## Project Status
Beginner learning project — functionality may be extended as Python and microbiology data-analysis skills develop.
