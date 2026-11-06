
import pandas as pd

df = pd.read_csv("customers.csv")

print("Q1: Dataset Information")
print("Shape:", df.shape)
print("Data Types:\n", df.dtypes)
print("Missing Values:\n", df.isnull().sum())

print("\nQ2: Removing Missing Customer IDs")
df.dropna(subset=["Customer_ID"], inplace=True)
print(df.shape)

print("\nQ3: Handling Missing Values")
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Total_Spent"] = df["Total_Spent"].fillna(df["Total_Spent"].mean())

print("\nQ4: Extracting Join Date Information")
df["Join_Date"] = pd.to_datetime(df["Join_Date"])
df["Join_Year"] = df["Join_Date"].dt.year
df["Join_Month"] = df["Join_Date"].dt.month_name()
print(df[["Join_Date", "Join_Year", "Join_Month"]])

print("\nQ5: Average Order Value")
df["Avg_Order_Value"] = df["Total_Spent"] / df["Order_Count"]
print(df[["Customer_ID", "Avg_Order_Value"]])

print("\nQ6: High Value Customers")
df["High_Value_Customer"] = df["Avg_Order_Value"] > 2500
print(df[["Customer_ID", "High_Value_Customer"]])

print("\nQ7: City Analysis")
city_summary = df.groupby("City").agg(
    Total_Customers=("Customer_ID", "count"),
    Average_Spent=("Total_Spent", "mean"),
    Max_Orders=("Order_Count", "max")
)
print(city_summary)

print("\nQ8: Category and VIP Pivot Table")
pivot = pd.pivot_table(
    df,
    values="Total_Spent",
    index="Category",
    columns="Is_VIP",
    aggfunc="sum"
)
print(pivot)

print("\nQ9: Top 5 Customers in Electronics and Clothing")
filtered = df[df["Category"].isin(["Electronics", "Clothing"])]
top_customers = filtered.nlargest(5, "Total_Spent")
print(top_customers)

print("\nQ10: VIP Order Count Comparison")
vip = df[df["Is_VIP"] == True]

karachi_avg = vip[vip["City"] == "Karachi"]["Order_Count"].mean()
lahore_avg = vip[vip["City"] == "Lahore"]["Order_Count"].mean()

print("Karachi Average:", karachi_avg)
print("Lahore Average:", lahore_avg)

print("\nQ11: Analytical Insights")

print("1. City with highest average spending:")
print(city_summary["Average_Spent"].idxmax())
print(city_summary["Average_Spent"].max())

print("2. Category with highest total revenue:")
print(pivot.sum(axis=1).idxmax())
print(pivot.sum(axis=1).max())

print("3. VIP city comparison:")
if karachi_avg > lahore_avg:
    print("Karachi VIP customers have a higher average order count.")
elif lahore_avg > karachi_avg:
    print("Lahore VIP customers have a higher average order count.")
else:
    print("Both cities have the same average order count.")

df.to_csv("cleaned_customers.csv", index=False)
