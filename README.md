# HTTPS Configuration Checker

A Python utility to check and verify HTTPS configurations, DNS settings, and API endpoint accessibility.

## Features

- DNS resolution check
- DNS server configuration display
- SSL/TLS connection verification
- HTTPS request testing
- Response time measurement
- Server information display

## Requirements

- Python 3.6+
- Required packages: requests


## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/https-config-checker.git
```
2. Install dependencies:
```bash
pip install requests
```

## Usage
1. Run the script:
```bash
python check_https.py
```
2. When prompted, enter the API endpoint you want to check, or press Enter to use the default example endpoint.

## Example Output
HTTPS Configuration Check
==================================================

1. DNS Resolution for api.example.com
✓ IP Address: 192.0.2.1

DNS Servers:
✓ DNS Servers . . . . . . . . . . . : 1.1.1.1
✓ DNS Servers . . . . . . . . . . . : 1.0.0.1

2. SSL/TLS Configuration
✓ SSL Version: TLSv1.3
✓ Cipher: TLS_AES_256_GCM_SHA384

3. HTTPS Request Test
✓ Status Code: 200
✓ Response Time: 0.25 seconds
✓ Server: nginx/1.18.0

Summary:
==================================================
✓ HTTPS configuration appears to be working correctly

## Contributing
Feel free to open issues or submit pull requests for improvements.

## License
MIT License

Would you like me to help you set up the repository with this README and the proper license file?