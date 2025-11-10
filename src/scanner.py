"""
YouTube Scam Ad Scanner - Main scanner implementation
Analyzes URLs for common scam indicators using heuristics.
"""

import re
import sys
from typing import Dict, List, Tuple
from urllib.parse import urlparse

import click
import requests
from bs4 import BeautifulSoup
import tldextract
import validators
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()


class ScamIndicators:
    """Common scam indicators and heuristics"""
    
    # Suspicious keywords often found in scam ads
    SCAM_KEYWORDS = [
        'get rich quick', 'make money fast', 'earn from home',
        'limited time offer', 'act now', 'click here now',
        'congratulations', 'you have won', 'claim your prize',
        'risk free', 'guaranteed income', 'double your money',
        'lose weight fast', 'miracle cure', 'one weird trick',
        'free trial', 'no credit card required', 'limited spots',
        'secret method', 'insider trading', 'passive income',
        'financial freedom', 'work from home', 'be your own boss'
    ]
    
    # Suspicious domain patterns
    SUSPICIOUS_TLD = ['.xyz', '.top', '.click', '.loan', '.work', '.gq', '.ml', '.cf', '.tk']
    
    # Urgency/pressure words
    URGENCY_WORDS = [
        'urgent', 'hurry', 'limited time', 'expires soon', 'today only',
        'don\'t miss out', 'last chance', 'act fast', 'now or never'
    ]
    
    # Too-good-to-be-true phrases
    TGTBT_PHRASES = [
        'free money', 'easy money', 'instant cash', 'guaranteed',
        'no risk', 'amazing results', 'shocking', 'unbelievable'
    ]


class ScamScanner:
    """Main scanner class for analyzing URLs"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scan_url(self, url: str) -> Dict:
        """
        Scan a URL for scam indicators
        
        Args:
            url: The URL to scan
            
        Returns:
            Dictionary containing scan results and risk score
        """
        results = {
            'url': url,
            'valid_url': False,
            'accessible': False,
            'risk_score': 0,
            'indicators': [],
            'details': {}
        }
        
        # Validate URL
        if not validators.url(url):
            results['indicators'].append('Invalid URL format')
            return results
        
        results['valid_url'] = True
        
        # Analyze domain
        domain_score, domain_indicators = self._analyze_domain(url)
        results['risk_score'] += domain_score
        results['indicators'].extend(domain_indicators)
        results['details']['domain_analysis'] = {
            'score': domain_score,
            'indicators': domain_indicators
        }
        
        # Try to fetch and analyze page content
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            results['accessible'] = True
            results['details']['status_code'] = response.status_code
            results['details']['final_url'] = response.url
            
            # Check for redirects
            if response.url != url:
                results['indicators'].append(f'Redirects to different URL')
                results['risk_score'] += 5
            
            if response.status_code == 200:
                # Analyze page content
                content_score, content_indicators = self._analyze_content(response.text, response.url)
                results['risk_score'] += content_score
                results['indicators'].extend(content_indicators)
                results['details']['content_analysis'] = {
                    'score': content_score,
                    'indicators': content_indicators
                }
                
        except requests.exceptions.RequestException as e:
            results['indicators'].append(f'Failed to fetch URL: {str(e)}')
            results['risk_score'] += 10
        
        # Calculate risk level
        results['risk_level'] = self._calculate_risk_level(results['risk_score'])
        
        return results
    
    def _analyze_domain(self, url: str) -> Tuple[int, List[str]]:
        """Analyze domain for suspicious characteristics"""
        score = 0
        indicators = []
        
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        domain = extracted.domain
        tld = f'.{extracted.suffix}'
        
        # Check for suspicious TLD
        if tld in ScamIndicators.SUSPICIOUS_TLD:
            score += 15
            indicators.append(f'Suspicious TLD: {tld}')
        
        # Check domain length (very long domains can be suspicious)
        if len(domain) > 20:
            score += 10
            indicators.append(f'Unusually long domain name ({len(domain)} chars)')
        
        # Check for excessive hyphens or numbers
        hyphen_count = domain.count('-')
        if hyphen_count > 2:
            score += 10
            indicators.append(f'Multiple hyphens in domain ({hyphen_count})')
        
        digit_count = sum(c.isdigit() for c in domain)
        if digit_count > 3:
            score += 5
            indicators.append(f'Multiple digits in domain ({digit_count})')
        
        # Check for HTTP (not HTTPS)
        if parsed.scheme == 'http':
            score += 10
            indicators.append('No HTTPS encryption')
        
        # Check for IP address instead of domain
        if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
            score += 20
            indicators.append('Using IP address instead of domain name')
        
        return score, indicators
    
    def _analyze_content(self, html: str, url: str) -> Tuple[int, List[str]]:
        """Analyze page content for scam indicators"""
        score = 0
        indicators = []
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Get text content
        text = soup.get_text().lower()
        title = soup.title.string.lower() if soup.title else ''
        
        # Check for scam keywords
        found_keywords = []
        for keyword in ScamIndicators.SCAM_KEYWORDS:
            if keyword in text or keyword in title:
                found_keywords.append(keyword)
        
        if found_keywords:
            score += len(found_keywords) * 5
            indicators.append(f'Found {len(found_keywords)} scam keywords: {", ".join(found_keywords[:3])}{"..." if len(found_keywords) > 3 else ""}')
        
        # Check for urgency words
        urgency_count = sum(1 for word in ScamIndicators.URGENCY_WORDS if word in text)
        if urgency_count > 2:
            score += urgency_count * 3
            indicators.append(f'High urgency language detected ({urgency_count} instances)')
        
        # Check for too-good-to-be-true phrases
        tgtbt_count = sum(1 for phrase in ScamIndicators.TGTBT_PHRASES if phrase in text)
        if tgtbt_count > 0:
            score += tgtbt_count * 5
            indicators.append(f'Too-good-to-be-true phrases detected ({tgtbt_count} instances)')
        
        # Check for excessive exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count > 10:
            score += 10
            indicators.append(f'Excessive exclamation marks ({exclamation_count})')
        
        # Check for popup/alert scripts (common in scams)
        if 'alert(' in html.lower() or 'confirm(' in html.lower():
            score += 15
            indicators.append('Contains popup/alert scripts')
        
        # Check for missing or suspicious meta tags
        if not soup.find('meta', attrs={'name': 'description'}):
            score += 5
            indicators.append('Missing meta description')
        
        # Check for external links (phishing often has few legitimate external links)
        external_links = soup.find_all('a', href=True)
        if len(external_links) < 3:
            score += 5
            indicators.append(f'Very few external links ({len(external_links)})')
        
        # Check for forms (potential data collection)
        forms = soup.find_all('form')
        if forms:
            password_fields = soup.find_all('input', attrs={'type': 'password'})
            if password_fields:
                score += 15
                indicators.append('Contains password input fields')
            
            # Check for forms without proper action
            for form in forms:
                if not form.get('action') or form.get('action') == '#':
                    score += 10
                    indicators.append('Form with suspicious or missing action')
                    break
        
        return score, indicators
    
    def _calculate_risk_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score >= 50:
            return 'HIGH'
        elif score >= 25:
            return 'MEDIUM'
        elif score >= 10:
            return 'LOW'
        else:
            return 'MINIMAL'


def print_results(results: Dict):
    """Pretty print scan results"""
    print("\n" + "=" * 70)
    print(f"SCAM SCAN RESULTS")
    print("=" * 70)
    print(f"\nURL: {results['url']}")
    print(f"Valid URL: {results['valid_url']}")
    print(f"Accessible: {results['accessible']}")
    
    # Color-coded risk level
    risk_level = results['risk_level']
    risk_score = results['risk_score']
    
    if risk_level == 'HIGH':
        color = Fore.RED
    elif risk_level == 'MEDIUM':
        color = Fore.YELLOW
    elif risk_level == 'LOW':
        color = Fore.YELLOW
    else:
        color = Fore.GREEN
    
    print(f"\n{color}Risk Level: {risk_level} (Score: {risk_score}){Style.RESET_ALL}")
    
    if results['indicators']:
        print(f"\nIndicators Found ({len(results['indicators'])}):")
        for i, indicator in enumerate(results['indicators'], 1):
            print(f"  {i}. {indicator}")
    else:
        print(f"\n{Fore.GREEN}No significant scam indicators detected.{Style.RESET_ALL}")
    
    if 'final_url' in results.get('details', {}):
        if results['details']['final_url'] != results['url']:
            print(f"\nFinal URL: {results['details']['final_url']}")
    
    print("\n" + "=" * 70)
    
    # Provide recommendation
    if risk_level == 'HIGH':
        print(f"\n{Fore.RED}⚠️  WARNING: This URL shows multiple scam indicators. Avoid interaction.{Style.RESET_ALL}")
    elif risk_level == 'MEDIUM':
        print(f"\n{Fore.YELLOW}⚠️  CAUTION: This URL shows some suspicious characteristics. Proceed carefully.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}✓ This URL appears relatively safe, but always exercise caution online.{Style.RESET_ALL}")
    
    print()


@click.command()
@click.option('--url', '-u', required=True, help='URL to scan for scam indicators')
@click.option('--timeout', '-t', default=10, help='Request timeout in seconds (default: 10)')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
def main(url: str, timeout: int, output_json: bool):
    """
    YouTube Scam Ad Scanner
    
    Scan a URL for common scam indicators including suspicious domains,
    scam keywords, urgency language, and other heuristics.
    """
    scanner = ScamScanner(timeout=timeout)
    
    click.echo(f"Scanning URL: {url}")
    click.echo("Please wait...")
    
    results = scanner.scan_url(url)
    
    if output_json:
        import json
        print(json.dumps(results, indent=2))
    else:
        print_results(results)
    
    # Exit with error code if high risk
    if results['risk_level'] == 'HIGH':
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
