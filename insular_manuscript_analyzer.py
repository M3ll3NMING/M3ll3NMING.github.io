#!/usr/bin/env python3

# SCRIPT NAME: insular_manuscript_analyzer.py
# DESCRIPTION:
# This script is designed to provide an analysis of Insular manuscripts
# produced in Britain between 700 CE and 1100 CE, specifically calculating
# the percentage of such manuscripts that contain illustrations or illuminations.
#
# AUTHOR: AI Assistant
# DATE: May 9, 2025
#
# IMPORTANT DATA SOURCE NOTE:
# This script, in its current conceptual form, CANNOT directly query live, disparate
# public archives and library databases in real-time to gather the necessary data.
# Doing so accurately for the specified criteria (known extant manuscripts,
# precise production year in Britain, illustration status) is not feasible
# via a simple script due to the lack of a unified, publicly accessible,
# machine-queryable database for this specific scholarly domain.
#
# TO FUNCTION AS INTENDED (providing numbers):
# This script requires a pre-compiled, local data file (e.g., a CSV)
# meticulously created from legitimate academic sources and library catalogs.
# The specific filename 'insular_manuscripts_britain_700_1100.csv' is now hardcoded
# with an absolute path.
#
# WITHOUT THIS PRE-COMPILED FILE:
# The script can only offer guidance on where to find relevant information
# using the '--list-sources' option. It will NOT guess or estimate numbers.

import argparse
import csv
import sys
import os

# --- CONFIGURATION ---
# Hardcoded absolute path for the data file within the WSL Linux environment
DATA_FILENAME = '/home/marie/things/insular_manuscripts_britain_700_1100.csv'
MIN_YEAR = 700
MAX_YEAR = 1100

# Example CSV columns (0-based index):
# 0: Manuscript_ID
# 1: Gneuss_Lapidge_Ref
# 2: Shelfmark
# 3: Production_Century
# 4: Production_Year_Start
# 5: Production_Year_End
# 6: Production_Place_Broad (e.g., Britain)
# 7: Production_Place_Specific
# 8: Script_Style (e.g., Insular)
# 9: Contains_Illustration (TRUE/FALSE)
# 10: Illustration_Details
# 11: Holding_Institution
# 12: Digitized_Link

# Column indices (based on the example structure)
COL_YEAR_START = 4
COL_YEAR_END = 5
COL_PLACE_BROAD = 6
COL_ILLUSTRATED = 9

# --- FUNCTIONS ---

def list_data_sources():
    """Prints a list of key data sources for researching manuscripts."""
    print("---------------------------------------------------------------------------------")
    print("Primary Data Sources for Researching Insular Manuscripts (Britain, 700-1100 CE)")
    print("---------------------------------------------------------------------------------")
    print("This script CANNOT directly query these sources for a statistical summary.")
    print("You will need to consult them directly for detailed research.")
    print("")
    print("1. Foundational Bibliographical Reference (for identifying the corpus of manuscripts):")
    print("   - Gneuss, Helmut, and Michael Lapidge. 'Anglo-Saxon Manuscripts: A Bibliographical Handlist of Manuscripts and Manuscript Fragments Written or Owned in England up to 1100.' Toronto: University of Toronto Press, 2014.")
    print("     (Essential for determining the scope of known manuscripts).")
    print("")
    print("2. Major Library Catalogues & Digital Collections (for details, dating, and illustration status):")
    print("   - British Library:")
    print("     - Main Catalogue: Explore Archives and Manuscripts (search.bl.uk)")
    print("     - Digitised Manuscripts: www.bl.uk/manuscripts")
    print("     - Catalogue of Illuminated Manuscripts: www.bl.uk/catalogues/illuminatedmanuscripts")
    print("     - Polonsky Foundation Project (Medieval England and France, 700-1200): www.bl.uk/projects/france-england-medieval-manuscripts-700-1200")
    print("")
    print("   - Bodleian Libraries, University of Oxford:")
    print("     - Bodleian Archives & Manuscripts: search.bodleian.ox.ac.uk/")
    print("     - Digital Bodleian: digital.bodleian.ox.ac.uk")
    print("")
    print("   - Cambridge University Library & College Libraries:")
    print("     - Cambridge University Digital Library (CUDL): cudl.lib.cam.ac.uk")
    print("     - Parker Library on the Web (Corpus Christi College, Cambridge): parkerweb.stanford.edu")
    print("       (Many important Insular manuscripts)")
    print("")
    print("   - Digital Scriptorium (digital-scriptorium.org):")
    print("     A union catalogue of pre-modern manuscripts, primarily in North American collections, but useful for finding records and images.")
    print("")
    print("3. Specific Projects (may contain relevant datasets or links):")
    print("   - 'Insular Manuscripts: Networks of Knowledge' (Leverhulme Trust funded, involving the British Library). Check for project outputs.")
    print("     (Note: Focused on 650-850 CE, so covers the earlier part of your range).")
    print("")
    print("Methodology for manual research:")
    print("   a. Consult Gneuss & Lapidge to identify manuscripts produced in Britain within your date range.")
    print("   b. Look up these identified manuscripts in the major library catalogues (many are now digitized or have detailed online descriptions).")
    print("   c. Note the presence of illustrations/illuminations as described in the catalogue entries.")
    print("---------------------------------------------------------------------------------")

def analyze_manuscripts(year_start, year_end):
    """
    Analyzes manuscript data from the pre-compiled file for a given year range.

    Args:
        year_start (int): The start year of the analysis range.
        year_end (int): The end year of the analysis range.
    """
    print("---------------------------------------------------------------------------------")
    print(f"Analyzing Insular Manuscripts Produced in Britain: {year_start} - {year_end} CE")
    print(f"Data Source: {DATA_FILENAME} (User-provided)") # Updated message to reflect absolute path
    print("---------------------------------------------------------------------------------")
    print("IMPORTANT: The accuracy of this analysis depends entirely on the completeness and")
    print(f"accuracy of the pre-compiled data file at '{DATA_FILENAME}'.") # Updated message
    print("")

    total_manuscripts = 0
    illustrated_manuscripts = 0

    try:
        # Open the file using the absolute path
        with open(DATA_FILENAME, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Skip header row

            # Basic check for expected number of columns
            required_cols = [COL_YEAR_START, COL_YEAR_END, COL_PLACE_BROAD, COL_ILLUSTRATED]
            if len(header) <= max(required_cols):
                 print(f"Error: CSV file '{DATA_FILENAME}' does not appear to have the expected number of columns (at least {max(required_cols) + 1}).")
                 print("Please ensure it matches the expected format.")
                 return

            for i, row in enumerate(reader):
                # Ensure row has enough columns
                if len(row) <= max(required_cols):
                    # print(f"Warning: Skipping row {i+2} due to insufficient columns.") # +2 for 0-based index and header
                    continue # Skip this row

                try:
                    # Extract data, handling potential errors
                    prod_year_start_str = row[COL_YEAR_START].strip()
                    prod_year_end_str = row[COL_YEAR_END].strip()
                    prod_place_broad = row[COL_PLACE_BROAD].strip()
                    contains_illustration_str = row[COL_ILLUSTRATED].strip().lower()

                    # Skip if essential date or place data is missing
                    if not prod_year_start_str or not prod_year_end_str or not prod_place_broad:
                        # print(f"Warning: Skipping row {i+2} due to missing date or place data.")
                        continue # Skip this row if essential fields are empty

                    # Convert years to integers
                    try:
                        prod_year_start = int(prod_year_start_str)
                        prod_year_end = int(prod_year_end_str)
                    except ValueError:
                        # print(f"Warning: Skipping row {i+2} due to invalid year format: '{prod_year_start_str}-{prod_year_end_str}'.")
                        continue # Skip if years are not valid integers

                    # Apply filters: Place is Britain and date ranges overlap
                    if prod_place_broad == "Britain" and \
                       (prod_year_start <= year_end and prod_year_end >= year_start):

                        total_manuscripts += 1

                        # Check illustration status
                        if contains_illustration_str in ("true", "yes", "1"): # Allow for variations in boolean representation
                            illustrated_manuscripts += 1

                except IndexError:
                    print(f"Error: Unexpected row structure at row {i+2}. Skipping.")
                    continue # Skip row if column index is out of bounds
                except Exception as e:
                     print(f"Error processing row {i+2}: {e}. Skipping.")
                     continue # Catch any other potential errors during row processing


    except FileNotFoundError:
        print("---------------------------------------------------------------------------------")
        print(f"ERROR: Data file '{DATA_FILENAME}' not found at the specified path.")
        print("Please ensure the file exists at this exact location.")
        print("Use the '--list-sources' option for guidance on where to find manuscript data.")
        print("---------------------------------------------------------------------------------")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return


    if total_manuscripts == 0:
        print(f"No known extant manuscripts found in '{DATA_FILENAME}' matching the criteria for the period {year_start}-{year_end} CE produced in Britain.")
        print("This could mean:")
        print("   - No such manuscripts are listed in the data file for this period and location.")
        print("   - The data file is incomplete or uses different notation for origin/dates.")
        print("   - The script's internal filters for 'Britain' or date logic need adjustment for your data file.")
    else:
        percentage = (illustrated_manuscripts / total_manuscripts) * 100 if total_manuscripts > 0 else 0.0
        print(f"Total known extant manuscripts (Britain, {year_start}-{year_end} CE): {total_manuscripts}")
        print(f"Number of these containing illustrations/illuminations: {illustrated_manuscripts}")
        print(f"Percentage illustrated: {percentage:.2f}%")
    print("---------------------------------------------------------------------------------")

# --- MAIN SCRIPT LOGIC ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze Insular manuscripts produced in Britain (700-1100 CE) to calculate the percentage of illustrated manuscripts.",
        formatter_class=argparse.RawTextHelpFormatter # Preserve formatting for description/epilog
    )

    # Create mutually exclusive group for analysis options
    analysis_group = parser.add_mutually_exclusive_group()

    analysis_group.add_argument(
        "--year",
        type=int,
        help=f"Analyze manuscripts for a specific year (e.g., 850). Must be between {MIN_YEAR} and {MAX_YEAR}."
    )

    analysis_group.add_argument(
        "--year-range",
        type=str,
        metavar="YYYY-YYYY",
        help=f"Analyze manuscripts within a range of years (e.g., 700-799). Years must be between {MIN_YEAR} and {MAX_YEAR} and start year cannot be after end year."
    )

    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List key public archives, libraries, and databases for researching these manuscripts."
    )

    args = parser.parse_args()

    if args.list_sources:
        list_data_sources()
    elif args.year is not None:
        if not (MIN_YEAR <= args.year <= MAX_YEAR):
            print(f"Error: Year must be between {MIN_YEAR} and {MAX_YEAR}.", file=sys.stderr)
            sys.exit(1)
        analyze_manuscripts(args.year, args.year)
    elif args.year_range:
        try:
            start_year_str, end_year_str = args.year_range.split('-')
            start_year = int(start_year_str)
            end_year = int(end_year_str)

            if not (MIN_YEAR <= start_year <= MAX_YEAR) or not (MIN_YEAR <= end_year <= MAX_YEAR):
                 print(f"Error: Both years in the range must be between {MIN_YEAR} and {MAX_YEAR}.", file=sys.stderr)
                 sys.exit(1)
            if start_year > end_year:
                print("Error: Start year cannot be after end year in the range.", file=sys.stderr)
                sys.exit(1)

            analyze_manuscripts(start_year, end_year)

        except ValueError:
            print("Error: Year range must be in<ctrl97>YYYY-YYYY format.", file=sys.stderr)
            sys.exit(1)
    else:
        # If no specific action is requested, show usage
        parser.print_help()
        sys.exit(1)