"""
Beer service module for handling business logic
"""
import os
import json
from typing import Dict, List, Any, Optional
from data_fetcher.fetcher import Fetcher
from database.db_manager import DatabaseManager
from data_analyzer.analyzer import BeerAnalyzer
from messaging.event_publisher import EventPublisher


class BeerService:
    """Service class to handle beer-related operations"""
    
    def __init__(self, data_dir: str = 'data', db_path: str = 'beer_data.db'):
        self.data_dir = data_dir
        self.db_manager = DatabaseManager(db_path)
        self.analyzer = BeerAnalyzer(data_dir)
        self.event_publisher = EventPublisher()
        
        os.makedirs(data_dir, exist_ok=True)
        
        self.event_publisher.subscribe('beer_data_fetched', self._handle_data_fetched)
        self.event_publisher.subscribe('analysis_complete', self._handle_analysis_complete)
    
    def _handle_data_fetched(self, data: List[Dict[str, Any]]):
        """Handle when new beer data is fetched"""
        if data and len(data) > 0:
            self.db_manager.save_beers_batch(data)
            print(f"Saved {len(data)} beers to database")
    
    def _handle_analysis_complete(self, data: Dict[str, Any]):
        """Handle when analysis is complete"""
        print(f"Analysis complete: {data}")
    
    def fetch_beer_data(self, pages: int = 5, per_page: int = 80) -> Dict[str, Any]:
        """
        Fetch beer data from PunkAPI
        
        Args:
            pages: Number of pages to fetch
            per_page: Number of beers per page
            
        Returns:
            Dict with operation result
        """
        try:
            all_beers = []
            
            for page in range(1, pages + 1):
                fetcher = Fetcher('https://api.punkapi.com/v2/beers', self.data_dir, page)
                page_data = fetcher.get_beers_page(per_page)
                
                if page_data:
                    all_beers.extend(page_data)
                    fetcher.save_to_file(page_data)
            
            self.event_publisher.publish('beer_data_fetched', all_beers)
            
            return {
                'success': True,
                'message': f'Successfully fetched {len(all_beers)} beers',
                'count': len(all_beers),
                'data': all_beers
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error fetching data: {str(e)}',
                'count': 0,
                'data': []
            }
    
    def get_all_beers(self) -> List[Dict[str, Any]]:
        """Get all beers from database"""
        return self.db_manager.get_all_beers()
    
    def get_beer_by_id(self, beer_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific beer by ID"""
        return self.db_manager.get_beer_by_id(beer_id)
    
    def run_analysis(self) -> Dict[str, Any]:
        """
        Run data analysis on beer collection
        
        Returns:
            Dict with analysis results
        """
        try:
            stats = self.analyzer.get_summary_stats()
            
            self.event_publisher.publish('analysis_complete', stats)
            
            return {
                'success': True,
                'analysis': stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error running analysis: {str(e)}',
                'analysis': {}
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        try:
            all_beers = self.db_manager.get_all_beers()
            
            analysis_stats = self.analyzer.get_summary_stats()
            
            return {
                'success': True,
                'statistics': {
                    'database': {
                        'total_beers_in_db': len(all_beers),
                        'latest_beers': all_beers[-5:] if all_beers else []
                    },
                    'analysis': analysis_stats
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error getting statistics: {str(e)}',
                'statistics': {}
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        try:
            self.db_manager.get_all_beers()
            
            return {
                'success': True,
                'status': 'healthy',
                'service': 'BeerDB API',
                'database': 'connected'
            }
            
        except Exception as e:
            return {
                'success': False,
                'status': 'unhealthy',
                'service': 'BeerDB API',
                'error': str(e)
            }
    
    def close(self):
        """Clean up resources"""
        self.db_manager.close()
