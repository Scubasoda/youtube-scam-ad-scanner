"""
Local API Server for YouTube Scam Ad Scanner
Enables the browser extension to automatically scan URLs in real-time
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.scanner import ScamScanner
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from browser extension

# Initialize scanner
scanner = ScamScanner(timeout=10)

# Setup logging directory
LOG_DIR = 'scan_logs'
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'api_server.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    """API status page"""
    return jsonify({
        'status': 'running',
        'service': 'YouTube Scam Ad Scanner API',
        'version': '0.1.0',
        'endpoints': {
            '/scan': 'POST - Scan a URL',
            '/status': 'GET - Check API status',
            '/logs': 'GET - View scan logs',
            '/stats': 'GET - Get scanning statistics'
        }
    })


@app.route('/status', methods=['GET'])
def status():
    """Check if API is running"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/scan', methods=['POST'])
def scan_url():
    """
    Scan a URL for scam indicators
    
    Request body:
    {
        "url": "https://example.com",
        "source": "browser-extension" (optional),
        "metadata": {} (optional)
    }
    """
    try:
        data = request.json
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        source = data.get('source', 'api')
        metadata = data.get('metadata', {})
        
        logger.info(f"Scanning URL from {source}: {url}")
        
        # Perform scan
        results = scanner.scan_url(url)
        
        # Add metadata
        results['source'] = source
        results['scanned_at'] = datetime.now().isoformat()
        results['metadata'] = metadata
        
        # Log the scan
        log_scan(results)
        
        logger.info(f"Scan complete: {url} - Risk: {results['risk_level']}")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error scanning URL: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/batch-scan', methods=['POST'])
def batch_scan():
    """
    Scan multiple URLs at once
    
    Request body:
    {
        "urls": ["https://url1.com", "https://url2.com", ...],
        "source": "browser-extension" (optional)
    }
    """
    try:
        data = request.json
        
        if not data or 'urls' not in data:
            return jsonify({'error': 'URLs array is required'}), 400
        
        urls = data['urls']
        source = data.get('source', 'api')
        
        if not isinstance(urls, list):
            return jsonify({'error': 'URLs must be an array'}), 400
        
        logger.info(f"Batch scanning {len(urls)} URLs from {source}")
        
        results = []
        for url in urls:
            try:
                result = scanner.scan_url(url)
                result['source'] = source
                result['scanned_at'] = datetime.now().isoformat()
                log_scan(result)
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'scanned_at': datetime.now().isoformat()
                })
        
        return jsonify({
            'total': len(urls),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error in batch scan: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """Get scan logs"""
    try:
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        risk_level = request.args.get('risk_level', None)
        
        log_file = os.path.join(LOG_DIR, 'scans.jsonl')
        
        if not os.path.exists(log_file):
            return jsonify({'logs': []})
        
        # Read logs
        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    # Filter by risk level if specified
                    if risk_level and log.get('risk_level') != risk_level:
                        continue
                    logs.append(log)
                except json.JSONDecodeError:
                    continue
        
        # Get most recent logs
        logs = logs[-limit:]
        logs.reverse()  # Most recent first
        
        return jsonify({
            'total': len(logs),
            'logs': logs
        })
        
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get scanning statistics"""
    try:
        log_file = os.path.join(LOG_DIR, 'scans.jsonl')
        
        if not os.path.exists(log_file):
            return jsonify({
                'total_scans': 0,
                'risk_levels': {},
                'sources': {}
            })
        
        stats = {
            'total_scans': 0,
            'risk_levels': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'MINIMAL': 0},
            'sources': {},
            'unique_urls': set()
        }
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    stats['total_scans'] += 1
                    
                    # Count by risk level
                    risk = log.get('risk_level', 'UNKNOWN')
                    if risk in stats['risk_levels']:
                        stats['risk_levels'][risk] += 1
                    
                    # Count by source
                    source = log.get('source', 'unknown')
                    stats['sources'][source] = stats['sources'].get(source, 0) + 1
                    
                    # Track unique URLs
                    stats['unique_urls'].add(log.get('url', ''))
                    
                except json.JSONDecodeError:
                    continue
        
        stats['unique_urls'] = len(stats['unique_urls'])
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        return jsonify({'error': str(e)}), 500


def log_scan(results):
    """Log scan results to JSONL file"""
    try:
        log_file = os.path.join(LOG_DIR, 'scans.jsonl')
        
        # Create a clean log entry
        log_entry = {
            'timestamp': results.get('scanned_at', datetime.now().isoformat()),
            'url': results.get('url'),
            'risk_level': results.get('risk_level'),
            'risk_score': results.get('risk_score'),
            'indicator_count': len(results.get('indicators', [])),
            'indicators': results.get('indicators', []),
            'source': results.get('source'),
            'valid_url': results.get('valid_url'),
            'accessible': results.get('accessible'),
            'metadata': results.get('metadata', {})
        }
        
        # Append to log file (JSONL format - one JSON object per line)
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
        # Also create a daily summary log
        daily_log = os.path.join(
            LOG_DIR, 
            f"scans_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        )
        with open(daily_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        logger.error(f"Error logging scan: {str(e)}")


if __name__ == '__main__':
    logger.info("Starting YouTube Scam Ad Scanner API Server")
    logger.info(f"Logs will be saved to: {os.path.abspath(LOG_DIR)}")
    logger.info("API available at: http://localhost:5000")
    logger.info("Press Ctrl+C to stop")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
