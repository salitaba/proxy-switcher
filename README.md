# proxy-switcher

HTTP, SOCKS4, SOCKS5 proxies scraper and swithcer.

- Can determine if the proxy is anonymous.
- Supports determining the geolocation of the proxy exit node.
- Can sort proxies by speed.
- Uses regex to find proxies of format `protocol://username:password@ip:port` on a web page or in a local file, allowing proxies to be extracted even from json without code changes.
- Supports proxies with authentication.
- It is possible to specify the URL to which to send a request to check the proxy.
- Supports saving to plain text and json.
- Asynchronous.
- Proxy switcher

You can get proxies obtained using this project in [monosans/proxy-list](https://github.com/monosans/proxy-list).

### Usage

After running the Docker image, the server runs on port 8000. Every request is proxied to the host specified in the target_url cookie.  

## Installation


- Install `Docker`.
- Download and unpack [the archive with the program](https://github.com/monosans/proxy-scraper-checker/archive/refs/heads/main.zip).
- Edit `config.toml` to your preference.
- Run the following commands:
  ```bash
  docker build -t proxy
  docker run -t proxy 
  ```

## Something else?

All other info is available in `config.toml` file.

## License

[MIT](LICENSE)

This product includes GeoLite2 Data created by MaxMind, available from <https://www.maxmind.com>.
