import ee
import pandas as pd

#authenticate and initialize 
try:
    ee.Initialize(project='sashwat22')
except Exception as e:
    ee.Authenticate()
    ee.Initialize()


START_DATE = '2018-01-01'
END_DATE = '2024-01-01'


DATASETS = {
    "Deforestation": {
        "collection": ee.ImageCollection("MODIS/061/MOD44B"),
        "bands": ["Percent_Tree_Cover"],  
    },
    "Air Pollution (NO2)": {
        "collection": ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2"),
        "bands": ["tropospheric_NO2_column_number_density"],  
    },
    "Water Quality": {
        "collection": ee.ImageCollection("LANDSAT/LC08/C02/T1_L2"),
        "bands": ["SR_B3", "SR_B4", "SR_B5"],  
    },
}


region = ee.Geometry.Rectangle([-15, 35, 15, 60]) 


def fetch_time_series(dataset, bands):
    images = (
        dataset
        .filterBounds(region)
        .select(bands)
        .filterDate(START_DATE, END_DATE)
        .limit(3000)
    )

    def reduce_region(img):
        stats = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=2000,
            maxPixels=1e20
        )
        date = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd")
        
        properties = {"date": date}
        for band in bands:
            properties[band] = stats.get(band)
        
        return ee.Feature(None, properties)

    reduced = images.map(reduce_region).getInfo()

    if "features" not in reduced or len(reduced["features"]) == 0:
        return pd.DataFrame(columns=["Date"] + bands)

    try:
        dates = [f["properties"]["date"] for f in reduced["features"]]
        data = {band: [f["properties"].get(band, None) for f in reduced["features"]] for band in bands}
        df = pd.DataFrame({"Date": dates, **data})
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    except KeyError as e:
        return pd.DataFrame(columns=["Date"] + bands)


merged_df = pd.DataFrame()
for metric, info in DATASETS.items():
    df = fetch_time_series(info["collection"], info["bands"])  
    if not df.empty:
        df.rename(columns={band: f"{metric} ({band})" for band in info["bands"]}, inplace=True)
        if merged_df.empty:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="Date", how="outer")


merged_df.to_csv("Satellite_Complete_Data.csv", index=False)
print("Merged dataset saved as Satellite_Complete_Data.csv!")




# --------------------------------------------------------------------------------------



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Satellite_Complete_Data.csv")
df["Date"] = pd.to_datetime(df["Date"]) 
df.set_index("Date", inplace=True)


plt.figure(figsize=(12, 6))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Environmental Trends Over Time")
plt.legend()
plt.grid(True)
plt.show()


correlation_matrix = df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Environmental Factors")
plt.show()

#thresholds
safe_limits = {
    "Air Pollution (NO2)": 0.0002,  
    "Water Quality (SR_B3)": 0.1,   
    "Water Quality (SR_B4)": 0.1,
    "Water Quality (SR_B5)": 0.1,
}

alerts = []
for metric, limit in safe_limits.items():
    if metric in df.columns:
        exceeded_dates = df[df[metric] > limit].index.strftime("%Y-%m-%d").tolist()
        if exceeded_dates:
            alerts.append(f"⚠️ {metric} exceeded safe limits on: {', '.join(exceeded_dates[:5])}...")


if alerts:
    print("\n".join(alerts))
else:
    print("All values within safe limits!")

