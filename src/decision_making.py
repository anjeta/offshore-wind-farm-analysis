# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

import numpy as np
from pyDecision.algorithm import ahp_method, fuzzy_ahp_method
from pyDecision.algorithm import topsis_method, fuzzy_topsis_method
import random


# =============================================================================
# Pairwise Comparison Matrix (PCM)
# =============================================================================
def PCM(criteria_num, preferable_criteria_range):
    """
    Generate pairwise comparison matrix by sampling importance scores from a 
    uniform distribution.
    """
    PCM = np.ones((criteria_num, criteria_num))

    i, j = 0, 0
    while i < np.size(PCM, 0):
        j = i + 1
        while j < np.size(PCM, 1):
            if i in preferable_criteria_range and j in preferable_criteria_range:
                score = random.choice(range(1, 3))
                exp = random.choice([-1, 1])
            elif i in preferable_criteria_range and j not in preferable_criteria_range:
                score = random.choice(range(3, 6))
                exp = 1
            elif i not in preferable_criteria_range and j in preferable_criteria_range:
                score = random.choice(range(3, 6))
                exp = -1
            elif i not in preferable_criteria_range and j not in preferable_criteria_range:
                score = random.choice(range(1, 3))
                exp = random.choice([-1, 1])
            PCM[i, j] = score ** exp
            PCM[j, i] = score ** (-exp)
            j += 1
        i += 1
    
    return PCM

# =============================================================================
# Fuzzy Pairwise Comparison Matrix (Fuzzy PCM)
# =============================================================================
def fuzzify_PCM(PCM):
    """
    Fuzzify pairwise comparison matrix.
    """
    fuzzy_PCM = np.empty_like(PCM, dtype=object)
    
    i, j = 0, 0
    while i < np.size(PCM, 0):
        j = i
        while j < np.size(PCM, 1):
            if i == j:
                fuzzy_PCM[i, j] = (1, 1, 1)
            else:
                m = PCM[i, j]
                if m < 1:
                    x = 1 / m
                    if x == 9:
                        l = 1 / x
                    else:
                        l = 1 / (x+1)
                    u = 1 / (x-1)
                elif m == 1:
                    l = m / 2
                    u = m + 1
                else:
                    l = m - 1
                    if m == 9:
                        u = m
                    else:
                        u = m + 1
                fuzzy_PCM[i, j] = (l, m, u)
                fuzzy_PCM[j, i] = (1/u, 1/m, 1/l)
            j += 1
        i += 1
    
    fuzzy_PCM = [list(row) for row in fuzzy_PCM]
    return fuzzy_PCM


# =============================================================================
# Decision Matrix (DM)
# =============================================================================
def DM(evaluated_dataset, preferable_criteria_range):
    """
    Generate decision matrix by sampling evaluation scores for each alternative
    and criteria combination from a uniform distribution.
    """
    DM = np.zeros_like(evaluated_dataset)
    
    for i in range(np.size(DM, 0)):
        for j in range(np.size(DM, 1)):
            if j in preferable_criteria_range:
                evaluated_value = int(evaluated_dataset[i, j])
                score = random.choice(range(evaluated_value-2, evaluated_value+2))
                if score > 9:
                    score = 9
                elif score < 1:
                    score = 1
                DM[i, j] = score
            else:
                DM[i, j] = 5
    return DM

# =============================================================================
# Fuzzy Decision Matrix (Fuzzy DM)
# =============================================================================
def fuzzify_DM(DM):
    """
    Fuzzify decision matrix.
    """
    fuzzy_DM = np.empty((np.size(DM, 0), np.size(DM, 1)), dtype=object)
    mapping = {"1": (1, 1, 2), "2": (2, 2, 3), "3": (3, 3, 4), "4": (4, 4, 5), 
               "5": (5, 5, 6), "6": (6, 6, 7), "7": (7, 7, 8), "8": (8, 8, 9),
               "9": (9, 9, 9)}
    # mapping = {"1": (1, 1, 3), "2": (1, 2, 4), "3": (1, 3, 5), "4": (2, 4, 6), 
    #            "5": (3, 5, 7), "6": (4, 6, 8), "7": (5, 7, 9), "8": (6, 8, 9),
    #            "9": (7, 9, 9)}
        
    for i in range(np.size(DM, 0)):
        for j in range(np.size(DM, 1)):
            fuzzy_DM[i, j] = mapping[str(DM[i, j])]
    
    return fuzzy_DM


# =============================================================================
# Analytic Hieraracy Process (AHP)
# =============================================================================
def AHP(PCM_list, verbose=False):
    weights_list = []
    
    # Calculate criteria weights based on each stakeholder's judgement matrix
    # (pairwise comparison matrix)
    for PCM in PCM_list:
    
        weight_derivation = 'max_eigen'  # 'mean'; 'geometric' or 'max_eigen'
        weights, rc = ahp_method(PCM, wd=weight_derivation)
        
        if verbose:
            for i in range(0, weights.shape[0]):
                print('w(C'+str(i+1)+'): ', round(weights[i], 3))
            
            # Consistency Ratio
            print('RC: ' + str(round(rc, 2)))
            if (rc > 0.10):
                print('The solution is inconsistent, the pairwise comparisons must be reviewed')
            else:
                print('The solution is consistent')
            
        if (rc < 0.10):
            weights_list.append(weights)
          
    weights_array = np.array(weights_list)
    ahp_weights = np.mean(weights_array, axis=0)
    
    return ahp_weights

# =============================================================================
# Fuzzy Analytic Hieraracy Process (Fuzzy AHP)
# =============================================================================
def fuzzy_AHP(PCM_list, verbose=False):
    weights_list = []
    fuzzy_weights_list = []
    consistent_fuzzy_PCM_list = []
    
    # Fuzzify stakeholder's judgement matrices and check their consistency
    # Then, calculate fuzzy criteria weights based on each stakeholder's fuzzified
    # judgement matrix (fuzzified pairwise comparison matrix)
    for PCM in PCM_list:
        
        fuzzy_PCM = fuzzify_PCM(PCM)
        fuzzy_weights, defuzzified_weights, normalized_weights, rc = fuzzy_ahp_method(fuzzy_PCM)
        
        if verbose:
            # Fuzzy weights
            print("\nFuzzy weights:")
            for i in range(0, len(fuzzy_weights)):
                print('g'+str(i+1)+': ', np.around(fuzzy_weights[i], 3))
              
            # Crisp Weigths
            print("\nCrisp weights:")
            for i in range(0, len(defuzzified_weights)):
                print('g'+str(i+1)+': ', round(defuzzified_weights[i], 3))
              
            # Normalized Weigths
            print("\nNormalized weights:")
            for i in range(0, len(normalized_weights)):
                print('g'+str(i+1)+': ', round(normalized_weights[i], 3))
                
            # Consistency Ratio
            print('RC: ' + str(round(rc, 2)))
            if (rc > 0.10):
                print('The solution is inconsistent, the pairwise comparisons must be reviewed')
            else:
                print('The solution is consistent')
        
        if (rc < 0.10):
            weights_list.append(normalized_weights)
            fuzzy_weights_list.append(fuzzy_weights)
            consistent_fuzzy_PCM_list.append(fuzzy_PCM)
    
    # Aggregate fuzzy PCM -----------------------------------------------------
    if not weights_list:
        return None, None
        
    weights_array = np.array(weights_list)
    criteria_num = len(np.mean(weights_array, axis=0))
    
    consistent_fuzzy_PCM_array = np.array(consistent_fuzzy_PCM_list)
    aggregate_fuzzy_PCM = np.empty((criteria_num, criteria_num), dtype=object)
    for i in range(criteria_num):
        for j in range(criteria_num):
            l = consistent_fuzzy_PCM_array[:, i, j, 0]
            m = consistent_fuzzy_PCM_array[:, i, j, 1]
            u = consistent_fuzzy_PCM_array[:, i, j, 2]
            aggregate_fuzzy_PCM[i, j] = (np.min(l), m.prod()**(1.0/len(m)), np.max(u))
            
    # Calculate aggregated fuzzy weights --------------------------------------
    fuzzy_weights, defuzzified_weights, normalized_weights, rc = fuzzy_ahp_method(aggregate_fuzzy_PCM)
        
    if verbose:
        # Fuzzy weights
        print("\nFuzzy weights:")
        for i in range(0, len(fuzzy_weights)):
            print('g'+str(i+1)+': ', np.around(fuzzy_weights[i], 3))
          
        # Crisp Weigths
        print("\nCrisp weights:")
        for i in range(0, len(defuzzified_weights)):
            print('g'+str(i+1)+': ', round(defuzzified_weights[i], 3))
          
        # Normalized Weigths
        print("\nNormalized weights:")
        for i in range(0, len(normalized_weights)):
            print('g'+str(i+1)+': ', round(normalized_weights[i], 3))
            
        # Consistency Ratio
        print('RC: ' + str(round(rc, 2)))
        if (rc > 0.10):
            print('The solution is inconsistent, the pairwise comparisons must be reviewed')
        else:
            print('The solution is consistent')
            
    return normalized_weights, fuzzy_weights_list


# =============================================================================
# Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)
# =============================================================================
def TOPSIS(data, weights, types):
    """
    Calculating the ranking of variables based on criteria.
    """
    ranking = topsis_method(data, weights, types, graph = False, verbose = False)
    return ranking


# =============================================================================
# Fuzzy TOPSIS
# =============================================================================
def fuzzy_TOPSIS(fuzzy_weights_list, DM_list, types):
    
    criteria_num = len(fuzzy_weights_list[0])
    alternative_num = len(DM_list[0])
    
    aggregated_fuzzy_weights = aggregate_fuzzy_weights(fuzzy_weights_list).tolist()
    
    # Generate a fuzzy decision matrix from simulated ranking of alternatives and
    # criteria by a group of stakeholders
    fuzzy_DM_list = []
    for DM in DM_list:
        fuzzy_DM = fuzzify_DM(DM)
        fuzzy_DM_list.append(fuzzy_DM)
    
    fuzzy_DM_array = np.array(fuzzy_DM_list)
    aggregated_fuzzy_DM = np.empty((alternative_num, criteria_num), dtype=object)
    
    for i in range(alternative_num):
        for j in range(criteria_num):
            l = np.array([f[0] for f in list(fuzzy_DM_array[:, i, j])])
            m = np.array([f[1] for f in list(fuzzy_DM_array[:, i, j])]).astype(np.int64)
            u = np.array([f[2] for f in list(fuzzy_DM_array[:, i, j])])
            # aggregate_fuzzy_DM[i, j] = (np.min(l), np.mean(m), np.max(u))  # With arithmetic mean
            aggregated_fuzzy_DM[i, j] = (np.min(l), m.prod()**(1.0/len(m)), np.max(u))  # With geometric mean
            
    ranking = fuzzy_topsis_method(aggregated_fuzzy_DM, list([aggregated_fuzzy_weights]), types, graph = False, verbose = False)
    return ranking


def aggregate_fuzzy_weights(fuzzy_weights_list, mode="geometric"):
    
    criteria_num = len(fuzzy_weights_list[0])
    
    # Aggregate fuzzy weights
    fuzzy_weights_array = np.array(fuzzy_weights_list)
    aggregate_fuzzy_weights = np.empty((criteria_num), dtype=object)

    for i in range(criteria_num):
        l = fuzzy_weights_array[:, i, 0]
        m = fuzzy_weights_array[:, i, 1]
        u = fuzzy_weights_array[:, i, 2]
        if mode == "arithmetic":
            aggregate_fuzzy_weights[i] = (np.min(l), np.mean(m), np.max(u))  # With arithmetic mean
        elif mode == "geometric":
            aggregate_fuzzy_weights[i] = (np.min(l), m.prod()**(1.0/len(m)), np.max(u))  # With geometric mean
        else:
            print(f"Invalid aggregation mode: {mode}")
            break
    return aggregate_fuzzy_weights

# =============================================================================
# WHAT-IF Scenario Analysis
# =============================================================================
def compare_locations(data, selected_data, criteria):
    filtered_data = data[criteria]
    # Calculate the deviation from mean value
    deviation = ((selected_data - filtered_data.mean()) / filtered_data.mean()) * 100
    return deviation