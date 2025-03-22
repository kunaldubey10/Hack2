# # import ee
# # import datetime
# # import pandas as pd
# # import matplotlib.pyplot as plt

# # # Authenticate and initialize Earth Engine
# # ee.Authenticate()
# # ee.Initialize(project="double-lore-430306-n1")

# # # Define location (Your farm's coordinates)
# # latitude, longitude = 25.280112, 87.286792
# # point = ee.Geometry.Point([longitude, latitude])

# # # Function to check if images exist for a given date range
# # def check_images_available(start_date, end_date):
# #     dataset = (
# #         ee.ImageCollection("COPERNICUS/S2_SR")
# #         .filterBounds(point)
# #         .filterDate(start_date, end_date)
# #     )
# #     return dataset.size().getInfo()  # Get number of images

# # # Function to apply cloud mask
# # def mask_clouds(image):
# #     scl = image.select("SCL")
# #     cloud_mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
# #     return image.updateMask(cloud_mask)

# # # Function to compute NDVI with enhanced error handling
# # def get_ndvi_image(start_date, end_date):
# #     dataset = (
# #         ee.ImageCollection("COPERNICUS/S2_SR")
# #         .filterBounds(point)
# #         .filterDate(start_date, end_date)
# #         .map(mask_clouds)
# #     )

# #     image_count = dataset.size().getInfo()

# #     if image_count == 0:
# #         print(f"⚠ No images found between {start_date} and {end_date}. Expanding search...")

# #         # Expand search range by 15 days
# #         new_start_date = (datetime.datetime.strptime(start_date, "%Y-%m-%d") - datetime.timedelta(days=15)).strftime("%Y-%m-%d")
# #         dataset = (
# #             ee.ImageCollection("COPERNICUS/S2_SR")
# #             .filterBounds(point)
# #             .filterDate(new_start_date, end_date)
# #             .map(mask_clouds)
# #         )

# #         image_count = dataset.size().getInfo()
# #         if image_count == 0:
# #             print("❌ No NDVI images found after expanding search. Returning default NDVI value.")
# #             return 0.2  # Default NDVI if no images found

# #     # Ensure dataset is not empty before reducing
# #     if image_count > 0:
# #         median_image = dataset.median()
# #         ndvi = median_image.normalizedDifference(["B8", "B4"]).rename("NDVI")

# #         ndvi_value = ndvi.reduceRegion(
# #             reducer=ee.Reducer.mean(),
# #             geometry=point,
# #             scale=30
# #         ).get("NDVI").getInfo()

# #         if ndvi_value is None:
# #             print("⚠ NDVI computation failed. Returning default value.")
# #             return 0.2  # Default NDVI if computation fails

# #         return round(ndvi_value, 4)

# #     return 0.2  # Final fallback in case of unexpected errors

# # # Define time intervals (Updated to September 2024 - December 2024)
# # dates = [
# #     ("2024-09-01", "2024-09-15"),
# #     ("2024-09-16", "2024-09-30"),
# #     ("2024-10-01", "2024-10-15"),
# #     ("2024-10-16", "2024-10-31"),
# #     ("2024-11-01", "2024-11-15"),
# #     ("2024-11-16", "2024-11-30"),
# #     ("2024-12-01", "2024-12-15"),
# #     ("2024-12-16", "2024-12-31")
# # ]

# # # Compute NDVI values and compare past vs present
# # ndvi_values = []
# # date_labels = []
# # past_ndvi_value = None

# # threshold = 0.2  # Adjusted NDVI threshold

# # for start, end in dates:
# #     if check_images_available(start, end) > 0:
# #         ndvi_value = get_ndvi_image(start, end)
# #         if ndvi_value is not None:
# #             date_labels.append(end)
# #             ndvi_values.append(ndvi_value)
# #             print(f"📅 {end} → NDVI: {ndvi_value:.4f}")

# #             # Compare past vs present NDVI
# #             if past_ndvi_value is not None:
# #                 ndvi_change = ndvi_value - past_ndvi_value
# #                 print(f"   🔄 NDVI Change: {ndvi_change:.4f}")

# #                 if ndvi_change < -0.1:
# #                     print("   ⚠ Warning: NDVI is decreasing! Possible disease or stress detected.\n")
# #                 else:
# #                     print("   ✅ NDVI is stable, no major risk detected.\n")

# #             past_ndvi_value = ndvi_value

# # # Convert to DataFrame for visualization
# # if len(ndvi_values) > 0:
# #     df = pd.DataFrame({"Date": date_labels, "NDVI": ndvi_values})
# #     df["Date"] = pd.to_datetime(df["Date"])

# #     # Calculate Precision (Std Dev) and Accuracy
# #     ndvi_std_dev = df["NDVI"].std()
# #     ndvi_accuracy = (df["NDVI"] > threshold).mean() * 100  # Percentage above 0.2

# #     print(f"\n📊 NDVI Precision (Std Dev): {ndvi_std_dev:.4f}")
# #     print(f"🎯 NDVI Accuracy (Above Threshold {threshold}): {ndvi_accuracy:.2f}%")

# #     # Plot NDVI trend
# #     plt.figure(figsize=(10, 5))
# #     plt.plot(df["Date"], df["NDVI"], marker="o", linestyle="-", color="green", label="NDVI")
# #     plt.axhline(y=threshold, color='red', linestyle='--', label=f"Threshold ({threshold})")
# #     plt.xlabel("Date")
# #     plt.ylabel("NDVI Value")
# #     plt.title("NDVI Trend (Sep 2024 - Dec 2024) with Cloud Masking")
# #     plt.xticks(rotation=45)
# #     plt.legend()
# #     plt.grid(True)

# #     # Highlight critical NDVI drops
# #     for i in range(1, len(df)):
# #         if df["NDVI"][i] - df["NDVI"][i-1] < -0.1:
# #             plt.scatter(df["Date"][i], df["NDVI"][i], color='red', label="⚠ Significant Drop")

# #     # Save the plot
# #     plt.savefig("ndvi_plot.png")
# #     print("📌 NDVI plot saved as 'ndvi_plot.png'.")
# #     plt.show()
# # else:
# #     print("No valid NDVI data available for the selected period.")


# import ee

# # 🌍 Initialize Google Earth Engine
# ee.Initialize()

# # 📡 Function to Fetch NDVI Data (Restrict Date)
# def get_ndvi_value(start_date, end_date):
#     try:
#         # Restrict NDVI fetching to **only till December 31, 2024**
#         max_allowed_date = "2024-12-31"

#         # If the requested date is beyond Dec 31, 2024, return None
#         if start_date > max_allowed_date:
#             print("⚠️ NDVI data fetching stopped at December 2024.")
#             return None

#         # Load Sentinel-2 Data
#         collection = (
#             ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
#             .filterDate(start_date, min(end_date, max_allowed_date))  # Restrict end date
#             .filterBounds(ee.Geometry.Point(87.286792, 25.280112))
#             .map(lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI"))
#         )

#         # Compute Mean NDVI Value
#         ndvi_mean = collection.mean().reduceRegion(
#             reducer=ee.Reducer.mean(),
#             geometry=ee.Geometry.Point(87.286792, 25.280112),
#             scale=30
#         ).get("NDVI").getInfo()

#         return ndvi_mean if ndvi_mean is not None else 0.0  # Return 0 if no data found

#     except Exception as e:
#         print(f"⚠️ Error fetching NDVI data: {e}")
#         return None  # Return None in case of error
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
