import pandas as pd
from gold_price_analysis import (
    load_data,
    preprocess_data,
    filter_high_GLD_price,
    calculate_yearly_average_GLD_price,
    train_model,
)


# 1st unit test for data loading
def test_load_data(tmp_path):
    test_file = tmp_path / "test_gold_data.csv"
    test_data = pd.DataFrame(
        {"Date": ["2020-01-01", "2021-01-02"], "GLD": [180.0, 185.0]}
    )
    test_data.to_csv(test_file, index=False)

    result = load_data(test_file)

    assert len(result) == 2
    assert "Date" in result.columns
    assert "GLD" in result.columns


# 2nd unit test for data preprocessing
def test_preprocess_data():
    test_data = pd.DataFrame(
        {"Date": ["2020-01-01", "2021-01-01"], "GLD": [180.0, 185.0]}
    )

    result = preprocess_data(test_data)

    assert pd.api.types.is_datetime64_any_dtype(result["Date"])
    assert "Year" in result.columns
    assert result["Year"].tolist() == [2020, 2021]


# 3rd unit test for filtering
def test_filter_high_GLD_price():
    test_data = pd.DataFrame({"GLD": [180.0, 210.0, 250.0, 195.0]})

    result = filter_high_GLD_price(test_data)

    assert len(result) == 2
    assert (result["GLD"] > 200).all()


# edge case
def test_filter_high_GLD_price_empty_result():
    test_data = pd.DataFrame({"GLD": [150, 160, 200]})

    result = filter_high_GLD_price(test_data)

    assert result.empty


# 4th unit test for calculating average gold price grouping by Year
def test_calculate_yearly_average_GLD_price():
    test_data = pd.DataFrame(
        {
            "Year": [2020, 2020, 2021, 2021, 2021],
            "GLD": [180.0, 175.0, 200.0, 190.0, 210.0],
        }
    )

    result = calculate_yearly_average_GLD_price(test_data)

    assert result.loc[2020, "GLD"] == 177.5
    assert result.loc[2021, "GLD"] == 200.0


# 5th unit test for linear regression
def test_train_model():
    test_data = pd.DataFrame(
        {
            "SPX": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            "USO": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            "SLV": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "EUR/USD": [1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19],
            "GLD": [150, 155, 160, 165, 170, 175, 180, 185, 190, 195],
        }
    )

    model, X_test, y_test, predictions = train_model(test_data)

    assert len(predictions) == len(y_test)
    assert X_test.shape[1] == 4
    assert hasattr(model, "coef_")


# entire system test
def test_entire_system(tmp_path):
    test_file = tmp_path / "test_gold_data.csv"

    test_data = pd.DataFrame(
        {
            "Date": [
                "2020-01-01",
                "2020-02-01",
                "2020-03-01",
                "2020-04-01",
                "2020-05-01",
                "2021-01-01",
                "2021-02-01",
                "2021-03-01",
                "2021-04-01",
                "2021-05-01",
            ],
            "SPX": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            "USO": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            "SLV": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "EUR/USD": [1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19],
            "GLD": [180, 190, 200, 210, 220, 230, 240, 250, 260, 270],
        }
    )

    test_data.to_csv(test_file, index=False)

    df = load_data(test_file)
    df = preprocess_data(df)
    high_GLD_price = filter_high_GLD_price(df)
    yearly_avg = calculate_yearly_average_GLD_price(df)
    model, X_test, y_test, predictions = train_model(df)

    assert "Year" in df.columns
    assert (high_GLD_price["GLD"] > 200).all()
    assert len(yearly_avg) == 2
    assert len(predictions) == len(y_test)
