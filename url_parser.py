from urllib.parse import urlparse, parse_qs

def parse_url(url):
    """Parse URL into structured components with clean output"""
    parsed = urlparse(url)
    query_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}
    
    return {
        'protocol': parsed.scheme or "None",
        'domain': parsed.netloc or "None",
        'path': parsed.path or "/",
        'query_params': query_params or "None"
    }

def display_url_analysis(url_data):
    """Print URL components in organized columns"""
    print("\n" + "=" * 50)
    print("{:<12} {:<15} {}".format("COMPONENT", "TYPE", "VALUE"))
    print("-" * 50)
    print("{:<12} {:<15} {}".format("Protocol", url_data['protocol'].upper(), 
          f"🔒 (Secure)" if url_data['protocol'] == 'https' else "⚠️ (Unsecure)"))
    print("{:<12} {:<15} {}".format("Domain", "FQDN", url_data['domain']))
    print("{:<12} {:<15} {}".format("Path", "Resource", url_data['path']))
    
    if url_data['query_params'] != "None":
        print("\n{:<12} {:<15} {}".format("PARAMETER", "VALUE", "TYPE"))
        print("-" * 50)
        for param, value in url_data['query_params'].items():
            val_type = "single" if not isinstance(value, list) else f"list[{len(value)}]"
            print("{:<12} {:<15} {}".format(param, str(value), val_type))
    print("=" * 50)

# Example usage
if __name__ == "__main__":
    sample_url = "https://tipsboard.net/what-is-the-first-iphone-to-have-wireless-charging/"
    parsed_data = parse_url(sample_url)
    display_url_analysis(parsed_data)