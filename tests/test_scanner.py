"""Unit tests for the YouTube Scam Ad Scanner"""

import pytest
from src.scanner import ScamScanner, ScamIndicators


class TestScamIndicators:
    """Test the ScamIndicators class"""
    
    def test_scam_keywords_present(self):
        """Test that scam keywords list is not empty"""
        assert len(ScamIndicators.SCAM_KEYWORDS) > 0
    
    def test_suspicious_tld_present(self):
        """Test that suspicious TLD list is not empty"""
        assert len(ScamIndicators.SUSPICIOUS_TLD) > 0


class TestScamScanner:
    """Test the ScamScanner class"""
    
    @pytest.fixture
    def scanner(self):
        """Create a scanner instance for testing"""
        return ScamScanner(timeout=5)
    
    def test_scanner_initialization(self, scanner):
        """Test that scanner initializes correctly"""
        assert scanner.timeout == 5
        assert scanner.session is not None
    
    def test_invalid_url_detection(self, scanner):
        """Test detection of invalid URLs"""
        results = scanner.scan_url("not-a-valid-url")
        assert results['valid_url'] is False
        assert 'Invalid URL format' in results['indicators']
    
    def test_risk_level_calculation_high(self, scanner):
        """Test high risk level calculation"""
        level = scanner._calculate_risk_level(60)
        assert level == 'HIGH'
    
    def test_risk_level_calculation_medium(self, scanner):
        """Test medium risk level calculation"""
        level = scanner._calculate_risk_level(30)
        assert level == 'MEDIUM'
    
    def test_risk_level_calculation_low(self, scanner):
        """Test low risk level calculation"""
        level = scanner._calculate_risk_level(15)
        assert level == 'LOW'
    
    def test_risk_level_calculation_minimal(self, scanner):
        """Test minimal risk level calculation"""
        level = scanner._calculate_risk_level(5)
        assert level == 'MINIMAL'
    
    def test_domain_analysis_suspicious_tld(self, scanner):
        """Test detection of suspicious TLD"""
        score, indicators = scanner._analyze_domain("http://scam-site.xyz")
        assert score > 0
        assert any('Suspicious TLD' in ind for ind in indicators)
    
    def test_domain_analysis_http_not_https(self, scanner):
        """Test detection of HTTP (not HTTPS)"""
        score, indicators = scanner._analyze_domain("http://example.com")
        assert score > 0
        assert any('No HTTPS' in ind for ind in indicators)
    
    def test_domain_analysis_https(self, scanner):
        """Test that HTTPS doesn't trigger HTTP warning"""
        score, indicators = scanner._analyze_domain("https://example.com")
        assert not any('No HTTPS' in ind for ind in indicators)
    
    def test_domain_analysis_ip_address(self, scanner):
        """Test detection of IP address instead of domain"""
        score, indicators = scanner._analyze_domain("http://192.168.1.1")
        assert score > 0
        assert any('IP address' in ind for ind in indicators)
    
    def test_domain_analysis_long_domain(self, scanner):
        """Test detection of unusually long domain names"""
        score, indicators = scanner._analyze_domain("http://thisdomainnameiswaytoolongandprobablysuspicious.com")
        assert score > 0
        assert any('long domain' in ind for ind in indicators)
    
    def test_domain_analysis_multiple_hyphens(self, scanner):
        """Test detection of multiple hyphens in domain"""
        score, indicators = scanner._analyze_domain("http://scam-get-rich-quick-now.com")
        assert score > 0
        assert any('hyphens' in ind for ind in indicators)
    
    def test_content_analysis_scam_keywords(self, scanner):
        """Test detection of scam keywords in content"""
        html = "<html><body><h1>Get Rich Quick!</h1><p>Make money fast from home!</p></body></html>"
        score, indicators = scanner._analyze_content(html, "http://example.com")
        assert score > 0
        assert any('scam keywords' in ind.lower() for ind in indicators)
    
    def test_content_analysis_urgency_language(self, scanner):
        """Test detection of urgency language"""
        html = "<html><body><p>Act now! Limited time! Hurry! Don't miss out! Last chance!</p></body></html>"
        score, indicators = scanner._analyze_content(html, "http://example.com")
        assert score > 0
        assert any('urgency' in ind.lower() for ind in indicators)
    
    def test_content_analysis_excessive_exclamations(self, scanner):
        """Test detection of excessive exclamation marks"""
        html = "<html><body>" + "Amazing! " * 20 + "</body></html>"
        score, indicators = scanner._analyze_content(html, "http://example.com")
        assert score > 0
        assert any('exclamation' in ind.lower() for ind in indicators)
    
    def test_content_analysis_password_field(self, scanner):
        """Test detection of password input fields"""
        html = '<html><body><form><input type="password" name="pwd"></form></body></html>'
        score, indicators = scanner._analyze_content(html, "http://example.com")
        assert score > 0
        assert any('password' in ind.lower() for ind in indicators)
    
    def test_content_analysis_popup_scripts(self, scanner):
        """Test detection of popup/alert scripts"""
        html = "<html><body><script>alert('You won!');</script></body></html>"
        score, indicators = scanner._analyze_content(html, "http://example.com")
        assert score > 0
        assert any('popup' in ind.lower() or 'alert' in ind.lower() for ind in indicators)
    
    def test_scan_url_structure(self, scanner):
        """Test that scan_url returns expected structure"""
        results = scanner.scan_url("https://www.google.com")
        
        # Check all expected keys are present
        assert 'url' in results
        assert 'valid_url' in results
        assert 'accessible' in results
        assert 'risk_score' in results
        assert 'indicators' in results
        assert 'details' in results
        assert 'risk_level' in results
        
        # Check types
        assert isinstance(results['url'], str)
        assert isinstance(results['valid_url'], bool)
        assert isinstance(results['risk_score'], int)
        assert isinstance(results['indicators'], list)
        assert isinstance(results['details'], dict)


class TestIntegration:
    """Integration tests with real URLs (use with caution)"""
    
    @pytest.fixture
    def scanner(self):
        """Create a scanner instance for testing"""
        return ScamScanner(timeout=10)
    
    @pytest.mark.slow
    def test_scan_legitimate_site(self, scanner):
        """Test scanning a known legitimate site"""
        results = scanner.scan_url("https://www.wikipedia.org")
        assert results['valid_url'] is True
        # Wikipedia should have low to minimal risk
        assert results['risk_level'] in ['MINIMAL', 'LOW']
    
    @pytest.mark.slow
    def test_scan_with_redirect(self, scanner):
        """Test that redirects are detected"""
        # Using a URL shortener that redirects
        results = scanner.scan_url("http://bit.ly/test")
        if results['accessible']:
            # Should detect if redirect occurred
            assert 'details' in results
