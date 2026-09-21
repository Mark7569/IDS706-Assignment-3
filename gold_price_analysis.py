import kagglehub
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# import the dataset of gold price from kaggle
path = kagglehub.dataset_download("mdanwarhossain200110/gold-price-2015-2025")

print("Path to dataset files:", path)

csv_path = os.path.join(path, "gold_data_2015_25.csv")
df = pd.read_csv(csv_path)


# inspect the dataset
print(df.head())

print("\nDataset Information:")
df.info()

print("\nSummary Statistics:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nNumber of Duplicate Rows:")
print(df.duplicated().sum())


# basic filtering and grouping
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

print(df.head())
df.info()

high_gold_price = df[df["GLD"] > 200]
print("\nObservations with GLD above 200:")
print(high_gold_price.head())

yearly_avg_gold = df.groupby("Year")["GLD"].mean()
print("\nAverage GLD Price by Year:")
print(yearly_avg_gold)


# ML
# linear regression
model_inputs = df[["SPX", "USO", "SLV", "EUR/USD"]]
model_outputs = df["GLD"]

print("\nModel Inputs:")
print(model_inputs.head())
print("\nModel Output:")
print(model_outputs.head())

X_train, X_test, y_train, y_test = train_test_split(
    model_inputs, model_outputs, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
results = pd.DataFrame({"Actual GLD": y_test, "Predicted GLD": predictions})

print("\nActual vs Predicted GLD:")
print(results.head())

print("\nR-squared:")
print(model.score(X_test, y_test))


# visualization
plt.scatter(y_test, predictions)
plt.xlabel("Actual GLD")
plt.ylabel("Predicted GLD")
plt.title("Actual vs Predicted GLD Prices")
plt.savefig("gold_price_visualization.png", bbox_inches="tight")
plt.show()
