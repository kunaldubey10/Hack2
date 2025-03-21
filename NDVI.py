import ee
import geemap
import pandas as pd
import matplotlib.pyplot as plt
ee.Authenticate()

# Initialize Earth Engine
ee.Initialize(project="double-lore-430306-n1")

# Define location (Your farm's coordinates)
latitude, longitude = 25.280112, 87.286792
point = ee.Geometry.Point([longitude, latitude])

# Function to check if images exist
def check_images_available(start_date, end_date):
    dataset = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterBounds(point)
        .filterDate(start_date, end_date)
    )
    return dataset.size().getInfo()  # Get number of images

# Function to mask clouds
def mask_clouds(image):
    cloud_mask = (
        image.select("MSK_CLASSI_OPAQUE").eq(0)
        .And(image.select("MSK_CLASSI_CIRRUS").eq(0))
    )
    return image.updateMask(cloud_mask)

# Function to compute NDVI with error handling
def get_ndvi_image(start_date, end_date):
    dataset = (
        ee.ImageCollection("COPERNICUS/S2")
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .map(mask_clouds)
    )

    # Check if dataset is empty
    image_count = dataset.size().getInfo()
    if image_count == 0:
        print(f"⚠️ No available images between {start_date} and {end_date}")
        return None

    # Compute median only if images are available
    median_image = dataset.median()
    ndvi = median_image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=30
    ).get("NDVI").getInfo()  # Extract NDVI value

# Define time intervals
dates = [
    ("2024-11-01", "2024-11-15"),
    ("2024-11-16", "2024-11-30"),
    ("2024-12-01", "2024-12-15"),
    ("2024-12-16", "2024-12-31"),
    ("2025-01-01", "2025-01-15"),
    ("2025-01-16", "2025-01-31"),
    ("2025-02-01", "2025-02-15"),
    ("2025-02-16", "2025-02-28")
]

# Compute NDVI values and compare past vs present
ndvi_values = []
date_labels = []
past_ndvi_value = None

for start, end in dates:
    if check_images_available(start, end) > 0:
        ndvi_value = get_ndvi_image(start, end)
        if ndvi_value is not None:
            date_labels.append(end)
            ndvi_values.append(ndvi_value)

            # Compare past vs present NDVI
            if past_ndvi_value is not None:
                ndvi_change = ndvi_value - past_ndvi_value
                print(f"📅 Date: {end}")
                print(f"   🌱 NDVI Value: {ndvi_value:.4f}")
                print(f"   🔄 NDVI Change: {ndvi_change:.4f}")

                if ndvi_change < -0.1:
                    print("   ⚠️ Warning: NDVI is decreasing! Possible disease or stress detected.\n")
                else:
                    print("   ✅ NDVI is stable, no major risk detected.\n")

            # Update past NDVI for next comparison
            past_ndvi_value = ndvi_value

# Convert to DataFrame for visualization
if len(ndvi_values) > 0:
    df = pd.DataFrame({"Date": date_labels, "NDVI": ndvi_values})
    df["Date"] = pd.to_datetime(df["Date"])

    # Plot NDVI trend
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["NDVI"], marker="o", linestyle="-", color="green", label="NDVI")
    plt.axhline(y=0.3, color='red', linestyle='--', label="Threshold (0.3)")
    plt.xlabel("Date")
    plt.ylabel("NDVI Value")
    plt.title("NDVI Trend (Nov 2024 - Mar 2025) with Cloud Masking")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Highlight critical NDVI drops
    for i in range(1, len(df)):
        if df["NDVI"][i] - df["NDVI"][i-1] < -0.1:
            plt.scatter(df["Date"][i], df["NDVI"][i], color='red', label="⚠️ Significant Drop")

    plt.show()
else:
    print("No valid NDVI data available for the selected period.")
