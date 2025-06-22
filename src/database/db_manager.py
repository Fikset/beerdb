import sqlite3
import json
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = 'beer_data.db'):
        self.db_path = db_path
        if db_path == ':memory:':
            self._conn = sqlite3.connect(db_path)
            self.init_database()
        else:
            self._conn = None
            self.init_database()
    
    def _get_connection(self):
        """Get database connection"""
        if self._conn:
            return self._conn
        else:
            return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        if self._conn:
            conn = self._conn
            conn.execute('''
                CREATE TABLE IF NOT EXISTS beers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    tagline TEXT,
                    abv REAL,
                    ibu REAL,
                    description TEXT,
                    ingredients TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS beers (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        tagline TEXT,
                        abv REAL,
                        ibu REAL,
                        description TEXT,
                        ingredients TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
    
    def save_beer(self, beer_data: Dict[str, Any]):
        """Save a single beer to database"""
        if self._conn:
            conn = self._conn
            conn.execute('''
                INSERT OR REPLACE INTO beers 
                (id, name, tagline, abv, ibu, description, ingredients)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                beer_data.get('id'),
                beer_data.get('name'),
                beer_data.get('tagline'),
                beer_data.get('abv'),
                beer_data.get('ibu'),
                beer_data.get('description'),
                json.dumps(beer_data.get('ingredients', {}))
            ))
            conn.commit()
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO beers 
                    (id, name, tagline, abv, ibu, description, ingredients)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    beer_data.get('id'),
                    beer_data.get('name'),
                    beer_data.get('tagline'),
                    beer_data.get('abv'),
                    beer_data.get('ibu'),
                    beer_data.get('description'),
                    json.dumps(beer_data.get('ingredients', {}))
                ))
                conn.commit()
    
    def save_beers_batch(self, beers: List[Dict[str, Any]]):
        """Save multiple beers to database"""
        for beer in beers:
            self.save_beer(beer)
    
    def get_all_beers(self) -> List[Dict[str, Any]]:
        """Retrieve all beers from database"""
        if self._conn:
            conn = self._conn
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM beers')
            return [dict(row) for row in cursor.fetchall()]
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM beers')
                return [dict(row) for row in cursor.fetchall()]
    
    def get_beer_by_id(self, beer_id: int) -> Dict[str, Any]:
        """Retrieve a specific beer by ID"""
        if self._conn:
            conn = self._conn
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM beers WHERE id = ?', (beer_id,))
            row = cursor.fetchone()
            return dict(row) if row else {}
        else:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('SELECT * FROM beers WHERE id = ?', (beer_id,))
                row = cursor.fetchone()
                return dict(row) if row else {}
    
    def close(self):
        """Close the database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
