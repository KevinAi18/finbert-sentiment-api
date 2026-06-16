 
## 2026-06-18 
### FinBERT Sentiment Analysis Notes 
- FinBERT is BERT model fine-tuned on financial news corpus 
- Classifies text as positive, negative or neutral sentiment 
- Used for stock market sentiment analysis from news headlines 
- FastAPI wraps FinBERT model as REST API for real-time inference 
 
## 2026-06-20 
### FinBERT API Optimization Notes 
- Model loaded once at startup to avoid reload on each request 
- Tokenizer max length set to 512 to match BERT architecture 
- Batch inference processes multiple texts in single forward pass 
- Redis cache stores repeated query results for faster response 
