import aiohttp
import asyncio

url = "https://news-api14.p.rapidapi.com/v2/article/random"

headers = {
    "x-rapidapi-key": "76d07a0f17msh6f72cf6bdc2dae4p15e8fcjsnd051e8460010", 
    "x-rapidapi-host": "news-api14.p.rapidapi.com"
}

async def GetRandomNews(lang: str = "en"):

    url = "https://news-api14.p.rapidapi.com/v2/article/random"
    query = {"language":lang,"topic":"cybersec"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=query) as response:
            resJson = await response.json()

    res = {
        "title": resJson["data"]["title"],
        "url": resJson["data"]["url"],
        "date": resJson["data"]["date"],
        "publisher": resJson["data"]["publisher"]["name"]
    }
    
    return res

async def ListNews(keyword: str, lang: str = "en"):
    url = "https://news-api14.p.rapidapi.com/v2/search/articles"
    query = {"language": lang, "query": keyword, "limit": 5}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=query) as response:
            resJson = await response.json()
    
    res: list = []
    for news in resJson["data"]:
        article = {
            "title": news["title"],
            "url": news["url"],
            "date": news["date"],
            "publisher": news["publisher"]["name"]
        }
        res.append(article)
    
    return res

if __name__ == "__main__":
    randomNews = asyncio.run(GetRandomNews())
    print(randomNews)

    # listOfNews = asyncio.run(ListNews("data breach"))
    # print(listOfNews)