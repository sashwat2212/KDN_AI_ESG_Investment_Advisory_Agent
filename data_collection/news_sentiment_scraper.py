import time
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


nltk.download("vader_lexicon") #for sentiment analysis
sia = SentimentIntensityAnalyzer()

#setting up the chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

#start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)["compound"]
    sentiment_label = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
    return sentiment_score, sentiment_label


def scrape_google_finance(query):
    print("Scraping Google Finance...")
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.find_all("div", class_="SoaBEf")
    news_data = []
    for article in articles[:10000]:
        try:
            headline = article.find("div", class_="nDgy9d").text.strip()
            link = article.find("a")["href"]
            sentiment_score, sentiment_label = analyze_sentiment(headline)
            news_data.append({
                "Source": "Google Finance",
                "Headline": headline,
                "Link": link,
                "Sentiment Score": sentiment_score,
                "Sentiment Label": sentiment_label
            })
        except Exception as e:
            print(f"Error scraping Google Finance article: {e}")
            continue
    print(f"Extracted {len(news_data)} news articles from Google Finance.")
    return news_data


def scrape_yahoo_finance():    
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    headers = {"User-Agent": user_agent}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch Yahoo Finance data. Status Code:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("h3")
    
    news_data = []
    for article in articles[:10000]:
        try:
            headline = article.text.strip()
            link_tag = article.find("a")
            if link_tag and "href" in link_tag.attrs:
                link = "https://finance.yahoo.com" + link_tag["href"]
                sentiment_score, sentiment_label = analyze_sentiment(headline)
                news_data.append({
                    "Source": "Yahoo Finance",
                    "Headline": headline,
                    "Link": link,
                    "Sentiment Score": sentiment_score,
                    "Sentiment Label": sentiment_label
                })
        except Exception as e:
            print(f"Error extracting Yahoo article: {e}")
            continue
    return news_data


def scrape_cnbc():    
    url = "https://www.cnbc.com/sustainable-future/"
    headers = {"User-Agent": user_agent}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch CNBC data. Status Code:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="Card-titleContainer")
    
    news_data = []
    for article in articles[:10000]:
        try:
            headline = article.text.strip()
            link_tag = article.find("a")
            if link_tag and "href" in link_tag.attrs:
                link = link_tag["href"]
                sentiment_score, sentiment_label = analyze_sentiment(headline)
                news_data.append({
                    "Source": "CNBC",
                    "Headline": headline,
                    "Link": link,
                    "Sentiment Score": sentiment_score,
                    "Sentiment Label": sentiment_label
                })
        except Exception as e:
            print(f"Error extracting CNBC article: {e}")
            continue
    return news_data


def scrape_morningstar():
    print("Scraping Morningstar...")
    url = "https://www.morningstar.com/lp/sustainable-investing"
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch Morningstar data. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("h2")  #headlines in <h2> tags

    news_data = []
    for article in articles[:10000]: 
        try:
            headline = article.text.strip()
            link_tag = article.find("a", href=True)
            link = f"https://www.morningstar.com{link_tag['href']}" if link_tag else "N/A"
            sentiment_score, sentiment_label = analyze_sentiment(headline)

            news_data.append({
                "Source": "Morningstar",
                "Headline": headline,
                "Link": link,
                "Sentiment Score": sentiment_score,
                "Sentiment Label": sentiment_label
            })
        except Exception as e:
            print(f"Error extracting Morningstar article: {e}")
            continue

    print(f"Extracted {len(news_data)} articles from Morningstar.")
    return news_data


def scrape_climate_home_news():
    url = "https://www.climatechangenews.com/"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    headers = {"User-Agent": user_agent}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch Climate Home News data. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    
    articles = soup.find_all("img", class_="wp-post-image")
    
    news_data = []
    for article in articles[:10000]:  
        try:
            headline = article["alt"].strip()
            link_tag = article.find_parent("a")  #find the link wrapping the image
            link = link_tag["href"] if link_tag else "No Link Found"
            
            if headline:
                news_data.append({
                    "Source": "Climate Home News",
                    "Headline": headline,
                    "Link": link
                })
        except Exception as e:
            print(f"Error extracting Climate Home News article: {e}")
            continue

    print(f"Extracted {len(news_data)} articles from Climate Home News.")
    return news_data


def save_to_csv(data, filename="esg_news_sentiment.csv"):
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"News sentiment data saved to '{filename}'.")

#run Scraping
query = "ESG investments"
google_news = scrape_google_finance(query)
yahoo_news = scrape_yahoo_finance()
cnbc_news = scrape_cnbc()
morningstar_news = scrape_morningstar()
climate_home_news = scrape_climate_home_news()



all_news = google_news + yahoo_news + cnbc_news + morningstar_news + climate_home_news
if all_news:
    save_to_csv(all_news)


driver.quit()
print("Scraping process completed!!!!!!!!!!!!!")

