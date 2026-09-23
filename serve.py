#!/usr/bin/env python3
"""PassGuard local preview server. No passwords leave this machine."""

from __future__ import print_function

import os
import sys

try:
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import ThreadingMixIn
    from BaseHTTPServer import HTTPServer

    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True


ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8080"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        try:
            super(Handler, self).__init__(*args, directory=ROOT, **kwargs)
        except TypeError:
            os.chdir(ROOT)
            SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[PassGuard] %s\n" % (fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        SimpleHTTPRequestHandler.end_headers(self)


def main():
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print("PassGuard vault is live.")
    print("Open in browser:  http://127.0.0.1:%s/" % PORT)
    print("Evaluation lab:   http://127.0.0.1:%s/evaluate.html" % PORT)
    print("Scoring method:   http://127.0.0.1:%s/method.html" % PORT)
    print("Stop with Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nVault sealed.")


if __name__ == "__main__":
    main()
