"""Static server with HTTP Range support (needed for <video> seeking). Run: python serve.py"""
import os, re, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class H(SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        rng = self.headers.get('Range')
        if not rng or not os.path.isfile(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)', rng)
        size = os.path.getsize(path)
        start = int(m.group(1)) if m.group(1) else max(0, size - int(m.group(2)))
        end = int(m.group(2)) if m.group(1) and m.group(2) else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416); return None
        f = open(path, 'rb'); f.seek(start)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        self._left = end - start + 1
        return f
    def copyfile(self, src, dst):
        left = getattr(self, '_left', None)
        if left is None:
            return super().copyfile(src, dst)
        while left > 0:
            chunk = src.read(min(65536, left))
            if not chunk: break
            dst.write(chunk); left -= len(chunk)
    def end_headers(self):
        if 'Accept-Ranges' not in self._headers_buffer_str():
            self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()
    def _headers_buffer_str(self):
        return b''.join(self._headers_buffer).decode('latin-1') if hasattr(self, '_headers_buffer') else ''

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
print(f'http://127.0.0.1:{port}/index.html')
ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
