"""Example client for the FinBERT sentiment API.""" 
 
import requests 
 
def check_sentiment(text): 
    response = requests.post("http://localhost:8000/sentiment", json={"text": text}) 
    return response.json() 
 
if __name__ == "__main__": 
    result = check_sentiment("Company reports record quarterly profit") 
    print(result) 
