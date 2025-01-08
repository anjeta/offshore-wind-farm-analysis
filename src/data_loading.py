# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

import pandas as pd

from messages import invalid_input_message, load_file_message

# =============================================================================
# Data Loading
# =============================================================================
def load_file():
    file_path = input(load_file_message())
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
            print("\nCSV file loaded successfully.\nContent:")
            data.info()
        elif file_path.endswith('.txt'):
            data = pd.read_csv(file_path)
            print("\nText file loaded successfully.\nContent:")
            data.info()
        else:
            print("\nUnsupported file format. Please load a .txt or .csv file.")
            data = None
    except FileNotFoundError:
        print("\nFile not found. Please check the path and try again.")
        data = None
    except pd.errors.EmptyDataError:
        print("\nThe file is empty. Please provide a valid file.")
        data = None
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        data = None
    return data

# =============================================================================
# Data Updating
# =============================================================================
def update_data(data):
    while(True):
        print("1. Load New Data")
        print("2. Update Existing Data")
        print("3. Back to Main Menu")
        sub_choice = input("Select an option (1-3): ")
        
        if sub_choice == "1":
            updated_data = load_file()
            return updated_data
        if sub_choice == "2":
            update = load_file()
            try:
                updated_data = pd.concat([data, update], ignore_index=True, sort=False)
                return updated_data
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                return data
        elif sub_choice == "3":
            return data
        else:
            print(invalid_input_message())