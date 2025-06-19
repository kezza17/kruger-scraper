import os
import pandas as pd

def export_to_csv(tweets_data, filename="tweets_output.csv", overwrite=True):
    try:
        flattened = []

        for tweet in tweets_data:
            flat = {
                "id": tweet.get("id"),
                "date": tweet.get("date"),
            }

            text = tweet.get("text", {})
            if text:
                flat["text_raw"] = text.get("raw")
                flat["text_time"] = text.get("time")
                flat["text_raw_descr"] = text.get("raw_descr")
                flat["text_info"] = text.get("info")
                flat["text_area"] = text.get("area")
                flat["text_rating"] = text.get("rating")
                flat["text_author"] = text.get("author")

            descr = text.get("descr", {})
            if descr:
                flat["descr_value"] = descr.get("value")
                flat["descr_quantity"] = descr.get("quantity")
                flat["descr_species"] = descr.get("species")
                flat["descr_activity"] = descr.get("activity")
                flat["descr_unknown"] = ", ".join(descr.get("unknown", []))

            location = text.get("location", {})
            if location:
                flat["location_original"] = location.get("original")
                flat["location_main_road"] = location.get("main_road")
                flat["location_distance"] = location.get("distance")
                flat["location_direction"] = location.get("direction")
                flat["location_proximity_type"] = location.get("proximity_type")
                flat["location_reference_point"] = location.get("reference_point")
                flat["location_at"] = location.get("at")

            flat["photos"] = ", ".join(tweet.get("photos", []))
            flattened.append(flat)

        new_df = pd.DataFrame(flattened)
        new_df['id'] = new_df['id'].astype(str).str.strip()

        if os.path.exists(filename):
            try:
                existing_df = pd.read_csv(filename)
                existing_df['id'] = existing_df['id'].astype(str).str.strip()

                if overwrite:
                    existing_df.set_index("id", inplace=True)
                    new_df.set_index("id", inplace=True)
                    existing_df.update(new_df)
                    combined_df = pd.concat([
                        existing_df,
                        new_df[~new_df.index.isin(existing_df.index)]
                    ])
                    combined_df.reset_index(inplace=True)
                    print(f"🔁 Updated {filename} with {len(new_df)} records (by ID).")
                else:
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                    combined_df.drop_duplicates(subset="id", keep="last", inplace=True)
                    print(f"➕ Appended {len(new_df)} records to {filename} (deduplicated).")

            except Exception as e:
                print(f"⚠️ Failed to read or update existing CSV file: {e}")
                combined_df = new_df
        else:
            combined_df = new_df
            print(f"🆕 Created new file {filename} with {len(new_df)} records.")

        # 🔄 Write final result
        combined_df.to_csv(filename, index=False)
        print(f"✅ Exported to {filename}")

    except PermissionError:
        print(f"❌ File '{filename}' is open. Please close it and try again.")
