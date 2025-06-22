import json
import os
from typing import Dict, List, Any
from collections import Counter

class BeerAnalyzer:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
    
    def load_data(self) -> List[Dict[str, Any]]:
        """Load all beer data from JSON files"""
        all_beers = []
        if not os.path.exists(self.data_dir):
            return all_beers
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.data_dir, filename), 'r') as f:
                    beers = json.load(f)
                    all_beers.extend(beers)
        return all_beers
    
    def analyze_abv_distribution(self) -> Dict[str, float]:
        """Analyze alcohol by volume distribution"""
        beers = self.load_data()
        abv_values = [beer.get('abv', 0) for beer in beers if beer.get('abv')]
        
        if not abv_values:
            return {}
            
        return {
            'average': sum(abv_values) / len(abv_values),
            'min': min(abv_values),
            'max': max(abv_values),
            'count': len(abv_values)
        }
    
    def analyze_hops_popularity(self) -> Dict[str, int]:
        """Analyze most popular hops used"""
        beers = self.load_data()
        hop_counter = Counter()
        
        for beer in beers:
            hops = beer.get('ingredients', {}).get('hops', [])
            for hop in hops:
                hop_name = hop.get('name', '').strip()
                if hop_name:
                    hop_counter[hop_name] += 1
                    
        return dict(hop_counter.most_common(10))
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall summary statistics"""
        beers = self.load_data()
        return {
            'total_beers': len(beers),
            'abv_stats': self.analyze_abv_distribution(),
            'top_hops': self.analyze_hops_popularity()
        }
