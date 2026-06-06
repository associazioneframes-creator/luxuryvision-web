import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configurazione chiave API
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "image" not in request.files:
        return jsonify({"error": "Nessuna immagine"}), 400

    file = request.files["image"]
    img_bytes = file.read()
    
    # Usiamo gemini-1.5-flash
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = "Sei un esperto real estate. Genera un prompt professionale per migliorare questa foto."

    try:
        response = model.generate_content([
            prompt,
            {"mime_type": file.mimetype, "data": img_bytes}
        ])
        return jsonify({"prompt": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
