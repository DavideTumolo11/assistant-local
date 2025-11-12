from flask import Flask, request, jsonify
from memory_semantic import SemanticMemory

app = Flask(__name__)
memory = SemanticMemory()

@app.route("/add_memory", methods=["POST"])
def add_memory():
    """Aggiunge un concetto alla memoria"""
    data = request.get_json()
    text = data.get("text", "")
    if text:
        memory.add(text)
        return jsonify({"status": "ok", "message": f"Aggiunto: {text}"})
    return jsonify({"status": "error", "message": "Nessun testo fornito"}), 400

@app.route("/query_memory", methods=["POST"])
def query_memory():
    """Cerca concetti simili nella memoria"""
    data = request.get_json()
    query = data.get("query", "")
    if query:
        results = memory.query(query)
        return jsonify({"status": "ok", "results": results})
    return jsonify({"status": "error", "message": "Nessuna query fornita"}), 400

if __name__ == "__main__":
    app.run(port=5000)
