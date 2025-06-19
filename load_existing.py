import pandas as pd

def load_existing_ids(excel_path: str, id_column: str = "id") -> set:
    try:
        df = pd.read_excel(excel_path)
        return set(df[id_column].dropna().astype(str))
    except Exception as e:
        print(f"Error loading existing IDs: {e}")
        return set()
