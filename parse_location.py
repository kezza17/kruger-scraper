import re

def parse_location(location_text):
    result = {
        "original": location_text,
        "main_road": None,
        "distance": None,
        "direction": None,
        "proximity_type": None,
        "reference_point": None,
        "at": None
    }

    # Split at first comma
    parts = location_text.split(",", 1)
    result["main_road"] = parts[0].strip()

    if len(parts) == 1:
        return result

    right_part = parts[1].strip()
    right_lower = right_part.lower()

    # --- Distance extraction ---
    distance_match = re.search(r'\b(about\s+)?\d+(\.\d+)?\s*(km|m)\b', right_lower)
    if distance_match:
        result["distance"] = distance_match.group().strip()

    # --- Direction extraction ---
    direction_match = re.search(r'\b([NSEW]{1,2})\b', right_part.upper())
    if direction_match:
        result["direction"] = direction_match.group()

    # --- Proximity types ---
    proximity_types = [
        "but close to", "close to", "just", "about halfway between", "between",
        "just W of", "just E of", "just N of", "just S of",
        "near", "from", "of"
    ]
    at_used_separately = False
    proximity_found = None

    for pt in proximity_types:
        if pt.lower() in right_lower:
            proximity_found = pt
            break

    # Handle "at" special case
    if ' at ' in right_lower and proximity_found:
        # Only use `at` field if there's a separate proximity phrase
        before_at, after_at = re.split(r'\s+at\s+', right_part, maxsplit=1, flags=re.IGNORECASE)
        result["at"] = after_at.strip()
        reference = before_at.strip()
        at_used_separately = True
    else:
        reference = right_part

    # Map proximity types to clean versions
    proximity_map = {
        "but close to": "close to",
        "close to": "close to",
        "just": "just",
        "about halfway between": "between",
        "between": "between",
        "just w of": "of",
        "just e of": "of",
        "just n of": "of",
        "just s of": "of",
        "near": "near",
        "from": "from",
        "of": "of"
    }

    if proximity_found:
        result["proximity_type"] = proximity_map.get(proximity_found.lower(), proximity_found)

    # Remove proximity phrase
    if proximity_found:
        reference = re.sub(re.escape(proximity_found), '', reference, flags=re.IGNORECASE).strip()

    # Remove distance
    if result["distance"]:
        reference = re.sub(re.escape(result["distance"]), '', reference, flags=re.IGNORECASE).strip()

    # Remove direction
    if result["direction"]:
        reference = re.sub(r'\b' + re.escape(result["direction"]) + r'\b', '', reference, flags=re.IGNORECASE).strip()

    reference = re.sub(r'\s{2,}', ' ', reference).strip(", ")

    # If no other proximity term was used and "at" is the only indicator
    if not at_used_separately and ' at ' in right_lower and result["proximity_type"] is None:
        result["reference_point"] = reference
    elif reference:
        result["reference_point"] = reference

    return result