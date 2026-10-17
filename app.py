"""
Krititva Web Application
Tagline: Architecting Value. Operationalizing Expertise.
Rooted in the Sanskrit concept of कृतित्व.
"""

import os
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "krititva-dev-secret-key-2026")


@app.route("/")
def index():
    """Renders the main Krititva platform landing page."""
    return render_template("index.html")


@app.route("/opensource-buddy")
def opensource_buddy():
    """Renders the OpenSource Buddy capability-discovery workspace."""
    return render_template("opensource_buddy.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "app": "Krititva", "version": "1.0.0"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
