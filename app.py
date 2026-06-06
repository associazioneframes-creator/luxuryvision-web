import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configurazione chiave API
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_best_model():
    """Trova il miglior modello disponibile evitando errori 404."""
    # Lista prioritaria di modelli da testare
    preferred_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for model in preferred_models:
        if f"models/{model}" in available:
            return model
    return "gemini-1.5-flash" # Fallback

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
    
    prompt = f"""
    Sei un esperto di workflow ComfyUI per il Real Estate.
    L'immagine è la base. Le note dell'utente sono: '{note_utente}'.
    Genera due output separati e pronti per ComfyUI:
    1. POSITIVE PROMPT: [Lista di tag descrittivi professionali]
    2. NEGATIVE PROMPT: [Lista di elementi da escludere]
    """

    try:
        model = genai.GenerativeModel(get_best_model())
        response = model.generate_content([
            prompt,
            {"mime_type": file.mimetype, "data": img_bytes}
        ])
        return jsonify({"prompt": response.text})
    except Exception as e:
        return jsonify({"error": f"Errore AI: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
