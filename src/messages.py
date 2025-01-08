# -*- coding: utf-8 -*-
"""
@author: Aneta Kartali
"""

def info_message():
    return "\nBefore the analysis you must upload the file containing performance data (Option 1). This is the information on how each location alternative performs against each criterion. After uploading the performance data, you can asses the available offshore wind farm location alternatives."

def invalid_input_message():
    return "\nInvalid input. Please try again.\n"

def load_file_message():
    return "\nData should be stored in a tabular form, in a .txt or .csv file. Please enter the path to file containing the data:\n"

def select_data_message():
    return "\nYou can select the data you want to consider in the analysis by specifying criteria types that will be used and criteria constraints that will be applied to your data.\n"

def criteria_selection_message():
    return "\nIf you wish to consider only certain criteria in the decision making analysis, please specify them. By default, all criteria are taken into consideration.\nTo enter prefered criteria, please type them in a comma separated manner (Option 1), or upload a file containing desired criteria (Option 2).\n"

def cost_benefit_message():
    return "\nBefore we continue, you need to specify whether each of the selected criteria is a cost or a benefit. In other words, you will specify whether each criteria needs to be maximized (if it is a benefit) or minimized (if it is a cost). This is a crucial step for the decision making process.\n"

def constraints_message():
    return "\nYou can further specify the constraints for viable offshore wind farm locations. By default, no constraints are defined and all data is taken into consideration. To enter constraints, please type desired criteria in a comma separated manner (Option 1), or upload a file containing constraints data (Option 2).\n"

def restrictions_message():
    return "\nFor each of the criteria you selected, you need to specify a threshold value above which the data is not valid for analysis. Defining constraints is an inportant aspect of the decision making process.\n"
    
def weighting_message():
    return "\nFor ranking alternative locations for offshore wind farm installation, evaluation criteria has to be weighted. Weights can be equal for all criteria (Option 1), calculated based on evaluation data obtained from stakeholders (Option 2), or simulated (Option 3).\n"

def ranking_message():
    return "\nThere are two ranking algorithm options to select from. One performs Technique for Order of Preference by Similarity to Ideal Solution (Option 1), while the other represents the fuzzy option which uses fuzzified weights (Option 2).\n"

def simulate_data_message():
    return "\nFor ranking alternative offshore wind farm locations let's simulate evaluation data obtained from different stakeholders. This data will contain information about the pairwise comparison of evaluation criteria. For simulating decision making of stakeholders you can select specific stakeholder groups (Option 1), or specific decision making criteria (Option 2).\n"

def select_stakeholders_message():
    return "\nTo ensure balanced decision making, all stakeholder groups are taken into consideration by default. If you wish to choose stakeholder groups for simulating preferences, please specify them. Note that taking only some stakeholder groups' preferences into consideration will result in decisions made ignoring the importance of some of the criteria. To select stakeholder groups, please type them in a comma separated manner. Press Enter to select all stakeholder groups.\n"

def ranking_option_message():
    return "\nRanking will result in a sorted list of all alternative offshore wind farm locations, ranked by existing criteria and their importance.\n"

def evaluation_message():
    return "\nFor each of the selected areas, you can see how each offshore wind farm location influences selected criteria, compared to their average value calculated from all possible areas and locations. This way, you can see how specific location performs in terms of selected criteria - the values are displayed in percentages of gain.\n"
    
def area_selection_message():
    return "\nFor location evaluation, please select the area(s) you want to evaluate. If you wish to select multiple areas, please separate them with a comma. To take all areas into consideration, press Enter.\n"

def factor_selection_message():
    return "\nIf you wish to consider only certain criteria in the evaluation analysis, please specify them. By default, all criteria are taken into consideration.\nTo enter prefered criteria, please type them in a comma separated manner (Option 1), or upload a file containing desired criteria (Option 2).\n"

def sensitivity_option_message():
    return "\nSensitivity analysis provides insights how stable each alternative is to the changes of stakeholder preferences (i.e. criteria weights).\n"

def sensitivity_message():
    return "\nTo perform sensitivity analysis, please specify an offshore wind farm location alternative based on its ranking. For example, for evaluating the best ranked location, type 1.\n"