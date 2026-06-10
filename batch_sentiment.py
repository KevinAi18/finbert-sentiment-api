"""
Batch Sentiment Analysis Utility
Analyze multiple financial headlines at once and get aggregated insights.
Usage: python batch_sentiment.py --input headlines.json
"""
import json
import argparse
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class SentimentResult:
    headline: str
    positive: float
    negative: float
    neutral: float
    label: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "headline": self.headline,
            "positive": round(self.positive, 4),
            "negative": round(self.negative, 4),
            "neutral": round(self.neutral, 4),
            "label": self.label,
            "confidence": round(self.confidence, 4),
            "timestamp": self.timestamp
        }

def classify_label(positive: float, negative: float, neutral: float) -> tuple:
    scores = {"positive": positive, "negative": negative, "neutral": neutral}
    label = max(scores, key=scores.get)
    confidence = scores[label]
    return label, confidence

def aggregate_results(results: List[SentimentResult]) -> Dict:
    if not results:
        return {}
    total = len(results)
    positive_count = sum(1 for r in results if r.label == "positive")
    negative_count = sum(1 for r in results if r.label == "negative")
    neutral_count = sum(1 for r in results if r.label == "neutral")
    avg_positive = sum(r.positive for r in results) / total
    avg_negative = sum(r.negative for r in results) / total
    avg_neutral = sum(r.neutral for r in results) / total
    avg_confidence = sum(r.confidence for r in results) / total

    market_signal = "BULLISH" if positive_count > negative_count else "BEARISH" if negative_count > positive_count else "NEUTRAL"

    return {
        "total_headlines": total,
        "distribution": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        },
        "percentages": {
            "positive": round(positive_count / total * 100, 1),
            "negative": round(negative_count / total * 100, 1),
            "neutral": round(neutral_count / total * 100, 1)
        },
        "avg_scores": {
            "positive": round(avg_positive, 4),
            "negative": round(avg_negative, 4),
            "neutral": round(avg_neutral, 4)
        },
        "avg_confidence": round(avg_confidence, 4),
        "market_signal": market_signal
    }

def process_batch(headlines: List[str]) -> Dict:
    results = []
    for headline in headlines:
        # Simulate FinBERT predictions for demonstration
        # In production, call the actual API endpoint
        import requests
        try:
            response = requests.post(
                "http://0.0.0.0:5000/sentiment/",
                json={"headline": headline},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                label, confidence = classify_label(
                    data.get("Positive", 0),
                    data.get("Negative", 0),
                    data.get("Neutral", 0)
                )
                results.append(SentimentResult(
                    headline=headline,
                    positive=data.get("Positive", 0),
                    negative=data.get("Negative", 0),
                    neutral=data.get("Neutral", 0),
                    label=label,
                    confidence=confidence
                ))
        except Exception as e:
            print(f"Warning: Could not process '{headline[:50]}...': {e}")

    return {
        "results": [r.to_dict() for r in results],
        "aggregate": aggregate_results(results)
    }

def main():
    parser = argparse.ArgumentParser(description="Batch financial sentiment analysis")
    parser.add_argument("--input", help="JSON file with list of headlines")
    parser.add_argument("--output", help="Output JSON file", default="sentiment_report.json")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            headlines = json.load(f)
    else:
        headlines = [
            "Apple reports record quarterly earnings, beating analyst expectations",
            "Federal Reserve signals potential rate cuts amid inflation concerns",
            "Tesla stock plunges after missing delivery targets for third quarter",
            "Goldman Sachs upgrades Amazon to buy with $200 price target",
            "Oil prices surge as OPEC announces production cuts"
        ]

    print(f"Processing {len(headlines)} headlines...")
    report = process_batch(headlines)

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nAggregate Market Signal: {report['aggregate'].get('market_signal', 'N/A')}")
    print(f"Distribution: {report['aggregate'].get('distribution', {})}")
    print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
