from flask import Flask, jsonify
import os


app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify({"message": "Hello, CI/CD!"})


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


@app.route('/info')
def info():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development")
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
