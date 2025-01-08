# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from data_selection import select_criteria, select_stakeholders
from decision_making import PCM, DM, TOPSIS
from messages import invalid_input_message, simulate_data_message

# =============================================================================
# Simulating Decision Making 
# =============================================================================
def simulate_decision_making(data, stakeholder_groups, criteria):
    
    criteria_num = len(criteria)    
    evaluated_data = evaluate_dataset(data)

    # Simulate decision makings for a selected number of stakeholders from different
    # stakeholder groups
    num_stakeholders_per_group = 5
    PCM_list = []
    DM_list = []

    for stakeholder, preferable_criteria in stakeholder_groups.items():
        preferable_criteria_range = [index for index, element in enumerate(criteria) if element in preferable_criteria]
        for p in range(num_stakeholders_per_group):
            PCM_list.append(PCM(criteria_num, preferable_criteria_range))
            DM_list.append(DM(evaluated_data, preferable_criteria_range))
    
    return PCM_list, DM_list

# =============================================================================
# Simulating Stakeholder Evaluation
# =============================================================================
def simulate_data(data):
    print(simulate_data_message())
    default_stakeholder_groups = {"socio-economic": ["average_income", "fishing_dependency", "unemployment_rate", "tourism_revenue"],
                          "fisheries": ["fish_stock_health", "potential_habitat_restoration"],
                          "environmental": ["marine_biodiversity", "carbon_sequestration_potential"],
                          "technical": ["current_offshore_wind_farms", "distance_from_offshore_wind_farm", "potential_wind_farm_capacity"]}
    
    criteria = list(data.columns)
    stakeholder_groups = {}
    for group, group_criteria in default_stakeholder_groups.items():
        criteria_tmp = []
        for criterion in group_criteria:
            if criterion in criteria:
                criteria_tmp.append(criterion)
        if criteria_tmp:
            stakeholder_groups[group] = criteria_tmp
        
    while(True):
        print("1. Select Stakeholder Groups")
        print("2. Select Criteria")
        print("3. Back to Main Menu")
        subsub_choice = input("Select an option (1-3): ")
        
        stakeholder_selection = None
        criteria_selection = None
        
        if subsub_choice == "1":
            stakeholder_selection = select_stakeholders(stakeholder_groups)
            if stakeholder_selection is not None:
                break
        elif subsub_choice == "2":
            criteria_selection, types = select_criteria(list(data.columns), return_types=True)
            if criteria_selection is not None:
                break
        elif subsub_choice == "3":
            break
        else:
            print(invalid_input_message())
            
    if stakeholder_selection is not None:
        criteria_selection = list(data.columns)
        stakeholder_selection = {key: stakeholder_groups[key] for key in stakeholder_selection}
        return simulate_decision_making(data, stakeholder_selection, criteria_selection)
    elif criteria_selection is not None:
        stakeholder_selection = dict(stakeholder_groups)
        for group, criteria in stakeholder_selection.items():
            criteria_tmp = []
            for criterion in criteria:
                if criterion in criteria_selection:
                    criteria_tmp.append(criterion)
            stakeholder_selection[group] = criteria_tmp
        return simulate_decision_making(data, stakeholder_selection, criteria_selection)


# =============================================================================
# Dataset Evaluation
# =============================================================================
def evaluate_dataset(dataset):
    """
    Convert data to Likert 9-point evaluation scale compared to the mean value.
    1 - Extremely Poor
    2 - Very Poor
    3 - Poor
    4 - Below Average
    5 - Fair
    6 - Above Average
    7 - Good
    8 - Very Good
    9 - Extremely Good
    """
    # Calculate the deviation from mean value
    deviation = ((dataset - dataset.mean()) / dataset.mean())
    deviation_max = 1
    deviation_min = -1
    normalized_deviation = (deviation - deviation_min) / (deviation_max - deviation_min)
    # Scaling to the range of 9-point scale
    scale_max = 9
    scale_min = 1
    evaluated_dataset = normalized_deviation * (scale_max - scale_min) + scale_min
    
    evaluated_dataset = np.array(evaluated_dataset)
    evaluated_dataset = np.rint(evaluated_dataset)
    evaluated_dataset[evaluated_dataset > 9] = 9
    evaluated_dataset[evaluated_dataset < 1] = 1
    
    return evaluated_dataset.astype(int)

# =============================================================================
# Sensitivity Analysis
# =============================================================================
def sensitivity_analysis(data, selected_data, criteria, types, selection_index):
    # Begin with equal weights and calculate the baseline ranking -------------
    criteria_num = len(criteria)
    baseline_weights = np.zeros(criteria_num) + (1. / criteria_num)
    
    ranking = TOPSIS(selected_data, baseline_weights, types)
    result = selected_data.copy()
    result["Ranking"] = ranking
    result.sort_values("Ranking", ascending=False, inplace=True)
    result["community_name"] = data.loc[result.index]["community_name"]
    baseline_ranking = result
    
    ranking_analysis = baseline_ranking[["Ranking"]].copy()
    ranking_analysis.rename(columns={"Ranking": "baseline_ranking"}, inplace=True)
    
    # Simulate weight changes and calculate ranking ---------------------------
    weight_range = [0.1, 0.15, 0.2, 0.25, 0.3]
    for i in range(criteria_num):
        for weight in weight_range:
            weights = np.zeros(criteria_num) + ((1.-weight) / (criteria_num-1))
            weights[i] = weight
            ranking = TOPSIS(selected_data, weights, types)
            result = selected_data.copy()
            result["Ranking"] = ranking
            result.sort_values("Ranking", ascending=False, inplace=True)
            result["community_name"] = data.loc[result.index]["community_name"]
            ranking = result
            ranking_analysis = pd.merge(ranking_analysis, ranking[["Ranking"]], left_index=True, right_index=True)
            ranking_analysis.rename(columns={"Ranking": f"{criteria[i]}_{weight}"}, inplace=True)

    # Analyze how each criteria influences the selected alternative -----------
    selection_analysis = ranking_analysis.loc[selection_index]
    selection_baseline_ranking = selection_analysis["baseline_ranking"]
    selection_community = data.loc[selection_index]["community_name"]
    selection_distance_from_shore = data.loc[selection_index]["distance_from_offshore_wind_farm"]
    selection_sensitivity = {}
    impact_range = {}
    for criterion in criteria:
        criterion_analysis = selection_analysis.filter(like=criterion, axis=0).tolist()
        selection_sensitivity[criterion] = {"min": np.min(criterion_analysis), "baseline": selection_baseline_ranking, "max": np.max(criterion_analysis)}
        impact_range[criterion] = np.max(criterion_analysis) - np.min(criterion_analysis)
        
    selection_sensitivity = pd.DataFrame.from_dict(selection_sensitivity).transpose()
    impact_range = pd.DataFrame.from_dict(impact_range, orient="index", columns=["impact"]).sort_values("impact", ascending=False)
    selection_sensitivity = selection_sensitivity.reindex(impact_range.index)

    sorted_criteria = list(selection_sensitivity.index)
    sorted_sensitivity = selection_sensitivity.to_numpy()

    # Plot impact ranges ------------------------------------------------------
    plt.figure(figsize=(20, 6))
    for i in range(len(sorted_criteria)):
        plt.barh(sorted_criteria[i], sorted_sensitivity[i, 2] - sorted_sensitivity[i, 1], left=sorted_sensitivity[i, 1], color='skyblue')
        # plt.barh(sorted_criteria[i], sorted_sensitivity[i, 1] - sorted_sensitivity[i, 0], left=sorted_sensitivity[i, 0], color='lightcoral')
        if sorted_sensitivity[i, 1] - sorted_sensitivity[i, 0] > 0:
            plt.barh(sorted_criteria[i], sorted_sensitivity[i, 1] - sorted_sensitivity[i, 0], left=sorted_sensitivity[i, 0], color='lightcoral')
        else:
            plt.barh(sorted_criteria[i], sorted_sensitivity[i, 1] - sorted_sensitivity[i, 0], left=sorted_sensitivity[i, 0], color='skyblue')

    plt.axvline(selection_baseline_ranking, color="gray", linestyle='--', label="Baseline")
    plt.xlabel("Score")
    plt.ylabel("Criteria")
    plt.title(f"Sensitivity Analysis ({selection_community}, distance from shore {selection_distance_from_shore} km)")
    plt.legend(['Baseline', 'Positive Impact', 'Negative Impact'])
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.savefig(f"Sensitivity Analysis ({selection_community}, distance from shore {selection_distance_from_shore} km).png")
    plt.close()
    
    return selection_sensitivity
