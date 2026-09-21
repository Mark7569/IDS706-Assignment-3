import kagglehub
import pandas as pd
import polars as pl
import os
import time

# Download the dataset from kaggle
path = kagglehub.dataset_download("mdanwarhossain200110/gold-price-2015-2025")
csv_path = os.path.join(path, "gold_data_2015_25.csv")

# Load the dataset using pandas and polars
pd_df = pd.read_csv(csv_path)
pl_df = pl.read_csv(csv_path)

print("Pandas shape:", pd_df.shape)
print("Polars shape:", pl_df.shape)

# Create Year column with polars
pl_df = pl_df.with_columns(pl.col("Date").str.to_date().dt.year().alias("Year"))

# Observations with GLD above 200
pl_above_200 = pl_df.filter(pl.col("GLD") > 200)
print("\nPolars filtered data with GLD above 200:")
print(pl_above_200.head())

# Average GLD price by year
pl_yearly_avg_GLD = pl_df.group_by("Year").agg(pl.col("GLD").mean()).sort("Year")

print("\nPolars Average GLD Price by Year:")
print(pl_yearly_avg_GLD)


# Benchmarks Pandas
start_time = time.perf_counter()

pd_df["Date"] = pd.to_datetime(pd_df["Date"])
pd_df["Year"] = pd_df["Date"].dt.year
pandas_filtered = pd_df[pd_df["GLD"] > 200]
pd_yearly_avg_GLD = pd_df.groupby("Year")["GLD"].mean()
pandas_time = time.perf_counter() - start_time

# Benchmark Polars
start_time = time.perf_counter()
pl_benchmark_df = pl.read_csv(csv_path)

pl_benchmark_df = pl_benchmark_df.with_columns(
    pl.col("Date").str.to_date().dt.year().alias("Year")
)

pl_filtered_benchmark = pl_benchmark_df.filter(pl.col("GLD") > 200)

pl_yearly_avg_GLD = (
    pl_benchmark_df.group_by("Year").agg(pl.col("GLD").mean()).sort("Year")
)

polars_time = time.perf_counter() - start_time

print("\nRuntime Comparison:")
print(f"Pandas runtime: {pandas_time:.6f} seconds")
print(f"Polars runtime: {polars_time:.6f} seconds")
