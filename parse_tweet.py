import re
from parse_location import parse_location
from parse_description import extract_description_fields

def parse_tweet_text(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    result = {
        "raw": text,
        "seen_yesterday": False,
        "time": None,
        "raw_descr": None,
        "descr": None,
        "info": None,
        "location": None,
        "area": None,
        "rating": None,
        "author": None,
    }

    # Detect and remove "Seen Yesterday" prefix
    if len(lines) > 3:

      if lines and lines[0].lower() in ["yesterday", "seen yesterday"]:
          result["seen_yesterday"] = True
          lines = lines[1:]

      for line in lines:
          # Time
          if result["time"] is None and re.match(r"^\d{1,2}:\d{2}(am|amm|a|pm)$", line.lower()):
              result["time"] = line
              continue

          # Quoted Info
          if result["info"] is None and line.startswith('"') and line.endswith('"'):
              result["info"] = line.strip('"')
              continue

          # Location (assume line with comma is the location line)
          if result["location"] is None and ',' in line:
              result["location"] = parse_location(line)
              continue

          # Area (starts with "Near")
          if result["area"] is None and line.lower().startswith("near "):
              result["area"] = line[5:].strip()
              continue

          # Rating (e.g. 4/5)
          if result["rating"] is None and re.match(r"^\d+/5$", line):
              result["rating"] = line.split("/")[0]
              continue

          # Author (e.g. Tinged by X)
          if result["author"] is None and line.lower().startswith("tinged by"):
              match = re.search(r"Tinged by (.+)", line, re.IGNORECASE)
              if match:
                  result["author"] = match.group(1).strip()
              continue

          # First unmatched line is likely the raw description
          if result["raw_descr"] is None:
              result["raw_descr"] = line
              result["descr"] = extract_description_fields(line)

    return result

