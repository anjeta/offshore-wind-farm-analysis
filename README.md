# **What-If Scenario Analysis and Decision Support Algorithm for Offshore Wind Farm Installation**

## **Project Overview**
A console-based tool for offshore wind farm location analysis that includes:
1. Location comparison based on different criteria.
2. Location ranking and optimal location selection based on desired criteria and their impact.
> 2.1. Stakeholder preferences can be read from a file or simulated.
> 2.2. Utilizing AHP (Analytic Hierarchy Process) for determining criteria weights and TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) for location ranking.
> 2.3. Uncertainty in decision making can be considered by employing a fuzzy logic approach.
3. Location evaluation with what-if scenario analysis. Assessing how selected locations perform compared to the average performance for each of the selected criteria.
4. Location evaluation with sensitivity analysis. Assessing how stable the selected location is to changes in stakeholder preferences.

## **Requirements**
Ensure you have the following dependencies installed (also available in `requirements.txt` file):
```bash
pip install matplotlib==3.8.0 numpy==1.26.4 pandas==2.1.4 pyDecision==4.5.8
```

## **Installation and Run**
1. Download the repository to your local machine.

2. Navigate to the repository on your local machine and open a terminal.

3. Run offshore_wind_farm_analysis.py script.
   ```bash
   python offshore_wind_farm_analysis.py
   ```

## **Structure**
`src` folder contains the code. Main is located in `offshore_wind_farm_analysis.py` file.
`data` folder contains exemplary data:
1. `Synthetic_Socio-Ecological_Data.csv` - Eample of performance data.
2. `Criteria_Selection.csv` - Example of criteria selection.
3. `Constraints.csv` - Example of constraints.
`reports` folder contains results example from the available synthetic dataset.


## **Usage**
Here is an example of application usage:
1. Run `offshore_wind_farm_analysis.py` and type `0` to view the information about the app.
2. Press Enter to acknowledge and type `1` to load the performance data.
3. Copy the path to the `Synthetic_Socio-Ecological_Data.csv` file and paste it in the console UI.
4. Type `3` to perform scenario analysis based on the available performance data. Select the area(s) you want to investigate and the criteria you want to compare the locations by. The criteria can be loaded via file upload or specified directly in the UI. Scenario analysis will be saved as a csv file.
5. Type `4` to define priorities and constraints for further location assessment and decision making. 
6. Type `2` to load a criteria file. Criteria selection can also be done manually in the terminal.
7. Copy the path to the `Criteria_Selection.csv` file and paste it in the console UI.
8. Type `2` to load the constraints file. Constraints can also be selected manually in the terminal
9. Copy the path to the `Constraints.csv` file and paste it in the console UI.
10. Type `YES` to remove restricted criteria from the analysis (this is not mandatory).
11. Type `5` to rank alternative locations.
12. For ranking, you can equally weight all criteria, load the desired criteria weights (currently unavailable), or simulate criteria weights based on different stakeholder preferences. Type `3` to simulate stakeholder preferences.
13. Type `1` to select stakeholder groups that will influence decision making. Then press Enter to take all stakeholder groups into consideration.
14. Type `YES` to simulate uncertain stakeholder decision making and calculate fuzzy weights using Fuzzy AHP.
15. Type `2` to perform ranking applying Fuzzy TOPSIS algorithm. Ranking will be saved to a file. Press Enter to acknowledge.
16. Type `6` to perform sensitivity analysis of the best ranked location. Type `1` to choose the best ranked alternative for the analysis. The sensitivity analysis result will be saved as csv file, and graphically, as a png file. Press Enter to acknowledge.
17. Type `7` to exit the application.

---

If you encounter any issues during the run, feel free to reach out!
