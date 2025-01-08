# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

import pandas as pd
import sys

from data_loading import load_file
from messages import invalid_input_message, select_data_message 
from messages import criteria_selection_message, cost_benefit_message
from messages import restrictions_message, constraints_message
from messages import select_stakeholders_message, factor_selection_message
from messages import area_selection_message

# =============================================================================
# Data Selection
# =============================================================================
def select_data(data):
    print(select_data_message())
    
    default_criteria = list(data.columns)
    criteria, types = select_criteria(default_criteria, True)
    selected_data = None
    if criteria is not None:
        selected_data = data[criteria].astype(float)    # Converting all Boolean columns to number columns
        constraints = select_constraints(criteria)
        constrained_data = pd.DataFrame()
        if constraints is not None and not constraints.empty:
            constraints_criteria = list(constraints["criteria"])
            lowcut_restrictions = list(constraints["restrict_values_lower_than"])
            highcut_restrictions = list(constraints["restrict_values_greater_than"])
            for i in range(len(constraints)):
                if lowcut_restrictions[i] is None:
                    lowcut_restrictions[i] = sys.float_info.min
                if highcut_restrictions[i] is None:
                    highcut_restrictions[i] = sys.float_info.max
                if type(lowcut_restrictions[i]) == str or type(highcut_restrictions[i]) == str:
                    print(f"\nConstraints for criteria {constraints_criteria[i]} are not valid. Warning: ignoring constraints for criteria {constraints_criteria[i]}.")
                    continue
                if highcut_restrictions[i] < lowcut_restrictions[i]:
                    print(f"\nConstraints for criteria {constraints_criteria[i]} are not valid. Warning: ignoring constraints for criteria {constraints_criteria[i]}.")
                    continue
                constrained_data = selected_data[(selected_data[constraints_criteria[i]] >= lowcut_restrictions[i]) & (selected_data[constraints_criteria[i]] <= highcut_restrictions[i])]
                while(True):
                    response = input("Do you want to completely remove constricted criteria from the analysis? (YES/NO) ")
                    if response == "YES" or response == "Y" or response == "Yes" or response == "yes" or response == "y":
                        if constraints_criteria[i] in criteria:
                            constraint_idx = criteria.index(constraints_criteria[i])
                            criteria.remove(constraints_criteria[i])
                            types.pop(constraint_idx)
                            constrained_data = constrained_data.drop(columns=constraints_criteria[i])
                        break
                    elif response == "NO" or response == "N" or response == "No" or response == "no" or response == "n":
                        if constraints_criteria[i] in criteria:
                            constraint_idx = criteria.index(constraints_criteria[i])
                            constraints_content = constrained_data[constraints_criteria[i]].to_numpy()
                            if (constraints_content[0] == constraints_content).all():
                                criteria.remove(constraints_criteria[i])
                                types.pop(constraint_idx)
                                constrained_data = constrained_data.drop(columns=constraints_criteria[i])
                        break
                    else:
                        print(invalid_input_message())                
        if not constraints.empty:
            selected_data = constrained_data
        if constrained_data.empty and not constraints.empty:
            print("\nConstraints result in no data selection. Warning: ignoring constraints completely.")        
        return selected_data, criteria, types
    else:
        return None, None, None

# =============================================================================
# Criteria Selection
# =============================================================================
def select_criteria(default_criteria, return_types):
    if return_types:
        print(criteria_selection_message())
    else:
        print(factor_selection_message())
    
    if "community_name" in default_criteria:
        default_criteria.remove("community_name")
    while(True):
        print("1. Input Prefered Criteria")
        print("2. Load Criteria File")
        print("3. Default: Consider All Criteria")
        print("4. Back to Main Menu")
        sub_choice = input("Select an option (1-4): ")
        
        if sub_choice == "1":
            print(f"Available criteria are: {default_criteria}")
            
            criteria_selection = input("Type selected criteria here: ")
            try:
                criteria_selection = criteria_selection.split(",")
                for i, criterion in enumerate(criteria_selection):
                    criterion = criterion.strip()
                    if criterion not in default_criteria:
                        print(f"\nCriterion \"{criterion}\" not found in the data. Please check the available criteria and try again.\n")
                        criteria_selection = None
                        break
                    else:
                        criteria_selection[i] = criterion 
                if criteria_selection is not None:
                    print(f"\nCriteria selected sucessfully.\nContent: {criteria_selection}")
                    if return_types:
                        types = cost_benefit_analysis(criteria_selection)
                        return criteria_selection, types
                    else:
                        return criteria_selection
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please check the available criteria and try again.")
                continue
        
        elif sub_choice == "2":
            loaded_criteria = load_file()
            if loaded_criteria is not None:
                try:
                    criteria_selection = list(loaded_criteria["criteria"])
                    types = list(loaded_criteria["type"])
                    for i, criterion in enumerate(criteria_selection):
                        if criterion not in default_criteria:
                            print(f"Criterion \"{criterion}\" not found in the data. Removing \"{criterion}\" from the selection.")
                            criteria_selection[i] = None
                            types[i] = None
                    criteria_selection = [criterion for criterion in criteria_selection if criterion is not None]
                    types = [typ for typ in types if typ is not None]
                    if return_types:
                        print("\nCriteria selected sucessfully.")
                        return criteria_selection, types
                    else:
                        print("\nCriteria selected sucessfully.")
                        return criteria_selection
                except Exception as e:
                    print(f"\nAn error occurred: {str(e)}")
                    print("Please check the loaded file and try again.")
                    continue
            else:
                continue
        
        elif sub_choice == "3" or sub_choice == "":
            criteria_selection = default_criteria
            print(f"\nCriteria selected sucessfully.\nContent: {criteria_selection}")
            if return_types:
                types = cost_benefit_analysis(criteria_selection)
                return criteria_selection, types
            else:
                return criteria_selection
        
        elif sub_choice == "4":
            if return_types:
                return None, None
            else:
                return None
        
        else:
            print(invalid_input_message())


def cost_benefit_analysis(criteria):
    print(cost_benefit_message())
    
    types = []
    i = 0
    while i < len(criteria):
        criterion = criteria[i]
        criteria_type = input(f"Is criteria \"{criterion}\" a benefit (1) or a cost (-1)? ")
        if criteria_type == "1":
            types.append("max")
            i += 1
        elif criteria_type == "-1":
            types.append("min")
            i += 1
        else:
            print("Invalid input. Please try again.")
    return types


# =============================================================================
# Constraints Selection
# =============================================================================
def select_constraints(criteria):
    print(constraints_message())
    
    while(True):
        print("1. Input Constrained Criteria")
        print("2. Load Constraints File")
        print("3. Default: Consider No Constraints")
        print("4. Back to Main Menu")
        sub_choice = input("Select an option (1-4): ")
        
        if sub_choice == "1":            
            print(f"Available criteria are: {criteria}")
            
            criteria_selection = input("Type selected criteria here: ")
            try:
                criteria_selection = criteria_selection.split(",")
                for i, criterion in enumerate(criteria_selection):
                    criterion = criterion.strip()
                    if criterion not in criteria:
                        print("\nCriterion not found. Please check the available criteria and try again.")
                        continue
                    else:
                        criteria_selection[i] = criterion                       
                restrictions = define_restrictions(criteria_selection)
                constraints = pd.DataFrame({"criteria": criteria_selection, "restrict_values_lower_than": [value_range[0] for value_range in restrictions.values()], "restrict_values_greater_than": [value_range[1] for value_range in restrictions.values()]})
                print(f"\nConstraints for criteria {criteria_selection} defined sucessfully.")
                return constraints
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please check the available criteria and try again.")
                continue
            
        elif sub_choice == "2":
            constraints = load_file()
            if constraints is not None:
                print(f"\nConstraints for criteria {list(constraints['criteria'])} selected sucessfully.")
                return constraints
            else:
                continue
            
        elif sub_choice == "3" or sub_choice == "":
            print("\nNo constraints will be considered.")
            return pd.DataFrame()
        
        elif sub_choice == "4":
            return None


def define_restrictions(criteria):
    print(restrictions_message())
    
    restrictions = dict.fromkeys(criteria)
    i = 0
    while i < len(criteria):
        criterion = criteria[i]
        if restrictions[criterion] is None:
            lowcut = input(f"Threshold value for criteria \"{criterion}\" below which the data is NOT considered valid: ")
            if not lowcut.isnumeric():
                if lowcut == "":
                    lowcut = None
                else:
                    print("\nInvalid input. Please try again.\n")
                    continue
            if lowcut is not None:
                lowcut = float(lowcut)
            restrictions[criterion] = [lowcut]
        if restrictions[criterion] is not None:
            highcut = input(f"Threshold value for criteria \"{criterion}\" above which the data is NOT considered valid: ")
            if not highcut.isnumeric():
                if highcut == "":
                    highcut = None
                else:
                    print("\nInvalid input. Please try again.\n")
                    continue
            if highcut is not None:
                highcut = float(highcut)
                if highcut < lowcut:
                    print("\nInvalid input. Please try again.\n")
                    continue
            restrictions[criterion].append(highcut)
            i += 1
            
    return restrictions     


# =============================================================================
# Stakeholder Selection
# ============================================================================= 
def select_stakeholders(stakeholder_groups):
    print(select_stakeholders_message())
    print(f"Avaliable stakeholder groups are: {list(stakeholder_groups.keys())}")
    
    stakeholder_selection = input("Type selected stakerholder groups here: ")
    try:
        if stakeholder_selection == "":
            stakeholder_selection = stakeholder_groups
        else:
            stakeholder_selection = stakeholder_selection.split(",")
            for i, stakeholder in enumerate(stakeholder_selection):
                stakeholder = stakeholder.strip()
                if stakeholder not in list(stakeholder_groups.keys()):
                    print(f"\nStakeholder group {stakeholder} not found. Please check the available stakeholder groups and try again.\n")
                    return None
                else:
                    stakeholder_selection[i] = stakeholder
        print(f"\nStakeholder groups selected sucessfully.\nContent: {stakeholder_selection}")
        return stakeholder_selection
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return None
 
# =============================================================================
# Area Selection
# =============================================================================
def select_areas(areas):
    print(area_selection_message())
    print(f"Available areas are: {areas}")
    area_selection = input("Type selected areas here: ")
    try:
        if area_selection == "":
            area_selection = areas
        else:
            area_selection = area_selection.split(",")
            for i, area in enumerate(area_selection):
                area = area.strip()
                if area not in areas:
                    print(f"\nArea {area} not found. Please check the available areas and try again.")
                    return None
                else:
                    area_selection[i] = area
        print(f"\nAreas selected sucessfully.\nContent: {area_selection}")
        return area_selection
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return None