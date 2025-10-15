"""
Simple HTTP server to preview generated HTML resumes.

Usage:
    python scripts/preview_server.py [port]
    
Then open http://localhost:8000/docs/ in your browser.
"""

import http.server
import socketserver
import sys
import webbrowser
import os
from pathlib import Path

def start_server(port=8000):
    """Start a simple HTTP server for previewing resumes."""
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Starting preview server at http://localhost:{port}")
            print(f"erving files from: {project_root}")
            print(f"View your resume at: http://localhost:{port}/")
            print("Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{port}/")
            except:
                pass
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Try a different port:")
            print(f"   python scripts/preview_server.py {port + 1}")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8000.")
    
    start_server(port)