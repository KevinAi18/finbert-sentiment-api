 
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
 
## 2026-06-22 
### FinBERT Preprocessing Pipeline Notes 
- Financial text needs special preprocessing before tokenization 
- Numbers and percentages normalized to reduce vocabulary size 
- News headlines truncated to 512 tokens to fit BERT input 
- Sliding window approach handles long financial reports 
 
## 2026-06-25 
### FinBERT Deployment Notes 
- Model exported to ONNX format for faster CPU inference 
- Docker container packages API with all dependencies included 
- Gunicorn with multiple workers handles concurrent requests 
- Health check endpoint added for monitoring API uptime 
 
## 2026-06-27 
### Real Time News Sentiment Pipeline Notes 
- News API fetches live financial headlines for analysis 
- Each headline passed through FinBERT for sentiment scoring 
- Aggregated sentiment score computed per stock ticker symbol 
- Pipeline runs on schedule using cron job every 15 minutes 
