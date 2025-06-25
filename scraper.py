import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_products(query, budget):
    url = f"https://www.flipkart.com/search?q={query}+under+{budget}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    products = []
    for item in soup.select("._1AtVbE"):
        name = item.select_one("._4rR01T") or item.select_one(".s1Q9rs")
        price = item.select_one("._30jeq3")
        rating = item.select_one("._3LWZlK")
        link = item.select_one("a")

        if name and price and link:
            try:
                clean_price = int(price.get_text().replace("₹", "").replace(",", ""))
                products.append({
                    "name": name.get_text(),
                    "price": clean_price,
                    "rating": rating.get_text() if rating else "NA",
                    "link": f"https://www.flipkart.com{link['href']}",
                    "features": name.get_text()
                })
            except:
                continue
    return products