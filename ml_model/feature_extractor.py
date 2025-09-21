import re
from urllib.parse import urlparse

# List of features model was trained on.
# The order is critical! The list of features that is return must match this exact order.
FEATURE_COLUMNS = [
    'NumDots', 'SubdomainLevel', 'PathLevel', 'UrlLength', 'NumDash',
    'NumDashInHostname', 'AtSymbol', 'TildeSymbol', 'NumUnderscore',
    'NumPercent', 'NumQueryComponents', 'NumAmpersand', 'NumHash',
    'NumNumericChars', 'NoHttps', 'RandomString', 'IpAddress',
    'DomainInSubdomains', 'DomainInPaths', 'HttpsInHostname',
    'HostnameLength', 'PathLength', 'QueryLength', 'DoubleSlashInPath',
    'NumSensitiveWords', 'EmbeddedBrandName', 'PctExtHyperlinks',
    'PctExtResourceUrls', 'ExtFavicon', 'InsecureForms', 'RelativeFormAction',
    'ExtFormAction', 'AbnormalFormAction', 'PctNullSelfRedirectHyperlinks',
    'FrequentDomainNameMismatch', 'FakeLinkInStatusBar',
    'RightClickDisabled', 'PopUpWindow', 'SubmitInfoToEmail',
    'IframeOrFrame', 'MissingTitle', 'ImagesOnlyInForm',
    'SubdomainLevelRT', 'UrlLengthRT', 'PctExtResourceUrlsRT',
    'AbnormalExtFormActionR', 'ExtMetaScriptLinkRT',
    'PctExtNullSelfRedirectHyperlinksRT'
]

# This is a sample list of sensitive words often found in phishing URLs.
# For a real-world application, this list would be much larger.
SENSITIVE_WORDS = ["login", "signin", "account", "verify", "update", "secure", "bank"]

def get_url_features(url):
    """
    Extracts all the necessary features from a single URL for model.
    
    Args:
        url (str): The URL string to analyze.

    Returns:
        list: A list of numerical features in the correct order.
    """
    try:
        parsed_url = urlparse(url)
    except ValueError:
        # Handle cases where the URL is malformed
        return [0] * len(FEATURE_COLUMNS) # Return a default list of zeros

    features = {}
    
    # 1. NumDots: Number of dots in the URL
    features['NumDots'] = url.count('.')
    
    # 2. SubdomainLevel: Depth of subdomain nesting
    if parsed_url.hostname:
        features['SubdomainLevel'] = parsed_url.hostname.count('.') - 1
    else:
        features['SubdomainLevel'] = 0

    # 3. PathLevel: Number of directories in the path
    features['PathLevel'] = parsed_url.path.count('/')

    # 4. UrlLength: Total character count of the URL
    features['UrlLength'] = len(url)

    # 5. NumDash: Number of dashes in the URL
    features['NumDash'] = url.count('-')

    # 6. NumDashInHostname: Number of dashes in the hostname
    if parsed_url.hostname:
        features['NumDashInHostname'] = parsed_url.hostname.count('-')
    else:
        features['NumDashInHostname'] = 0
        
    # 7. AtSymbol: Presence of "@" symbol
    features['AtSymbol'] = 1 if '@' in url else 0

    # 8. TildeSymbol: Presence of "~" symbol
    features['TildeSymbol'] = 1 if '~' in url else 0
    
    # 9. NumUnderscore: Presence of "_" symbol
    features['NumUnderscore'] = url.count('_')
    
    # 10. NumPercent: Presence of "%" symbol
    features['NumPercent'] = url.count('%')
    
    # 11. NumQueryComponents: Number of query components
    features['NumQueryComponents'] = parsed_url.query.count('&') + 1 if parsed_url.query else 0

    # 12. NumAmpersand: Number of ampersand symbols
    features['NumAmpersand'] = url.count('&')
    
    # 13. NumHash: Number of hash symbols
    features['NumHash'] = url.count('#')

    # 14. NumNumericChars: Number of numeric characters
    features['NumNumericChars'] = sum(c.isdigit() for c in url)
    
    # 15. NoHttps: Does the URL use HTTPS?
    features['NoHttps'] = 1 if parsed_url.scheme != 'https' else 0

    # 16. RandomString: Is there a random string in the URL? (Simplified)
    # A simple heuristic: check for a long string of mixed characters without separators
    random_str_pattern = re.compile(r'[a-zA-Z0-9]{15,}')
    features['RandomString'] = 1 if random_str_pattern.search(url) else 0

    # 17. IpAddress: Presence of an IP address in the URL
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    features['IpAddress'] = 1 if ip_pattern.search(url) else 0

    # 18. DomainInSubdomains: Whether domain appears in subdomain
    # Will assume a simple check for now.
    features['DomainInSubdomains'] = 0 
    
    # 19. DomainInPaths: Whether domain appears in paths
    features['DomainInPaths'] = 1 if parsed_url.hostname and parsed_url.hostname in parsed_url.path else 0
    
    # 20. HttpsInHostname: Is "https" in the hostname?
    features['HttpsInHostname'] = 1 if 'https' in parsed_url.hostname else 0

    # 21. HostnameLength: Character count of the hostname
    features['HostnameLength'] = len(parsed_url.hostname) if parsed_url.hostname else 0
    
    # 22. PathLength: Character count of the path
    features['PathLength'] = len(parsed_url.path)

    # 23. QueryLength: Character count of the query string
    features['QueryLength'] = len(parsed_url.query)

    # 24. DoubleSlashInPath: Is there a "//" in the path?
    features['DoubleSlashInPath'] = 1 if '//' in parsed_url.path else 0

    # 25. NumSensitiveWords: Number of sensitive words in the URL
    features['NumSensitiveWords'] = sum(1 for word in SENSITIVE_WORDS if word in url.lower())
    
    # The following features are based on the webpage content, not just the URL.
    # For a simple MVP, we will assume these are always 0.
    # In a real-world scenario, would need to fetch the page content and analyze it.
    features['EmbeddedBrandName'] = 0
    features['PctExtHyperlinks'] = 0
    features['PctExtResourceUrls'] = 0
    features['ExtFavicon'] = 0
    features['InsecureForms'] = 0
    features['RelativeFormAction'] = 0
    features['ExtFormAction'] = 0
    features['AbnormalFormAction'] = 0
    features['PctNullSelfRedirectHyperlinks'] = 0
    features['FrequentDomainNameMismatch'] = 0
    features['FakeLinkInStatusBar'] = 0
    features['RightClickDisabled'] = 0
    features['PopUpWindow'] = 0
    features['SubmitInfoToEmail'] = 0
    features['IframeOrFrame'] = 0
    features['MissingTitle'] = 0
    features['ImagesOnlyInForm'] = 0
    features['SubdomainLevelRT'] = 0
    features['UrlLengthRT'] = 0
    features['PctExtResourceUrlsRT'] = 0
    features['AbnormalExtFormActionR'] = 0
    features['ExtMetaScriptLinkRT'] = 0
    features['PctExtNullSelfRedirectHyperlinksRT'] = 0
    
    # Create the final list of features in the correct order.
    # This is critical as the model expects a fixed order.
    final_features_list = [features[col] for col in FEATURE_COLUMNS]
    
    return final_features_list
