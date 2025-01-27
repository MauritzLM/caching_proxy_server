# Caching Proxy Server

This is a small project for roadmap.sh on the backend path.

## Notes

- The server starts by typing: caching-proxy --port <number> --origin <url> into the terminal on the provided port.
- Get requests are forwarded to the origin url if there is no cached response for that request. Otherwise the cached response is returned.
