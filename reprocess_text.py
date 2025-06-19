import pandas as pd
from parse_tweet import parse_tweet_text

def reprocess_all_raw_text(filename="tweets_output.csv"):
    try:
        df = pd.read_csv(filename)
        if "text_raw" not in df.columns:
            print("❌ Column 'text_raw' not found in the CSV.")
            return

        df['id'] = df['id'].astype(str).str.strip()

        print(f"🔁 Reprocessing {len(df)} rows...")

        for idx in df.index:
            raw_text = df.at[idx, "text_raw"]
            if pd.isna(raw_text) or not str(raw_text).strip():
                continue

            parsed = parse_tweet_text(str(raw_text))
            if not parsed or not isinstance(parsed, dict):
              continue

            # Update text fields
            df.at[idx, "text_time"] = parsed.get("time")
            df.at[idx, "text_raw_descr"] = parsed.get("raw_descr")
            df.at[idx, "text_info"] = parsed.get("info")
            df.at[idx, "text_area"] = parsed.get("area")
            df.at[idx, "text_rating"] = float(parsed.get("rating")) if parsed.get("rating") else None
            df.at[idx, "text_author"] = parsed.get("author")

            # Update description fields
            descr = parsed.get("descr") or {}
            df.at[idx, "descr_value"] = descr.get("value")
            df.at[idx, "descr_quantity"] = descr.get("quantity")
            df.at[idx, "descr_species"] = descr.get("species")
            df.at[idx, "descr_activity"] = descr.get("activity")
            df.at[idx, "descr_unknown"] = ", ".join(descr.get("unknown", []))

            # Update location fields
            loc = parsed.get("location") or {}
            df.at[idx, "location_original"] = loc.get("original")
            df.at[idx, "location_main_road"] = loc.get("main_road")
            df.at[idx, "location_distance"] = loc.get("distance")
            df.at[idx, "location_direction"] = loc.get("direction")
            df.at[idx, "location_proximity_type"] = loc.get("proximity_type")
            df.at[idx, "location_reference_point"] = loc.get("reference_point")
            df.at[idx, "location_at"] = loc.get("at")

            if (parsed and parsed.get("area") == "Stara"):
                print("STARA VALUE", parsed)

        # Save changes
        df.to_csv(filename, index=False)
        print(f"✅ Reprocessed and saved {len(df)} records to {filename}.")

    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
    except Exception as e:
        print(f"⚠️ Error while reprocessing: {e}")


if __name__ == "__main__":
    reprocess_all_raw_text()
