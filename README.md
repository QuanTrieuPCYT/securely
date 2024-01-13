# securely
Simple, no HTTPS, no bullshit, straight to the point and easy to use reverse proxy server with basic authentication, all configurable in a simple [`config.json`](config.json) file.

Pair this with your existing app to add basic authentication for testing without modifying their code!

Please include HTTPS support with a proper external webserver (or Cloudflare Tunnel, I personally recommend this one) if you're intending to expose this to the internet. Might include a simple HTTP rate-limiter in the future, configurable via config file.
## Features
- Lightweight as hell, using Python's built-in libraries.
- Redirects all headers to make requests look like it's coming directly to the target server.
- Detailed logging.
- Configurable via the [`config.json`](config.json) file.
- No bullshit and straight to the point 🚀.
## Usage
- Make sure to have Python 3 installed.
- Clone this repository via `git` if you have that installed
```
git clone https://github.com/QuanTrieuPCYT/securely
```
or just download this repository as a ZIP file and extract it (some will do).
- Run the thing in a terminal.
```
python3 main.py
```