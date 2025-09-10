"""Generic HTTP server utilities for serving static files.

Provides a reusable HTTP server with features like:
- Extensionless URL support (serves /foo as /foo.html)
- Cache control options
- Request logging control
- Address reuse to avoid "address already in use" errors
"""

import http.server
import socketserver
import os
from functools import partial
from typing import Optional, Callable, Any


class ReusableTCPServer(socketserver.TCPServer):
    """TCP server that allows address reuse to avoid 'Address already in use' errors."""
    allow_reuse_address = True


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with extensionless URL support and cache control.
    
    Features:
    - Serves /foo as /foo.html if the HTML file exists
    - Optional cache disabling for development
    - Optional request logging control
    """
    
    def __init__(self, *args, **kwargs):
        self.disable_cache = kwargs.pop("disable_cache", False)
        self.log_requests = kwargs.pop("log_requests", True)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests with extensionless URL support."""
        # Parse the requested path
        path = self.path
        # Check if the path has no extension
        if not os.path.splitext(path)[1]:
            # Append '.html' to the path
            new_path = f"{path}.html"
            # Construct the full file path
            full_path = os.path.join(self.directory, new_path.lstrip("/"))
            # Check if the .html file exists
            if os.path.exists(full_path):
                self.path = new_path  # Update the path to the .html file
        # Call the superclass method to handle the request
        return super().do_GET()

    def end_headers(self):
        """Add cache control headers if cache is disabled."""
        if self.disable_cache:
            # Disable caching by setting appropriate headers
            self.send_header(
                "Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate"
            )
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Surrogate-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args):
        """Override to control request logging."""
        if not self.log_requests:
            return
        return super().log_message(format, *args)


def start_server(
    host: str,
    port: int,
    directory: str,
    disable_cache: bool = False,
    quiet_requests: bool = False,
    handler_class: Optional[Callable[..., Any]] = None,
) -> None:
    """Start an HTTP server to serve static files.
    
    Args:
        host: Host interface to bind to (e.g., "127.0.0.1", "0.0.0.0")
        port: Port number to listen on
        directory: Directory to serve files from
        disable_cache: If True, send no-cache headers
        quiet_requests: If True, suppress per-request log messages
        handler_class: Optional custom handler class (defaults to CustomHTTPRequestHandler)
        
    Raises:
        ValueError: If directory doesn't exist or isn't a directory
        OSError: If server can't bind to the specified host/port
    """
    # Fail fast on invalid directory
    if not os.path.isdir(directory):
        raise ValueError(f"Directory is missing or not a directory: {directory}")
    
    if handler_class is None:
        handler_class = CustomHTTPRequestHandler
        
    handler = partial(
        handler_class,
        directory=directory,
        disable_cache=disable_cache,
        log_requests=not quiet_requests,
    )
    
    with ReusableTCPServer((host, port), handler) as httpd:
        print(f"Serving at http://{host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
        finally:
            httpd.server_close()