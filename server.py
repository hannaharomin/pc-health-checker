"""
server.py — Tiny web server for PC Health Checker
Run this file, then open http://localhost:8000 in your browser.

Usage:
    python server.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import health_checker


class HealthHandler(SimpleHTTPRequestHandler):
    """Handles web requests from the browser."""

    def do_GET(self):
        # When the browser asks for /check, run our health checks
        if self.path == '/check':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # This line allows the HTML file to talk to our server
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Run all the checks and send back the results as JSON
            report = health_checker.run_all_checks()
            self.wfile.write(json.dumps(report).encode())

        else:
            # For everything else (like loading index.html), serve the file normally
            super().do_GET()

    def log_message(self, format, *args):
        # Show a simple message in the terminal when a request comes in
        print(f"  → {self.address_string()} requested {args[0]}")


if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), HealthHandler)
    print(f"\n🖥️  PC Health Checker server is running!")
    print(f"   Open your browser and go to: http://localhost:{PORT}/index.html")
    print(f"   Press Ctrl+C to stop the server.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
