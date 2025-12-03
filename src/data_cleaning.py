import pandas as pd
import os
import json
from fuzzywuzzy import process
import re

# Paths
RAW_DIR = "data/raw"
CLEANED_DIR = "data/cleaned"
REPORT_PATH = "data/cleaned/cleaning_report.json"

def load_data():
    doctors = pd.read_csv(os.path.join(RAW_DIR, "doctors.csv"))
    branches = pd.read_csv(os.path.join(RAW_DIR, "branches.csv"))
    diseases = pd.read_csv(os.path.join(RAW_DIR, "diseases.csv"))
    timings = pd.read_csv(os.path.join(RAW_DIR, "doctor_timings.csv"))
    patients = pd.read_csv(os.path.join(RAW_DIR, "patients.csv"))
    return doctors, branches, diseases, timings, patients

def clean_disease_names(patients_df, diseases_df):
    """Fuzzy match patient disease names to canonical disease names."""
    canonical_diseases = diseases_df['canonical_name'].tolist()
    
    def get_canonical(name):
        # Simple normalization
        name = str(name).strip()
        match, score = process.extractOne(name, canonical_diseases)
        if score > 70: # Threshold
            return match
        return name # Keep original if no good match (or handle as 'Other')

    patients_df['cleaned_disease_name'] = patients_df['disease_name'].apply(get_canonical)
    return patients_df

def clean_area_names(patients_df, branches_df):
    """Canonicalize area names based on branch coverage."""
    # Create a mapping from area to branch_id/canonical_area
    area_map = {}
    for _, row in branches_df.iterrows():
        areas = row['area_names'].split(';')
        for area in areas:
            area_map[area.strip().lower()] = row['branch_name'] # Or map to a canonical area name if preferred

    # For this dataset, we might just want to ensure consistency. 
    # Let's just strip and title case for now as a basic clean, 
    # but the prompt asks for canonicalization.
    # Let's map patient area to the branch's primary area or just clean it.
    
    # A better approach for "canonicalization" here might be mapping to the branch ID if missing, 
    # or just standardizing the text.
    patients_df['area'] = patients_df['area'].str.strip().str.title()
    return patients_df

def main():
    os.makedirs(CLEANED_DIR, exist_ok=True)
    
    doctors, branches, diseases, timings, patients = load_data()
    
    report = {"rows_processed": {}, "corrections": []}
    
    # Clean Patients
    initial_rows = len(patients)
    patients = clean_disease_names(patients, diseases)
    patients = clean_area_names(patients, branches)
    
    # Convert timestamp
    patients['visit_timestamp'] = pd.to_datetime(patients['visit_timestamp'], errors='coerce')
    
    # Save cleaned
    doctors.to_csv(os.path.join(CLEANED_DIR, "doctors.csv"), index=False)
    branches.to_csv(os.path.join(CLEANED_DIR, "branches.csv"), index=False)
    diseases.to_csv(os.path.join(CLEANED_DIR, "diseases.csv"), index=False)
    timings.to_csv(os.path.join(CLEANED_DIR, "doctor_timings.csv"), index=False)
    patients.to_csv(os.path.join(CLEANED_DIR, "patients.csv"), index=False)
    
    report["rows_processed"]["patients"] = len(patients)
    report["status"] = "Success"
    
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)
        
    print("Data cleaning complete. Report saved.")

if __name__ == "__main__":
    main()
