"""Fact checking and verification tool."""

from typing import Dict, Any, List, Tuple
from difflib import SequenceMatcher


class FactChecker:
    """Tool for cross-checking facts across multiple sources."""
    
    def __init__(self, similarity_threshold: float = 0.7):
        """Initialize fact checker.
        
        Args:
            similarity_threshold: Minimum similarity to consider facts matching
        """
        self.similarity_threshold = similarity_threshold
    
    def check_consistency(
        self,
        fact_sets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Check consistency across multiple fact sets.
        
        Args:
            fact_sets: List of fact dictionaries from different sources
            
        Returns:
            Consistency analysis
        """
        contradictions = []
        verified_facts = []
        
        # Compare each field across sources
        all_keys = set()
        for fact_set in fact_sets:
            all_keys.update(fact_set.keys())
        
        for key in all_keys:
            values = []
            sources = []
            
            for i, fact_set in enumerate(fact_sets):
                if key in fact_set and fact_set[key] is not None:
                    values.append(fact_set[key])
                    sources.append(f"Source {i+1}")
            
            if len(values) > 1:
                # Check if values are consistent
                if self._are_values_consistent(values):
                    verified_facts.append({
                        "field": key,
                        "value": values[0],
                        "sources": sources,
                        "confidence": "High"
                    })
                else:
                    contradictions.append({
                        "field": key,
                        "values": values,
                        "sources": sources
                    })
        
        return {
            "contradictions": contradictions,
            "verified_facts": verified_facts,
            "consistency_score": self._calculate_consistency_score(
                len(verified_facts),
                len(contradictions)
            )
        }
    
    def _are_values_consistent(self, values: List[Any]) -> bool:
        """Check if values are consistent.
        
        Args:
            values: List of values to compare
            
        Returns:
            True if consistent
        """
        if not values:
            return True
        
        # For numbers, check if within 10% range
        if all(isinstance(v, (int, float)) for v in values):
            min_val = min(values)
            max_val = max(values)
            if min_val == 0:
                return max_val == 0
            return (max_val - min_val) / min_val <= 0.1
        
        # For strings, check similarity
        if all(isinstance(v, str) for v in values):
            first = values[0].lower()
            return all(
                self._string_similarity(first, str(v).lower()) >= self.similarity_threshold
                for v in values[1:]
            )
        
        # For other types, check exact equality
        return all(v == values[0] for v in values[1:])
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score (0-1)
        """
        return SequenceMatcher(None, str1, str2).ratio()
    
    def _calculate_consistency_score(
        self,
        verified_count: int,
        contradiction_count: int
    ) -> float:
        """Calculate overall consistency score.
        
        Args:
            verified_count: Number of verified facts
            contradiction_count: Number of contradictions
            
        Returns:
            Consistency score (0-1)
        """
        total = verified_count + contradiction_count
        if total == 0:
            return 1.0
        return verified_count / total
    
    def identify_outliers(
        self,
        values: List[float],
        threshold: float = 2.0
    ) -> List[int]:
        """Identify outlier values using standard deviation.
        
        Args:
            values: List of numeric values
            threshold: Number of standard deviations for outlier
            
        Returns:
            Indices of outlier values
        """
        if len(values) < 3:
            return []
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        outliers = []
        for i, value in enumerate(values):
            if abs(value - mean) > threshold * std_dev:
                outliers.append(i)
        
        return outliers
