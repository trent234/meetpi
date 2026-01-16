#!/usr/bin/env python3
import os
from bottle import Bottle, request, template, run, static_file
from .main import generate_jwt

app = Bottle()

INDEX_HTML = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MeetPi</title>
    <link rel="icon" href="/static/logo.png">
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>
    <header class="site-header">
      <img src="/static/logo.png" alt="MeetPi" class="logo">
      <h1>Generate Jitsi URL</h1>
    </header>
    <form action="/generate" method="post">
      <button class="btn" type="submit">Generate Room &amp; URL</button>
    </form>
  </body>
</html>
"""

RESULT_HTML = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MeetPi — Result</title>
    <link rel="icon" href="/static/logo.png">
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body>
    <header class="site-header">
      <img src="/static/logo.png" alt="MeetPi" class="logo">
      <h1>Room created</h1>
    </header>
    <div class="container">
      <p><button class="btn" id="copyBtn" data-url="{{url}}" type="button">Copy Join Link</button></p>
      <p><a class="btn secondary" href="/">Generate another</a></p>
      <p id="copyMsg" style="transition:opacity .2s;opacity:0;color:var(--muted-text);text-align:center;margin-top:8px;"></p>
    </div>
    <script src="/static/app.js" defer></script>
  </body>
</html>
"""

@app.get("/static/<filename>")
def static(filename):
    root = os.path.join(os.path.dirname(__file__), "static")
    return static_file(filename, root=root)

@app.get("/")
def index():
    return INDEX_HTML

@app.post("/generate")
def generate():
    # generate_jwt() returns (room, token)
    room, token = generate_jwt()
    url = f"https://meet.trentwilson.com/{room}?jwt={token}"
    return template(RESULT_HTML, url=url)

if __name__ == "__main__":
    # Default development port; the container can expose/forward as needed.
    run(app, host="0.0.0.0", port=8080)
