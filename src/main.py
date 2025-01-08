# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

import numpy as np
import os
import time

from data_loading import load_file, update_data
from data_selection import select_data, select_criteria, select_areas
from decision_making import AHP, fuzzy_AHP, TOPSIS, fuzzy_TOPSIS, compare_locations
from messages import info_message, invalid_input_message
from messages import weighting_message, ranking_message, ranking_option_message
from messages import evaluation_message, sensitivity_option_message, sensitivity_message
from simulations import simulate_data, sensitivity_analysis

  
# =============================================================================
# 0. Information
# =============================================================================
def option_zero():
    print("\n-------------------------------------------------------")
    print("Information")
    print("-------------------------------------------------------")
    print(info_message())

# =============================================================================
# 1. Data Loading
# =============================================================================
def option_one():
    print("\n-------------------------------------------------------")
    print("Load Data")
    print("-------------------------------------------------------")
    file_loaded = False
    data = load_file()
    if data is not None:
        file_loaded = True
    return file_loaded, data

# =============================================================================
# 2. Data Updating
# =============================================================================
def option_two(data):
    print("\n-------------------------------------------------------")
    print("Update Data")
    print("-------------------------------------------------------")
    file_loaded = False
    updated_data = update_data(data)
    if updated_data is not None:
        file_loaded = True
    return file_loaded, data

# =============================================================================
# 3. Scenario Analysis
# =============================================================================
def option_three(data):
    print("\n-------------------------------------------------------")
    print("Scenario Analysis")
    print("-------------------------------------------------------")
    result = evaluate_locations(data)
    return result

def evaluate_locations(data):
    print(evaluation_message())
    areas = list(data.sort_values("community_name")["community_name"].unique())
    area_selection = select_areas(areas)
    if area_selection is None:
        print("\nScenario analysis was unsuccessful.")
        return None
    default_criteria = list(data.columns)
    criteria_selection = select_criteria(default_criteria, False)
    if criteria_selection is None:
        print("\nScenario analysis was unsuccessful.")
        return None
    selected_data = data.copy()
    selected_data = selected_data[selected_data["community_name"].isin(area_selection)]
    selected_data = selected_data[criteria_selection].astype(float)
    result = compare_locations(data, selected_data, criteria_selection)
    result["distance_from_offshore_wind_farm"] = data.loc[result.index]["distance_from_offshore_wind_farm"]
    result["community_name"] = data.loc[result.index]["community_name"]
    return result

# =============================================================================
# 4. Defining Priorities and Constraints
# =============================================================================
def option_four(data):
    print("\n-------------------------------------------------------")
    print("Define Priorities and Constraints")
    print("-------------------------------------------------------")
    constraints_selected = False
    selected_data, criteria, types = select_data(data)
    if selected_data is not None:
        constraints_selected = True
        return constraints_selected, selected_data, criteria, types
    else:
        return constraints_selected, None, None, None

# =============================================================================
# 5. Ranking
# =============================================================================
def option_five(data, selected_data, criteria, types):
    print("\n-------------------------------------------------------")
    print("Rank Alternative Locations")
    print("-------------------------------------------------------")
    print(ranking_option_message())
    ranking = get_ranking(selected_data, criteria, types)
    if ranking is not None:
        result = selected_data.copy()
        result["Ranking"] = ranking
        result.sort_values("Ranking", ascending=False, inplace=True)
        result["community_name"] = data.loc[result.index]["community_name"]
        print(f"Best ranked alternative is:\n{result.iloc[0]}")
        return result
    else:
        return None
    
def get_ranking(data, criteria, types):
    
    print(weighting_message())
    while(True):
        print("1. Use Equal Weights")
        if len(criteria) > 1:
            print("2. Load Evaluation Data for Weight Calculation")
            print("3. Use Simulated Data for Weight Calculation")
        print("4. Back to Main Menu")
        sub_choice = input("Select an option (1-4): ")
        
        simulated_weights = False
        uncertain_decision_making = False
        
        if sub_choice == "1":
            PCM_list, DM_list = None, None
            weights = np.zeros(len(criteria)) + (1. / len(criteria))
            break
        
        elif sub_choice == "2" and len(criteria) > 1:
            print("\nPlease note that this option is currently unavailable and select another option.\n")
            
        elif sub_choice == "3" and len(criteria) > 1:
            simulated_weights = True
            PCM_list, DM_list = simulate_data(data)
            if PCM_list is None and DM_list is None:
                return None
            response = input("Do you want to simulate uncertain stakeholder decision making? (YES/NO)")
            if response == "YES" or response == "Y" or response == "Yes" or response == "yes" or response == "y":
                uncertain_decision_making = True
                weights, fuzzy_weights_list = fuzzy_AHP(PCM_list)
                if weights is None:
                    print("\nUnable to simulate decision making.")
                    return None
                break
            elif response == "NO" or response == "N" or response == "No" or response == "no" or response == "n":
                weights = AHP(PCM_list)
                break
            else:
                print(invalid_input_message())
                
        elif sub_choice == "4":
            return None
        else:
            print(invalid_input_message())
    
    
    print(ranking_message())
    while(True):
        print("1. TOPSIS ranking")
        if simulated_weights and uncertain_decision_making:
            print("2. Fuzzy TOPSIS ranking")
        print("3. Back to Main Menu")
        sub_choice = input("Select an option (1-3): ")
        
        if sub_choice == "1":
            try:
                ranking = TOPSIS(data, weights, types)
                print("\nRanking of alternative locations completed sucessfully.")
                return ranking
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                return None
            
        elif sub_choice == "2" and simulated_weights and uncertain_decision_making:
            try:
                ranking = fuzzy_TOPSIS(fuzzy_weights_list, DM_list, types)
                print("\nRanking of alternative locations completed sucessfully.")
                return ranking
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                return None
            return ranking
        
        elif sub_choice == "3":
            return None
        else:
            print(invalid_input_message())

# =============================================================================
# 6. Sensitivity Analysis
# =============================================================================    
def option_six(data, selected_data, criteria, types, ranking):
    print("\n-------------------------------------------------------")
    print("Sensitivity Analysis")
    print("-------------------------------------------------------")
    print(sensitivity_option_message())
    print(sensitivity_message())
    rank_selection = input("Offshore wind farm location rank: ")
    alternative_num = len(ranking)
    if not rank_selection.isnumeric() and int(rank_selection) not in range(alternative_num):
        print("\nSensitivity analysis was unsuccessful.")
        return None
    rank_selection = int(rank_selection)
    if rank_selection > alternative_num:
        print("\nSensitivity analysis was unsuccessful.")
        return None
    selection_index = ranking.index[rank_selection-1]
    print(f"You have selected the following offshore wind farm location for sensitivity analysis:\n{data.loc[selection_index]}")
    sensitivity = sensitivity_analysis(data, selected_data, criteria, types, selection_index)
    print("\nSensitivity analysis successful.")
    return sensitivity

# =============================================================================
# 7. Exit
# =============================================================================    
def option_seven():
    print("\n-------------------------------------------------------")
    print("Exit")
    print("-------------------------------------------------------")
    print("Exiting Offshore Wind Farm Assessment. See you next time!\n\n")

# =============================================================================
# Main console UI
# =============================================================================
def console_ui():
    
    file_loaded = False
    constraints_selected = False
    alternatives_ranked = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========================================================")
    print("  Welcome to the Offshore Wind Farm Location Evaluator  ")
    print("========================================================")
    
    while(True):
        print("\n")
        print("0. Information")
        print("1. Load Data")
        if file_loaded:
            print("2. Update Data")
            print("3. Scenario Analysis")
            print("4. Define Priorities and Constraints")
        if file_loaded and constraints_selected:
            print("5. Rank Alternative Locations")
        if file_loaded and constraints_selected and alternatives_ranked:
            print("6. Sensitivity Analysis")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ")
        
        if choice == "0":
            option_zero()
            
        elif choice == "1":
            file_loaded, data = option_one()
            alternatives_ranked = False
            
        elif choice in ["2", "3", "4", "5"] and not file_loaded:
            print("Please load a file first (Option 1).")
        
        elif choice == "2" and file_loaded:
            file_loaded, data = option_two(data)
            alternatives_ranked = False
            
        elif choice == "3" and file_loaded:
            location_assessment = option_three(data)
            if location_assessment is not None:
                location_assessment.to_csv(f"scenario_analysis_{time.strftime('%Y%m%d-%H%M%S')}.csv", index=False)  
                print("Scenario analysis results saved to a file.")
                
        elif choice == "4" and file_loaded:
            constraints_selected, selected_data, criteria, types = option_four(data)
            
        elif choice == "5" and file_loaded and constraints_selected:
            ranking = option_five(data, selected_data, criteria, types)
            if ranking is not None:
                alternatives_ranked = True
                ranking.to_csv(f"ranking_{time.strftime('%Y%m%d-%H%M%S')}.csv", index=False)  
                print("Ranking results saved to a file.")
            
        elif choice == "6" and file_loaded and constraints_selected and alternatives_ranked:
            sensitivity = option_six(data, selected_data, criteria, types, ranking)
            if sensitivity is not None:
                sensitivity.to_csv(f"sensitivity_{time.strftime('%Y%m%d-%H%M%S')}.csv", index=False)  
                print("Sensitivity analysis results saved to a file.")
        
        elif choice == "7":
            option_seven()
            break
        else:
            print(invalid_input_message())
        
        input("\nPress Enter to continue ")

if __name__ == "__main__":
    console_ui()
