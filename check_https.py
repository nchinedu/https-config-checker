import requests
import socket
import ssl
from urllib.parse import urlparse

def check_https_configuration(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 443

        # Check DNS resolution
        print(f"\n1. DNS Resolution for {hostname}")
        ip_address = socket.gethostbyname(hostname)
        print(f"✓ IP Address: {ip_address}")

         # Add DNS server check
        print("\nDNS Servers:")
        import subprocess
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'DNS Servers' in line:
                print(f"✓ {line.strip()}")
                
        # Check SSL/TLS connection
        print("\n2. SSL/TLS Configuration")
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"✓ SSL Version: {ssock.version()}")
                print(f"✓ Cipher: {ssock.cipher()[0]}")

        # Test HTTPS request
        print("\n3. HTTPS Request Test")
        response = requests.get(url, timeout=10)
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response Time: {response.elapsed.total_seconds():.2f} seconds")
        print(f"✓ Server: {response.headers.get('Server', 'N/A')}")

        return True

    except socket.gaierror:
        print("✗ DNS resolution failed. Check your network connection.")
    except ssl.SSLError as e:
        print(f"✗ SSL/TLS error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"✗ HTTPS request failed: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")
    
    return False

if __name__ == "__main__":
    print("HTTPS Configuration Check")
    print("=" * 50)
    
    # Get API endpoint from user or use default
    api_url = input("Enter API endpoint to check (or press Enter for default example): ").strip()
    if not api_url:
        api_url = "https://api.example.com"
        print(f"Using default endpoint: {api_url}")
    
    success = check_https_configuration(api_url)
    
    print("\nSummary:")
    print("=" * 50)
    if success:
        print("✓ HTTPS configuration appears to be working correctly")
    else:
        print("✗ HTTPS configuration check failed")