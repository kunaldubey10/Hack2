import ee
import pandas as pd
import matplotlib.pyplot as plt

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project="double-lore-430306-n1")

# Function to fetch NDVI for given coordinates
def get_ndvi_analysis(latitude, longitude):
    point = ee.Geometry.Point([longitude, latitude])

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

    ndvi_values = []
    date_labels = []
    past_ndvi_value = None
    results = []

    # Function to check if images exist
    def check_images_available(start_date, end_date):
        dataset = ee.ImageCollection("COPERNICUS/S2").filterBounds(point).filterDate(start_date, end_date)
        return dataset.size().getInfo()

    # Function to compute NDVI
    def get_ndvi_image(start_date, end_date):
        dataset = (
            ee.ImageCollection("COPERNICUS/S2")
            .filterBounds(point)
            .filterDate(start_date, end_date)
        )

        if dataset.size().getInfo() == 0:
            return None  # No images found

        median_image = dataset.median()
        ndvi = median_image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        return ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=30
        ).get("NDVI").getInfo()

    # Compute NDVI values for the given location
    for start, end in dates:
        if check_images_available(start, end) > 0:
            ndvi_value = get_ndvi_image(start, end)
            if ndvi_value is not None:
                date_labels.append(end)
                ndvi_values.append(ndvi_value)

                # Compare past vs present NDVI
                if past_ndvi_value is not None:
                    ndvi_change = ndvi_value - past_ndvi_value
                    result = f"📅 Date: {end}\n🌱 NDVI Value: {ndvi_value:.4f}\n🔄 NDVI Change: {ndvi_change:.4f}"

                    if ndvi_change < -0.1:
                        result += "\n⚠️ Warning: NDVI is decreasing! Possible disease or stress detected.\n"
                    else:
                        result += "\n✅ NDVI is stable, no major risk detected.\n"

                    results.append(result)

                past_ndvi_value = ndvi_value  # Update for next comparison

    # Create a DataFrame for visualization
    if len(ndvi_values) > 0:
        df = pd.DataFrame({"Date": date_labels, "NDVI": ndvi_values})
        df["Date"] = pd.to_datetime(df["Date"])

        # Plot NDVI trend
        plt.figure(figsize=(10, 5))
        plt.plot(df["Date"], df["NDVI"], marker="o", linestyle="-", color="green", label="NDVI")
        plt.axhline(y=0.3, color='red', linestyle='--', label="Threshold (0.3)")
        plt.xlabel("Date")
        plt.ylabel("NDVI Value")
        plt.title(f"NDVI Trend for ({latitude}, {longitude})")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)

        # Highlight critical NDVI drops
        for i in range(1, len(df)):
            if df["NDVI"][i] - df["NDVI"][i-1] < -0.1:
                plt.scatter(df["Date"][i], df["NDVI"][i], color='red', label="⚠️ Significant Drop")

        plt.show()

    return results
