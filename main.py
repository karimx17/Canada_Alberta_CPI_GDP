import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# IF YOU ARE A RECRUITER AND ARE NOT FAMILIAR WITH PYTHON, SHOW THIS TO A SOFTWARE DEVELOPER AND THEY CAN RUN IT


                                    #------------------- CPI -------------------#
# READ FILE
data = pd.read_csv("consumer_price_index_csv_2022-01-20 (1).csv")

# CLEANING THE FILE
# print(data.isna().values.any())
# print(data.duplicated().values.any())

# REMOVING NAN VALUES
data.dropna(inplace=True)

# CHANGING STR FORMATTED DATE INTO TIMESERIES
data["REF_DATE"] = pd.to_datetime(data["REF_DATE"], format="%b-%y")


# SPLITTING DF INTO ALBERTA/CANADA
alberta_df = data[data["GEO"] == "Alberta"]
canada_df = data[data["GEO"] == "Canada"]

# GROUPING THE DATES AND AVERAGING THE CPI
alberta_average_cpi = alberta_df.groupby("REF_DATE", as_index=False).agg({"VALUE": pd.Series.mean})
canada_average_cpi = canada_df.groupby("REF_DATE", as_index=False).agg({"VALUE": pd.Series.mean})

# FUNCTION TO PLOT USING MATPLOTLIB
def plot_data(df, df2, y_axis, title, color, label, color2, label2):
    plt.figure(figsize=(12, 6))
    plt.title(title, fontsize=14)
    plt.ylabel("Average CPI", fontsize=14)
    plt.plot(
        df["REF_DATE"],
        df[y_axis],
        color=color,
        label=label,
        linewidth=2
    )
    plt.plot(
        df2["REF_DATE"],
        df2[y_axis],
        color=color2,
        label=label2,
        linewidth=2
    )
    plt.legend()
    plt.show()


plot_data(alberta_average_cpi, canada_average_cpi, "VALUE", "Alberta vs Canada Average CPI", "blue", "Alberta", "red", "Canada")


# PIE CHART SHOWING AVG CPI FROM YEAR 2008 - 2022 AS A PERCENTAGE OF TOTAL CPI
canada_product = canada_df.groupby("Products_and_product_groups", as_index=False).agg({"VALUE":pd.Series.mean})
alberta_product = alberta_df.groupby("Products_and_product_groups", as_index=False).agg({"VALUE":pd.Series.mean})

pie_chart = px.pie(
    canada_product,
    values="VALUE",
    names="Products_and_product_groups",
    hole=0.6,
    title="Canada Products CPI "
)
pie_chart.update_traces(textposition="outside", textinfo="percent+label")

pie_chart.show()

                                    #------------------- GDP -------------------#

# CLEANING DATA
gdp_data = pd.read_csv("real_GDP.csv")
gdp_data.dropna(inplace=True)

# FORMATTING DATETIME
gdp_data["REF_DATE"] = pd.to_datetime(gdp_data["REF_DATE"], format="%Y")

# REMOVING PERCENT SIGN AND CHANGING TO NUMERIC DATA TYPE
gdp_data["GDP Percentage Change (%)"] = gdp_data["GDP Percentage Change (%)"].astype(str).str.replace("%", "")
gdp_data["GDP Percentage Change (%)"] = pd.to_numeric(gdp_data["GDP Percentage Change (%)"])

# SEPARATING ALBERTA VS CANADA TO PLOT % CHANGE FOR BOTH
alberta_gdp = gdp_data[gdp_data["GEO"] == "Alberta"]
canada_gdp = gdp_data[gdp_data["GEO"] == "Canada"]

# PLOT FUNCTION USED AGAIN
plot_data(alberta_gdp, canada_gdp, "GDP Percentage Change (%)", "GDP % Change", "blue", "Alberta", "red", "Canada")


# ANOTHER WAY OF DOING THE SAME THING AS LINES 87 BUT WITH PLOTLY
fig = px.line(
    gdp_data,
    x="REF_DATE",
    y="GDP Percentage Change (%)",
    color="GEO",
    markers=True
)
fig.show()
