#!/usr/bin/env python3
"""
KB Manager — Server locale per macOS

Avvia con:
    python3 launcher_server.py

Poi apri http://localhost:8765 nel browser.

Endpoint:
    POST /api/open         -> apre app esterne (Finder, VSCode, Obsidian, Ghostty)
    POST /api/mkdir        -> crea directory
    POST /api/list-parent  -> elenca le directory nel path madre
    POST /api/sizes        -> dimensioni di più cartelle
    POST /api/last-update  -> ultimo aggiornamento per path
    POST /api/log          -> ultima sezione di log.md
"""

import json
import os
import subprocess
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8765
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def format_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes_val) < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def format_time_ago(timestamp):
    import time
    diff = time.time() - timestamp
    if diff < 60:
        return "just now"
    elif diff < 3600:
        m = int(diff // 60)
        return f"{m} min ago"
    elif diff < 86400:
        h = int(diff // 3600)
        return f"{h} hour ago" if h == 1 else f"{h} hours ago"
    elif diff < 604800:
        d = int(diff // 86400)
        return f"{d} day ago" if d == 1 else f"{d} days ago"
    elif diff < 2592000:
        w = int(diff // 604800)
        return f"{w} week ago" if w == 1 else f"{w} weeks ago"
    elif diff < 31536000:
        mo = int(diff // 2592000)
        return f"{mo} month ago" if mo == 1 else f"{mo} months ago"
    else:
        y = int(diff // 31536000)
        return f"{y} year ago" if y == 1 else f"{y} years ago"


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.path = "/kb_manager.html"
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/open":
            self._handle_open()
        elif self.path == "/api/mkdir":
            self._handle_mkdir()
        elif self.path == "/api/list-parent":
            self._handle_list_parent()
        elif self.path == "/api/sizes":
            self._handle_sizes()
        elif self.path == "/api/last-update":
            self._handle_last_update()
        elif self.path == "/api/log":
            self._handle_log()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    def _handle_open(self):
        try:
            data = self._read_json()
            action = data.get("action")
            path = data.get("path", "")
            vault = data.get("vault", "")

            if action == "finder":
                subprocess.run(["open", path], check=True)
            elif action == "vscode":
                subprocess.run(["code", path], check=True)
            elif action == "obsidian":
                vault_name = vault or os.path.basename(path)
                uri = f"obsidian://open?vault={urllib.parse.quote(vault_name)}"
                subprocess.run(["open", uri], check=True)
            elif action == "ghostty":
                subprocess.run(["open", "-a", "Ghostty", path], check=True)
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Unknown action")
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _handle_mkdir(self):
        try:
            data = self._read_json()
            path = data.get("path", "")
            if not path:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing path")
                return
            os.makedirs(path, exist_ok=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _handle_list_parent(self):
        try:
            data = self._read_json()
            parent_path = data.get("parentPath", "")
            if not parent_path:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing parentPath")
                return
            if not os.path.isdir(parent_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"directories": []}).encode())
                return
            entries = []
            for entry in os.listdir(parent_path):
                if entry.startswith("."):
                    continue
                full = os.path.join(parent_path, entry)
                if os.path.isdir(full):
                    entries.append(entry)
            entries.sort()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"directories": entries}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _handle_sizes(self):
        try:
            data = self._read_json()
            paths = data.get("paths", [])
            sizes = {}
            for path in paths:
                try:
                    result = subprocess.run(
                        ["du", "-sk", path],
                        capture_output=True, text=True, check=True
                    )
                    kb = int(result.stdout.split()[0])
                    sizes[path] = format_size(kb * 1024)
                except Exception:
                    sizes[path] = "--"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"sizes": sizes}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _handle_last_update(self):
        try:
            data = self._read_json()
            paths = data.get("paths", [])
            updates = {}
            for path in paths:
                updates[path] = self._get_last_update(path)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"lastUpdates": updates}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _get_last_update(self, path):
        search_path = path
        wiki_path = os.path.join(path, "wiki")
        if os.path.isdir(wiki_path):
            search_path = wiki_path
        latest = 0
        try:
            for root, dirs, files in os.walk(search_path):
                for f in files:
                    if f.startswith("."):
                        continue
                    full = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(full)
                        if mtime > latest:
                            latest = mtime
                    except Exception:
                        pass
        except Exception:
            pass
        if latest == 0:
            return {"text": "--", "ts": 0}
        return {"text": format_time_ago(latest), "ts": latest}

    def _handle_log(self):
        try:
            data = self._read_json()
            paths = data.get("paths", [])
            logs = {}
            for path in paths:
                logs[path] = self._get_log(path)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"logs": logs}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _get_log(self, path):
        log_path = os.path.join(path, "wiki", "log.md")
        if not os.path.isfile(log_path):
            return "No log found"
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return "No log found"
        import re
        matches = list(re.finditer(r"^##\s*\[(\d{4}-\d{2}-\d{2})\]", content, re.MULTILINE))
        if not matches:
            return "No log found"
        # pick the most recent date
        latest_match = max(matches, key=lambda m: m.group(1))
        start = latest_match.start()
        # extract until next section heading or end of file
        idx = matches.index(latest_match)
        if idx + 1 < len(matches):
            end = matches[idx + 1].start()
            section = content[start:end]
        else:
            section = content[start:]
        return section.strip()

    def log_message(self, format, *args):
        # Silenzia i log di accesso
        pass


def main():
    os.chdir(ROOT_DIR)
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"=" * 50)
    print(f"  KB Manager Server")
    print(f"=" * 50)
    print(f"  URL:     http://localhost:{PORT}")
    print(f"  Root:    {ROOT_DIR}")
    print(f"  Stop:    Ctrl+C")
    print(f"=" * 50)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
