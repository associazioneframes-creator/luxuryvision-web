import os
import base64
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configurazione chiave API
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY non trovata nelle variabili d'ambiente.")

genai.configure(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "image" not in request.files:
        return jsonify({"error": "Nessuna immagine caricata"}), 400

    file = request.files["image"]
    # Leggiamo i dati e li trasformiamo in un formato compatibile
    img_bytes = file.read()
    
    model = genai.GenerativeModel("gemini-1.5-flash") # Usiamo 1.5-flash per massima compatibilità
    
    prompt = """
    Sei LuxuryVision AI, un assistente esperto in real estate. 
    Analizza questa immagine e genera SOLO il PROMPT professionale finale per migliorare la foto, 
    senza spiegazioni o introduzioni. Se l'immagine non è una foto immobiliare, avvisa gentilmente.
    """

    try:
        # Passiamo i dati come dizionario esplicito
        response = model.generate_content([
            prompt,
            {"mime_type": file.mimetype, "data": img_bytes}
        ])
        return jsonify({"prompt": response.text})

    except Exception as e:
        print(f">>> ERRORE DETTAGLIATO GEMINI: {str(e)}")
        return jsonify({"error": f"Errore AI: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)