#!/usr/bin/env python3

import os
import sys
import json
from flask import Flask, request, jsonify, render_template_string
from prometheus_client import generate_latest, Summary, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.beer_service import BeerService

app = Flask(__name__)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
FETCH_COUNTER = Counter('data_fetch_total', 'Total number of data fetch operations')
ANALYSIS_COUNTER = Counter('analysis_runs_total', 'Total number of analysis runs')

beer_service = BeerService()

@app.route("/")
def main():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BeerDB - Craft Beer Management System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .action-buttons { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .btn { padding: 12px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; text-align: center; border: none; cursor: pointer; font-size: 14px; }
            .btn:hover { background: #2980b9; }
            .btn-success { background: #27ae60; }
            .btn-success:hover { background: #219a52; }
            .btn-warning { background: #f39c12; }
            .btn-warning:hover { background: #e67e22; }
            .endpoints { margin-top: 30px; }
            .endpoint { background: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍺 BeerDB Management System</h1>
            <p>Comprehensive craft beer data collection, storage, and analysis platform.</p>
            
            <div class="action-buttons">
                <a href="/api/fetch" class="btn btn-success">Fetch New Data</a>
                <a href="/api/analyze" class="btn btn-warning">Run Analysis</a>
                <a href="/api/beers" class="btn">View All Beers</a>
                <a href="/api/stats" class="btn">View Statistics</a>
            </div>
            
            <div class="endpoints">
                <h3>Available API Endpoints:</h3>
                <div class="endpoint">GET /api/beers - List all beers</div>
                <div class="endpoint">GET /api/beers/{id} - Get specific beer</div>
                <div class="endpoint">POST /api/fetch - Fetch new data from PunkAPI</div>
                <div class="endpoint">GET /api/analyze - Run data analysis</div>
                <div class="endpoint">GET /api/stats - Get summary statistics</div>
                <div class="endpoint">GET /health - Health check</div>
                <div class="endpoint">GET /metrics - Prometheus metrics</div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/api/fetch", methods=["GET", "POST"])
@REQUEST_TIME.time()
def fetch_data():
    """Fetch new beer data from PunkAPI"""
    FETCH_COUNTER.inc()
    
    result = beer_service.fetch_beer_data()
    
    if result['success']:
        return jsonify({
            'status': 'success',
            'message': result['message'],
            'count': result['count']
        })
    else:
        return jsonify({
            'status': 'error',
            'message': result['message']
        }), 500

@app.route("/api/beers", methods=["GET"])
@REQUEST_TIME.time()
def get_all_beers():
    """Get all beers from database"""
    try:
        beers = beer_service.get_all_beers()
        return jsonify({
            'status': 'success',
            'count': len(beers),
            'beers': beers
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route("/api/beers/<int:beer_id>", methods=["GET"])
@REQUEST_TIME.time()
def get_beer_by_id(beer_id):
    """Get a specific beer by ID"""
    try:
        beer = beer_service.get_beer_by_id(beer_id)
        if beer:
            return jsonify({
                'status': 'success',
                'beer': beer
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Beer not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route("/api/analyze", methods=["GET"])
@REQUEST_TIME.time()
def run_analysis():
    """Run data analysis on beer collection"""
    ANALYSIS_COUNTER.inc()
    
    result = beer_service.run_analysis()
    
    if result['success']:
        return jsonify({
            'status': 'success',
            'analysis': result['analysis']
        })
    else:
        return jsonify({
            'status': 'error',
            'message': result['message']
        }), 500

@app.route("/api/stats", methods=["GET"])
@REQUEST_TIME.time()
def get_statistics():
    """Get summary statistics"""
    result = beer_service.get_statistics()
    
    if result['success']:
        return jsonify({
            'status': 'success',
            'statistics': result['statistics']
        })
    else:
        return jsonify({
            'status': 'error',
            'message': result['message']
        }), 500

@app.route("/health", methods=["GET"])
@REQUEST_TIME.time()
def health_check():
    """Health check endpoint"""
    result = beer_service.health_check()
    
    if result['success']:
        return jsonify({
            'status': result['status'],
            'service': result['service'],
            'database': result['database']
        })
    else:
        return jsonify({
            'status': result['status'],
            'service': result['service'],
            'error': result['error']
        }), 500

@app.route("/metrics", methods=["GET"])
@REQUEST_TIME.time()
def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
