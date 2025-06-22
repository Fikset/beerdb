import json
import time
from typing import Dict, Any, List, Callable
from threading import Thread
import queue

class EventPublisher:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = queue.Queue()
        self.worker_thread = Thread(target=self._process_events, daemon=True)
        self.worker_thread.start()
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to events of a specific type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event"""
        event = {
            'type': event_type,
            'data': data,
            'timestamp': time.time()
        }
        self.event_queue.put(event)
    
    def _process_events(self):
        """Process events in background thread"""
        while True:
            try:
                event = self.event_queue.get(timeout=1)
                event_type = event['type']
                
                if event_type in self.subscribers:
                    for callback in self.subscribers[event_type]:
                        try:
                            callback(event['data'])
                        except Exception as e:
                            print(f"Error processing event {event_type}: {e}")
                
                self.event_queue.task_done()
            except queue.Empty:
                continue

if __name__ == "__main__":
    # global event publisher instance
    event_publisher = EventPublisher()

    # event handlers
    def handle_beer_data_fetched(data):
        """Handle when new beer data is fetched"""
        print(f"New beer data fetched: {len(data)} beers")

    def handle_data_analyzed(data):
        """Handle when data analysis is complete"""
        print(f"Data analysis complete: {data}")

    # subscribe to events
    event_publisher.subscribe('beer_data_fetched', handle_beer_data_fetched)
    event_publisher.subscribe('data_analyzed', handle_data_analyzed)
