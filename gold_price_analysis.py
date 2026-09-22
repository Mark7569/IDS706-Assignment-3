import kagglehub
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def load_data(csv_path):
    return pd.read_csv(csv_path)


def preprocess_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    return df


def filter_high_GLD_price(df):
    return df[df["GLD"] > 200]


def calculate_yearly_average_GLD_price(df):
    return df.groupby("Year").mean(numeric_only=True)


# ML
def train_model(df):
    model_inputs = df[["SPX", "USO", "SLV", "EUR/USD"]]
    model_outputs = df["GLD"]
    X_train, X_test, y_train, y_test = train_test_split(
        model_inputs, model_outputs, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return model, X_test, y_test, predictions


def main():
    # import the gold price dataset from kaggle
    path = kagglehub.dataset_download("mdanwarhossain200110/gold-price-2015-2025")
    print("Path to dataset files:", path)

    csv_path = os.path.join(path, "gold_data_2015_25.csv")
    df = load_data(csv_path)

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

    # preprocess the data
    df = preprocess_data(df)

    print(df.head())
    df.info()

    # basic filtering and grouping
    high_gold_price = filter_high_GLD_price(df)

    print("\nObservations with GLD above 200:")
    print(high_gold_price.head())

    yearly_avg_gold = calculate_yearly_average_GLD_price(df)

    print("\nAverage GLD Price by Year:")
    print(yearly_avg_gold)

    # linear regression
    model, X_test, y_test, predictions = train_model(df)

    results = pd.DataFrame({"Actual": y_test, "Predicted": predictions})

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


if __name__ == "__main__":
    main()
