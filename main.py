from fastapi import FastAPI
from openai import OpenAI
import requests
import os

app = FastAPI()

openai_key = os.getenv("OPENAI_API_KEY")

client = None

if openai_key:
    client = OpenAI(api_key=openai_key)

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/macro")
async def macro():

    if client is None:
        return {
            "error": "OPENAI_API_KEY não configurada"
        }

    try:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista macro institucional."
                },
                {
                    "role": "user",
                    "content": "DXY forte, yields subindo, Nasdaq fraco."
                }
            ]
        )

        return {
            "analysis": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/risk")
async def risk():

    dxy = 104.5
    yields = 4.35
    vix = 22

    score = 0

    if dxy > 104:
        score -= 2

    if yields > 4.2:
        score -= 2

    if vix > 20:
        score -= 3

    regime = "RISK OFF" if score < 0 else "RISK ON"

    return {
        "regime": regime,
        "score": score
    }



@app.get("/usd")
async def usd():

    usd_score = 7

    return {
        "usd_score": usd_score
    }

@app.get("/gold")
async def gold():

    yields = 4.35
    dxy = 104.5

    gold_score = 0

    if yields > 4.2:
        gold_score -= 2

    if dxy > 104:
        gold_score -= 2

    bias = "BEARISH" if gold_score < 0 else "BULLISH"

    return {
        "gold_score": gold_score,
        "bias": bias
    }

@app.get("/jpy")
async def jpy():

    boj = "dovish"
    risk = "RISK OFF"

    jpy_score = 0

    if risk == "RISK OFF":
        jpy_score += 3

    if boj == "dovish":
        jpy_score -= 2

    bias = "BULLISH" if jpy_score > 0 else "BEARISH"

    return {
        "jpy_score": jpy_score,
        "bias": bias
    }

@app.get("/news")
async def news():

    headlines = [
        "Fed mantém postura hawkish",
        "Treasury yields sobem",
        "Mercado reduz apostas de corte"
    ]

    return {
        "headlines": headlines
    }

@app.get("/signal")
async def signal():

    usd_score = 7
    jpy_score = 1
    risk = "RISK OFF"

    signal = "BUY USDJPY"
    confidence = 8.5

    return {
        "signal": signal,
        "confidence": confidence,
        "risk": risk
    }

@app.get("/market")
async def market():


    api_key = os.getenv("TWELVEDATA_API_KEY")

    url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={api_key}"

    response = requests.get(url)

    return response.json()



@app.get("/dashboard")
async def dashboard():

    api_key = os.getenv("TWELVEDATA_API_KEY")

    symbols = {
        "gold": "XAU/USD",
        "usdjpy": "USD/JPY",
        "eurusd": "EUR/USD"
    }

    market_data = {}

    for name, symbol in symbols.items():

        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={api_key}"

        response = requests.get(url)

        data = response.json()

        market_data[name] = {
            "price": data.get("price")
        }

    return {
        "market": market_data,

        "macro": {
            "risk": "RISK OFF",
            "usd_bias": "BULLISH",
            "gold_bias": "BEARISH"
        },

        "signal": {
            "pair": "USDJPY",
            "direction": "BUY",
            "confidence": 8.5
        },

        "news": [
            "Fed mantém postura hawkish",
            "Treasury yields sobem"
        ]
    }



    