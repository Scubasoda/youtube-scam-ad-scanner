"""
Batch URL Scanner - Test multiple URLs at once

Usage:
    python test_batch.py
    
This script reads URLs from sample_urls.txt and scans them all.
"""

from src.scanner import ScamScanner
import sys


def load_urls_from_file(filename='sample_urls.txt'):
    """Load URLs from a text file, ignoring comments and empty lines"""
    urls = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    urls.append(line)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    
    return urls


def main():
    # Example URLs to test
    urls = [
        "https://www.wikipedia.org",
        "https://www.github.com",
        "https://www.python.org",
    ]
    
    print("=" * 70)
    print("BATCH URL SCANNER")
    print("=" * 70)
    print(f"\nScanning {len(urls)} URLs...\n")
    
    scanner = ScamScanner(timeout=10)
    
    results_summary = []
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Scanning: {url}")
        
        try:
            results = scanner.scan_url(url)
            
            risk_level = results['risk_level']
            risk_score = results['risk_score']
            indicator_count = len(results['indicators'])
            
            # Color coding for console output
            if risk_level == 'HIGH':
                symbol = '❌'
            elif risk_level == 'MEDIUM':
                symbol = '⚠️ '
            elif risk_level == 'LOW':
                symbol = '⚡'
            else:
                symbol = '✓'
            
            print(f"    {symbol} Risk: {risk_level} (Score: {risk_score}, Indicators: {indicator_count})")
            
            results_summary.append({
                'url': url,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'indicator_count': indicator_count
            })
            
        except Exception as e:
            print(f"    ❌ Error scanning URL: {e}")
            results_summary.append({
                'url': url,
                'risk_level': 'ERROR',
                'risk_score': -1,
                'indicator_count': 0
            })
        
        print()
    
    # Print summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal URLs scanned: {len(results_summary)}")
    
    high_risk = sum(1 for r in results_summary if r['risk_level'] == 'HIGH')
    medium_risk = sum(1 for r in results_summary if r['risk_level'] == 'MEDIUM')
    low_risk = sum(1 for r in results_summary if r['risk_level'] == 'LOW')
    minimal_risk = sum(1 for r in results_summary if r['risk_level'] == 'MINIMAL')
    errors = sum(1 for r in results_summary if r['risk_level'] == 'ERROR')
    
    print(f"  HIGH risk:    {high_risk}")
    print(f"  MEDIUM risk:  {medium_risk}")
    print(f"  LOW risk:     {low_risk}")
    print(f"  MINIMAL risk: {minimal_risk}")
    if errors > 0:
        print(f"  Errors:       {errors}")
    
    print("\n" + "=" * 70)
    
    # List high-risk URLs if any
    if high_risk > 0:
        print("\n⚠️  HIGH RISK URLs:")
        for r in results_summary:
            if r['risk_level'] == 'HIGH':
                print(f"  - {r['url']} (Score: {r['risk_score']})")
        print()


if __name__ == '__main__':
    main()
