import random
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from parse_tweet import parse_tweet_text
from urllib.parse import quote

from export import export_to_csv
from check_data_dates import analyse_date_ranges
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MAX_ROLLS = 1000
OVERWRITE = True

BATCH_SIZE = 100
EXPORT_FILENAME = "tweets_output.csv"

STALE_SCROLL_THRESHOLD = 5

def scrape_tweet(username: str, start_date: datetime, end_date: datetime = None) -> list:
    if end_date:
        search_query = f"(from:{username}) until:{end_date.strftime('%Y-%m-%d')} since:{start_date.strftime('%Y-%m-%d')}"
        search_url = f"https://twitter.com/search?q={quote(search_query)}&src=typed_query&f=live"
    else:
        search_query = f"(from:{username}) since:{start_date.strftime('%Y-%m-%d')}"
        search_url = f"https://twitter.com/search?q={quote(search_query)}&src=typed_query&f=live"

    print(search_query)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, args=["--start-minimized"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 920, "height": 700},
            screen={"width": 920, "height": 700},
            is_mobile=False,
            device_scale_factor=1,
            has_touch=False
        )

        context.add_cookies([{
            "name": "auth_token",
            "value": AUTH_TOKEN,
            "domain": ".x.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax"
        }])

        page = context.new_page()
        page.goto(search_url, wait_until="load")

        page.wait_for_selector("[data-testid='tweet']")

        tweets_data = {}
        tweets_batch = []

        # done = False

        scrolls = 0
        stale_scrolls = 0
        last_total = 0

        while scrolls < MAX_ROLLS and stale_scrolls < STALE_SCROLL_THRESHOLD:
            if "rate limit" in page.content().lower():
                print("⚠️ Rate limited. Sleeping for 5 minutes.")
                time.sleep(300)
                continue  # or break depending on how you want to recover


            tweets = page.locator("[data-testid='tweet']")
            count = tweets.count()

            # Extract
            new_count = extract_tweets(count, tweets, tweets_data, start_date)

            # Add new tweets to batch
            new_ids = list(tweets_data)[-new_count:]
            for tweet_id in new_ids:
                tweets_batch.append(tweets_data[tweet_id])

            # 🧾 Export if batch is full
            if not OVERWRITE and len(tweets_batch) >= BATCH_SIZE:
                    export_to_csv(tweets_batch, filename=EXPORT_FILENAME, overwrite=False)
                    tweets_batch.clear()

            # Check if any new tweets appeared
            current_total = len(tweets_data)
            if current_total == last_total:
                stale_scrolls += 1
                print(f"⚠️ No new tweets found. Stale scrolls: {stale_scrolls}")
            else:
                stale_scrolls = 0  # Reset if new tweets found
                last_total = current_total

            # Scroll and wait
            page.mouse.wheel(0, random.randint(900, 2700))
            page.mouse.move(random.randint(400, 600), random.randint(300, 500))
            page.wait_for_timeout(random.randint(1000, 2000))
            scrolls += 1

            if (scrolls % 10 == 0):
                print(f"Scrolled {scrolls}/{MAX_ROLLS}. Total tweets: {len(tweets_data)}")

        # Final export if anything left
        if tweets_batch:
            if OVERWRITE:
                # When overwrite=True, export all tweets once (combine all batches)
                export_to_csv(list(tweets_data.values()), filename=EXPORT_FILENAME, overwrite=True)
            else:
                # When overwrite=False, export remaining batch incrementally
                export_to_csv(tweets_batch, filename=EXPORT_FILENAME, overwrite=False)

        print(f"✅ Scraped {len(tweets_data)} tweets.")
        browser.close()
        return list(tweets_data.values())
    
# @profile
def extract_tweets(count, tweets, tweets_data, cutoff_date):
    from datetime import timezone, timedelta

    tweet_metadata = tweets.page.eval_on_selector_all(
        "[data-testid='tweet']",
        """
        els => els.map(tweet => {
            const link = tweet.querySelector("a:has(time)");
            const id = link?.href?.split('/').pop();
            const time = tweet.querySelector("time")?.getAttribute("datetime");
            const text = tweet.querySelector("[data-testid='tweetText']")?.innerText || "";
            const photos = Array.from(tweet.querySelectorAll("[data-testid='tweetPhoto'] img"))
                                .map(img => img.src);
            return { id, time, text, photos };
        })
        """
    )

    new_tweet_count = 0

    for tweet in tweet_metadata[:count]:
        tweet_id = tweet.get("id")
        if not tweet_id:
            continue

        # 📆 Parse timestamp
        timestamp_str = tweet.get("time")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else None
        except:
            timestamp = None

        if not timestamp or timestamp < cutoff_date.replace(tzinfo=timezone.utc):
            continue

        # 🧠 Parse text
        parsed_text = parse_tweet_text(tweet.get("text", ""))

        # 📅 Adjust date if needed
        tweet_date = timestamp.date()
        if parsed_text.get("seen_yesterday"):
            tweet_date -= timedelta(days=1)
        date_str = tweet_date.strftime("%Y-%m-%d")

        # ➕ Store
        tweets_data[tweet_id] = {
            "id": tweet_id,
            "text": parsed_text,
            "photos": tweet.get("photos", []),
            "date": date_str
        }
        new_tweet_count += 1

    return new_tweet_count
  
if __name__ == "__main__":
    year = 2023
    while year < 2026:
        month = 7
        while month < 13:
            day = 1
            while day <= 30:
                end_year = year
                end_month = month
                end_day = day + 5
                # if at end of month, need to check if end of year too
                if end_day > 30:
                    end_month += 1
                    end_day = 1
                    if end_month > 12:
                        end_month = 1
                        end_year += 1
                    
                scraped_data = scrape_tweet(
                    username="LatestKruger",
                    start_date=datetime(year, month, day),#1, 6, 16, 21, 26
                    end_date=datetime(end_year, end_month, end_day)#6, 11, 21, 26, 31
                )
                day +=5
                sleep_time = random.randint(120, 180)
                print(f"going to sleep for {sleep_time} seconds")
                time.sleep(sleep_time)
            month += 1
            analyse_date_ranges()
        year += 1


    # scraped_data = scrape_tweet(
    #     username="LatestKruger",
    #     start_date=datetime(2025, 5, 31)
    # )