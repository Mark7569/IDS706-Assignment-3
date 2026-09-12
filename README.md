# GOLD PRICE ANALYSIS

## Project Overview
This project analyzes gold price data from 2015 to 2025 with Python and Pandas. The dataset also contains several financial market variables, including the S&P 500 (SPX), oil (USO), silver (SLV), and the EUR/USD exchange rate. The project explores the dataset through basic data inspection, filtering, grouping, visualization, and a simple linear regression model.

## Dataset
The dataset was downloaded from Kaggle. It contains six variables and 2666 observations in total:
- Date
- SPX
- GLD
- USO
- SLV
- EUR/USD

## Data Inspection
In data inspection, 'head()', 'info()', and 'describe()' were used to inspect and summarize the data. At the same time, missing values and duplicate were checked.

## Filtering and Grouping
The Date column was converted to a datetime format and a Year variable was created.
I filtered the dataset to examine observations where GLD was above 200. 
I also grouped the data by Year and calculated the average GLD price for each year.

The yearly averages show an increase in GLD prices over the sample period, with a particularly noticeable increase in the later years.

## Machine Learning
Linear regression was chose to predict GLD prices.
Inputs:
- SPX
- USO
- SLV
- EUR/USD

Outputs:
- GLD

I split the dataset into 80% training data and 20% testing data. The linear regression model achieved an R-squared value of approximately 0.921 on the test set.

## Visualization
I created a scatter plot comparing the actual GLD prices with the values predicted by the linear regression model.
The plot shows a strong positive relationship between actual and predicted GLD values. Most predictions are relatively close to the actual values, although larger prediction errors appear at higher GLD prices.

## Conclusion
The analysis shows that GLD prices generally increased from 2015 to 2025. The initial linear regression experiment also suggests that SPX, USO, SLV, and EUR/USD contain useful information for explaining variation in GLD prices.