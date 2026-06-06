import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configurazione chiave API (prende il valore da Render)
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_best_model():
    return "gemini-1.5-flash"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "image" not in request.files:
        return jsonify({"error": "Nessuna immagine"}), 400

    file = request.files["image"]
    note_utente = request.form.get("notes", "Nessuna nota aggiuntiva.")
    img_bytes = file.read()
    
    prompt = f"Sei un esperto di workflow ComfyUI. Note utente: '{note_utente}'. Genera POSITIVE e NEGATIVE prompt."

    try:
        model = genai.GenerativeModel(get_best_model())
        response = model.generate_content([prompt, {"mime_type": file.mimetype, "data": img_bytes}])
        return jsonify({"prompt": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
