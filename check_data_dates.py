import pandas as pd

def analyse_date_ranges(filename="tweets_output.xlsx", sheet_name="scraped_data"):
    try:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if "date" not in df.columns:
            print("❌ 'date' column not found in the Excel file.")
            return

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        valid_dates = df["date"].dropna().dt.date.unique()
        valid_dates = sorted(valid_dates)

        if not valid_dates:
            print("❌ No valid dates found.")
            return

        # Identify date ranges by checking for gaps
        ranges = []
        range_start = valid_dates[0]
        prev_date = valid_dates[0]

        for current in valid_dates[1:]:
            if (current - prev_date).days > 1:
                # Gap detected
                ranges.append((range_start, prev_date))
                range_start = current
            prev_date = current

        # Add final range
        ranges.append((range_start, prev_date))

        print(f"📅 Found {len(ranges)} continuous date range(s):\n")
        for start, end in ranges:
            if start == end:
                print(f"• {start}")
            else:
                print(f"• {start} → {end}")

    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
    except Exception as e:
        print(f"⚠️ Error while analyzing dates: {e}")


if __name__ == "__main__":
    analyse_date_ranges()
