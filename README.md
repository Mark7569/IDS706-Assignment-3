# GOLD PRICE ANALYSIS

[![Python Tests](https://github.com/Mark7569/IDS706-Assignment-3/actions/workflows/test.yml/badge.svg)](https://github.com/Mark7569/IDS706-Assignment-3/actions/workflows/test.yml)

## Project Overview

This project analyzes gold price data from 2015 to 2025 with Python, Pandas, and Polars. The dataset also contains several financial market variables, including the S&P 500 (SPX), oil (USO), silver (SLV), and the EUR/USD exchange rate. The project explores the dataset through basic data inspection, filtering, grouping, visualization, and a simple linear regression model.

## Problem Statement

Gold prices are influenced by movements across different financial markets. This project examines how gold prices changed from 2015 to 2025 and explores whether market variables including the S&P 500 (SPX), oil (USO), silver (SLV), and the EUR/USD exchange rate can help explain variation in GLD prices.

The analysis focuses on three questions:

- How did average GLD prices change over time?
- What can be learned from periods when GLD prices were above 200?
- How well can SPX, USO, SLV, and EUR/USD explain GLD prices using a simple linear regression model?

## Files

- "gold_price_analysis.py"
- "gold_price_visualization.png"
- "pandas_vs_polars.py"
- "rust_vs_python_intro.ipynb"

## Dataset

The dataset was downloaded from Kaggle. It contains six variables and 2666 observations in total:
- Date
- SPX
- GLD
- USO
- SLV
- EUR/USD

## Setup

Install the required Python packages:

```bash
pip install pandas scikit-learn matplotlib kagglehub pytest black flake8
```

Run the analysis with:

```bash
python gold_price_analysis.py
```

## Testing

The project includes unit tests for data loading, preprocessing, filtering, yearly average calculation, linear regression modeling, and visualization. An edge case tests the filtering function when no GLD prices are above 200. An entire system test is also included to validate the complete analysis workflow.

The current test suite contains 8 tests.

Run the tests with:

```bash
python -m pytest tests/ -v
```

## Testing Results

![Pytest Results](screenshots/pytest_results.png)

## Code Quality

Black and Flake8 are used to maintain consistent formatting and code quality.

Check code formatting with:

```bash
black --check gold_price_analysis.py tests/test_gold_price_analysis.py
```

Run linting with:

```bash
flake8 gold_price_analysis.py tests/test_gold_price_analysis.py
```

The Flake8 configuration uses a maximum line length of 88 characters to remain consistent with Black.

## Refactoring

I refactored the project to improve readability and make the code easier to test and maintain. I renamed functions to use consistent snake_case naming and extracted data inspection and visualization logic from `main()` into separate functions.

For example, the data inspection code was moved into an `inspect_data()` function, which makes `main()` shorter and gives each function a clearer responsibility. I also extracted the visualization logic into `create_visualization()` and added a test for the generated visualization.

After refactoring, I ran pytest, Black, and Flake8 to verify that the project still works correctly and follows consistent code-quality standards.

### Refactoring Evidence

The commit diff below shows the data inspection logic being removed from `main()` and replaced with a call to the new `inspect_data()` function.

<img src="screenshots/refactoring_diff.png" width="700">

## Continuous Integration

GitHub Actions automatically runs the project checks whenever changes are pushed to the repository or submitted through a pull request. The workflow is also scheduled to run weekly.

The CI workflow tests the project with Python 3.10, 3.11, and 3.12. For each Python version, it:

- checks code formatting with Black,
- checks code quality with Flake8, and
- runs the complete pytest test suite.

All three Python environments currently pass the CI workflow.

![GitHub Actions Results](screenshots/github_actions.png)

## Docker and Containerization

The project is containerized with Docker so that the analysis can run in a consistent and reproducible environment.

### Build the Docker Image

```bash
docker build -t gold-price-analysis .
```

### Run the Container

```bash
docker run --name gold-price-container gold-price-analysis
```
The container downloads the dataset, runs the full analysis, trains the regression model, and generates the visualization. A successful run exits with status code 0.

### Verify the Container

```bash
docker ps -a
docker images
```

### What I learned

Containerizing the project helped me understand how Docker packages the code and its dependencies into a reproducible environment. I also practiced building images, running containers, checking container status, and verifying that the analysis produces the expected output inside the container.

### Docker Evidence

Successful image build:
<img src="screenshots/docker_image.png" width="700">

Successful container run:
<img src="screenshots/docker_container.png" width="700">


## Data Inspection

In data inspection, 'head()', 'info()', and 'describe()' were used to inspect and summarize the data. At the same time, missing values and duplicate were checked.

## Data Cleaning and Outlier Treatment

I checked the dataset for missing values and duplicate observations before conducting the analysis. No missing values or duplicate rows were found, so no observations needed to be removed for these reasons.

I also reviewed the numerical variables using summary statistics. I did not automatically remove unusually high or low values because financial market data can contain genuine extreme movements that are economically meaningful. Instead, the original observations were retained for the analysis.

The GLD > 200 filter used in this project is an analytical choice for examining periods of relatively high gold prices rather than an outlier-removal rule.

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

![Actual vs Predicted GLD Prices](gold_price_visualization.png)

## Key Findings and Takeaways

- Average GLD prices generally increased over the 2015–2025 period, with stronger increases appearing in the later years.
- Filtering observations where GLD was above 200 helped isolate relatively high-price periods for further inspection.
- The linear regression model achieved an R-squared of approximately 0.921 on the test set, indicating that SPX, USO, SLV, and EUR/USD together explain a large portion of the variation in GLD prices in this dataset.
- The actual-versus-predicted visualization shows that most predictions are relatively close to the observed GLD values, although prediction errors become more noticeable for some higher-price observations.
- These results show useful relationships between GLD and other financial market variables, but they should not be interpreted as evidence that these variables cause changes in gold prices.

## Pandas vs. Polars Comparison

I re-implemented the main data manipulation operations using Polars and compared them with my original Pandas implementation. Both approaches created a Year column, filtered observations where GLD was greater than 200, and calculated the average GLD price by year.

The syntax is slightly different between the two libraries. Pandas uses direct DataFrame indexing and `groupby()`, while Polars uses expressions such as `pl.col()`, `filter()`, and `group_by()`.

I also compared the runtime of the two implementations using `time.perf_counter()`:
- Pandas runtime: 0.007119 seconds
- Polars runtime: 0.002176 seconds

In this run, Polars was about 3.27 times faster than Pandas. However, since this dataset contains only 2,666 observations and the measured runtimes are very short, this simple benchmark should not be interpreted as a general performance comparison between the two libraries.

## Conclusion

The analysis shows that GLD prices generally increased from 2015 to 2025. The linear regression experiment also suggests that SPX, USO, SLV, and EUR/USD contain useful information for explaining variation in GLD prices, although these relationships should not be interpreted as causal.

The project was improved through automated testing, continuous integration, code refactoring, Black and Flake8 checks, and Docker containerization. These additions make the analysis more reliable, reproducible, and easier to maintain.