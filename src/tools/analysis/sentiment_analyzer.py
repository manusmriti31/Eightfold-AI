"""Sentiment analysis tool."""

from typing import Dict, Any, List, Literal


class SentimentAnalyzer:
    """Simple sentiment analyzer for text."""
    
    # Positive and negative word lists (simplified)
    POSITIVE_WORDS = {
        'excellent', 'great', 'good', 'positive', 'success', 'growth',
        'strong', 'innovative', 'leading', 'profitable', 'expanding',
        'opportunity', 'advantage', 'improvement', 'achievement', 'win'
    }
    
    NEGATIVE_WORDS = {
        'bad', 'poor', 'negative', 'failure', 'decline', 'weak',
        'loss', 'problem', 'issue', 'concern', 'risk', 'threat',
        'controversy', 'lawsuit', 'scandal', 'layoff', 'bankruptcy'
    }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = "Neutral"
            score = 0.0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.2:
                sentiment = "Positive"
            elif score < -0.2:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": positive_count,
            "negative_count": negative_count
        }
    
    def analyze_batch(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze sentiment of multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Aggregated sentiment analysis
        """
        results = [self.analyze(text) for text in texts]
        
        sentiments = [r["sentiment"] for r in results]
        avg_score = sum(r["score"] for r in results) / len(results) if results else 0
        
        return {
            "overall_sentiment": self._determine_overall(sentiments),
            "average_score": avg_score,
            "positive_count": sum(1 for s in sentiments if s == "Positive"),
            "negative_count": sum(1 for s in sentiments if s == "Negative"),
            "neutral_count": sum(1 for s in sentiments if s == "Neutral"),
            "total_analyzed": len(texts)
        }
    
    def _determine_overall(
        self,
        sentiments: List[str]
    ) -> Literal["Positive", "Negative", "Neutral", "Mixed"]:
        """Determine overall sentiment from list.
        
        Args:
            sentiments: List of sentiment labels
            
        Returns:
            Overall sentiment
        """
        if not sentiments:
            return "Neutral"
        
        pos = sentiments.count("Positive")
        neg = sentiments.count("Negative")
        neu = sentiments.count("Neutral")
        
        total = len(sentiments)
        
        if pos > total * 0.6:
            return "Positive"
        elif neg > total * 0.6:
            return "Negative"
        elif neu > total * 0.6:
            return "Neutral"
        else:
            return "Mixed"
