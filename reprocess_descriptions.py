import pandas as pd
from openpyxl import load_workbook
from parse_tweet import extract_description_fields

def reprocess_unknown_descriptions(filename="tweets_output.xlsx"):
    sheet_name = "scraped_data"

    try:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if "descr_unknown" not in df.columns or "text_raw_descr" not in df.columns:
            print("❌ Required columns not found in the Excel file.")
            return

        df['id'] = df['id'].astype(str).str.strip()

        # Filter rows where `descr_unknown` is not empty
        mask = df['descr_unknown'].fillna("").str.strip() != ""
        affected_rows = df[mask]
        print(f"🔍 Found {len(affected_rows)} rows with unknown descriptions. Reprocessing...")

        for idx in affected_rows.index:
            raw_descr = df.at[idx, 'text_raw_descr']
            if pd.isna(raw_descr) or not raw_descr.strip():
                continue

            parsed = extract_description_fields(raw_descr)
            df.at[idx, "descr_value"] = parsed.get("value")
            df.at[idx, "descr_quantity"] = parsed.get("quantity")
            df.at[idx, "descr_species"] = parsed.get("species")
            df.at[idx, "descr_activity"] = parsed.get("activity")
            df.at[idx, "descr_unknown"] = ", ".join(parsed.get("unknown", []))

        # ✅ Preserve other sheets when saving
        with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"✅ Updated {filename} with reprocessed description fields (only '{sheet_name}' updated).")

    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
    except Exception as e:
        print(f"⚠️ Error during processing: {e}")


if __name__ == "__main__":
    reprocess_unknown_descriptions()
