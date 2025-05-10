# car-analysis
Car Dataset Analysis
🔍 Objective:
The notebook performs data analysis on a dataset of cars, focusing on key features such as fuel type, mileage, engine size, power, and pricing to derive insights and visualize trends.

📊 Key Steps in the Notebook:
1. Data Loading & Cleaning
Reads a CSV file containing car data.

Handles missing values.

Cleans and converts data types (e.g., Mileage, Engine, Power columns converted from string formats to numeric).

2. Exploratory Data Analysis (EDA)
Uses pandas and matplotlib/seaborn for visualization.

Common analyses include:

Distribution of car prices.

Relationship between car brand and price.

Correlation heatmaps to analyze variable relationships.

3. Data Visualization
Bar plots, box plots, and heatmaps are used to understand:

Average prices by car brand.

Price trends based on fuel type, transmission, and ownership.

Feature correlations.

4. Feature Engineering
Extracts brand names from car names.

Converts categorical columns (like Fuel_Type, Transmission) to numeric or encoded formats for analysis.

📌 Insights Derived:
Brands like Audi, BMW, and Mercedes tend to have higher average prices.

Cars with automatic transmission are generally more expensive than manual ones.

Mileage and power show notable influence on pricing.

🧰 Technologies Used:
Python libraries: pandas, numpy, matplotlib, seaborn

