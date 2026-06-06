import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configurazione chiave API
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_available_model():
    """Cerca automaticamente un modello valido tra quelli disponibili."""
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Preferiamo i modelli Flash per velocità e compatibilità
            if 'flash' in m.name:
                return m.name
    return "gemini-1.5-flash" # Fallback di sicurezza

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "image" not in request.files:
        return jsonify({"error": "Nessuna immagine caricata"}), 400

    file = request.files["image"]
    img_bytes = file.read()
    
    try:
        # Selezioniamo il modello dinamicamente
        model_name = get_available_model()
        model = genai.GenerativeModel(model_name)
        
        prompt = "Sei LuxuryVision AI, un esperto real estate. Analizza la foto e genera solo un prompt professionale per valorizzarla."

        response = model.generate_content([
            prompt,
            {"mime_type": file.mimetype, "data": img_bytes}
        ])
        return jsonify({"prompt": response.text})
        
    except Exception as e:
        print(f">>> ERRORE CRITICO: {str(e)}")
        return jsonify({"error": f"Errore durante l'analisi: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
