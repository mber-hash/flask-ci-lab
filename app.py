import os

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Hello, DevOps!"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/info")
def info():
    return jsonify(
        {"version": os.getenv("APP_VERSION", "1.0.0"), "environment": os.getenv("ENVIRONMENT", "development")}
    )


@app.route("/api/calc")
def calc():
    a = request.args.get("a")
    b = request.args.get("b")
    op = request.args.get("op")

    if not a or not b or not op:
        return jsonify({"error": "missing parameters"}), 400

    try:
        a_float = float(a)
        b_float = float(b)
    except ValueError:
        return jsonify({"error": "invalid number"}), 400

    if op == "add":
        res = a_float + b_float
    elif op == "sub":
        res = a_float - b_float
    elif op == "mul":
        res = a_float * b_float
    else:
        return jsonify({"error": "unknown operation"}), 400

    return jsonify({"result": res, "operation": op})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
