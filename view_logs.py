"""
View and analyze scan logs from the YouTube Scam Ad Scanner
"""

import json
import os
from datetime import datetime
from collections import Counter
import click


LOG_DIR = 'scan_logs'


@click.group()
def cli():
    """Scan log viewer and analyzer"""
    pass


@cli.command()
@click.option('--limit', '-n', default=20, help='Number of recent logs to show')
@click.option('--risk-level', '-r', type=click.Choice(['HIGH', 'MEDIUM', 'LOW', 'MINIMAL']), 
              help='Filter by risk level')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'detailed']), 
              default='table', help='Output format')
def view(limit, risk_level, format):
    """View recent scan logs"""
    log_file = os.path.join(LOG_DIR, 'scans.jsonl')
    
    if not os.path.exists(log_file):
        click.echo("No scan logs found. Run some scans first!")
        return
    
    # Read logs
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log = json.loads(line)
                if risk_level and log.get('risk_level') != risk_level:
                    continue
                logs.append(log)
            except json.JSONDecodeError:
                continue
    
    # Get most recent
    logs = logs[-limit:]
    logs.reverse()
    
    if not logs:
        click.echo("No logs found matching criteria")
        return
    
    if format == 'json':
        click.echo(json.dumps(logs, indent=2))
    elif format == 'detailed':
        for log in logs:
            print_detailed_log(log)
    else:
        print_table(logs)


@cli.command()
def stats():
    """Show scanning statistics"""
    log_file = os.path.join(LOG_DIR, 'scans.jsonl')
    
    if not os.path.exists(log_file):
        click.echo("No scan logs found")
        return
    
    # Collect stats
    total = 0
    risk_counts = Counter()
    source_counts = Counter()
    urls = set()
    high_risk_urls = []
    
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log = json.loads(line)
                total += 1
                risk_counts[log.get('risk_level', 'UNKNOWN')] += 1
                source_counts[log.get('source', 'unknown')] += 1
                urls.add(log.get('url'))
                
                if log.get('risk_level') == 'HIGH':
                    high_risk_urls.append(log.get('url'))
                    
            except json.JSONDecodeError:
                continue
    
    # Print stats
    click.echo("\n" + "=" * 70)
    click.echo("SCAN STATISTICS")
    click.echo("=" * 70)
    click.echo(f"\nTotal Scans: {total}")
    click.echo(f"Unique URLs: {len(urls)}")
    
    click.echo("\nRisk Level Distribution:")
    for risk in ['HIGH', 'MEDIUM', 'LOW', 'MINIMAL']:
        count = risk_counts.get(risk, 0)
        pct = (count / total * 100) if total > 0 else 0
        bar = '█' * int(pct / 2)
        click.echo(f"  {risk:8s}: {count:4d} ({pct:5.1f}%) {bar}")
    
    click.echo("\nSources:")
    for source, count in source_counts.most_common():
        click.echo(f"  {source}: {count}")
    
    if high_risk_urls:
        click.echo(f"\n⚠️  HIGH RISK URLs ({len(high_risk_urls)}):")
        for url in high_risk_urls[:10]:
            click.echo(f"  - {url}")
        if len(high_risk_urls) > 10:
            click.echo(f"  ... and {len(high_risk_urls) - 10} more")
    
    click.echo("\n" + "=" * 70 + "\n")


@cli.command()
@click.argument('url')
def find(url):
    """Find scans for a specific URL"""
    log_file = os.path.join(LOG_DIR, 'scans.jsonl')
    
    if not os.path.exists(log_file):
        click.echo("No scan logs found")
        return
    
    found = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log = json.loads(line)
                if url in log.get('url', ''):
                    found.append(log)
            except json.JSONDecodeError:
                continue
    
    if not found:
        click.echo(f"No scans found for URL containing: {url}")
        return
    
    click.echo(f"\nFound {len(found)} scan(s) for URLs containing: {url}\n")
    for log in found:
        print_detailed_log(log)


@cli.command()
@click.option('--output', '-o', default='scan_report.html', help='Output file')
def report(output):
    """Generate HTML report of scan logs"""
    log_file = os.path.join(LOG_DIR, 'scans.jsonl')
    
    if not os.path.exists(log_file):
        click.echo("No scan logs found")
        return
    
    # Read all logs
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    # Generate HTML report
    html = generate_html_report(logs)
    
    with open(output, 'w') as f:
        f.write(html)
    
    click.echo(f"✅ Report generated: {output}")
    click.echo(f"Total scans: {len(logs)}")


def print_table(logs):
    """Print logs in table format"""
    click.echo("\n" + "=" * 120)
    click.echo(f"{'Timestamp':<20} {'Risk':<8} {'Score':<6} {'URL':<70}")
    click.echo("=" * 120)
    
    for log in logs:
        timestamp = log.get('timestamp', '')[:19]
        risk = log.get('risk_level', 'N/A')
        score = log.get('risk_score', 0)
        url = log.get('url', '')[:70]
        
        # Color code by risk
        if risk == 'HIGH':
            risk = click.style(risk, fg='red', bold=True)
        elif risk == 'MEDIUM':
            risk = click.style(risk, fg='yellow')
        elif risk == 'LOW':
            risk = click.style(risk, fg='yellow')
        else:
            risk = click.style(risk, fg='green')
        
        click.echo(f"{timestamp:<20} {risk:<8} {score:<6} {url:<70}")
    
    click.echo("=" * 120 + "\n")


def print_detailed_log(log):
    """Print detailed log entry"""
    click.echo("─" * 70)
    click.echo(f"Timestamp: {log.get('timestamp')}")
    click.echo(f"URL: {log.get('url')}")
    
    risk = log.get('risk_level', 'N/A')
    if risk == 'HIGH':
        risk = click.style(risk, fg='red', bold=True)
    elif risk == 'MEDIUM':
        risk = click.style(risk, fg='yellow')
    else:
        risk = click.style(risk, fg='green')
    
    click.echo(f"Risk Level: {risk} (Score: {log.get('risk_score', 0)})")
    click.echo(f"Source: {log.get('source', 'N/A')}")
    click.echo(f"Valid URL: {log.get('valid_url')}")
    click.echo(f"Accessible: {log.get('accessible')}")
    
    indicators = log.get('indicators', [])
    if indicators:
        click.echo(f"\nIndicators ({len(indicators)}):")
        for i, ind in enumerate(indicators, 1):
            click.echo(f"  {i}. {ind}")
    
    metadata = log.get('metadata', {})
    if metadata:
        click.echo(f"\nMetadata: {json.dumps(metadata, indent=2)}")
    
    click.echo()


def generate_html_report(logs):
    """Generate HTML report"""
    # Calculate stats
    total = len(logs)
    risk_counts = Counter(log.get('risk_level') for log in logs)
    
    high_risk = [log for log in logs if log.get('risk_level') == 'HIGH']
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Scan Report - YouTube Scam Ad Scanner</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #333; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-card {{ background: #f9f9f9; padding: 20px; border-radius: 5px; text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #0066cc; }}
        .stat-label {{ color: #666; margin-top: 10px; }}
        .high-risk {{ background: #ffebee; }}
        .high-risk .stat-value {{ color: #d32f2f; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #0066cc; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .risk-HIGH {{ color: #d32f2f; font-weight: bold; }}
        .risk-MEDIUM {{ color: #f57c00; }}
        .risk-LOW {{ color: #fbc02d; }}
        .risk-MINIMAL {{ color: #388e3c; }}
        .url-cell {{ max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Scan Report - YouTube Scam Ad Scanner</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Total Scans</div>
            </div>
            <div class="stat-card high-risk">
                <div class="stat-value">{risk_counts.get('HIGH', 0)}</div>
                <div class="stat-label">HIGH Risk</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{risk_counts.get('MEDIUM', 0)}</div>
                <div class="stat-label">MEDIUM Risk</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{risk_counts.get('LOW', 0) + risk_counts.get('MINIMAL', 0)}</div>
                <div class="stat-label">LOW/MINIMAL Risk</div>
            </div>
        </div>
        
        <h2>Recent Scans</h2>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>URL</th>
                <th>Risk Level</th>
                <th>Score</th>
                <th>Indicators</th>
            </tr>
"""
    
    for log in reversed(logs[-100:]):  # Last 100 scans
        risk = log.get('risk_level', 'N/A')
        html += f"""
            <tr>
                <td>{log.get('timestamp', '')[:19]}</td>
                <td class="url-cell" title="{log.get('url', '')}">{log.get('url', '')}</td>
                <td class="risk-{risk}">{risk}</td>
                <td>{log.get('risk_score', 0)}</td>
                <td>{len(log.get('indicators', []))}</td>
            </tr>
"""
    
    html += """
        </table>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == '__main__':
    cli()
