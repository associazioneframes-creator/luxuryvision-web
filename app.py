print(">>> STO ESEGUENDO QUESTO FILE APP.PY <<<")

import os
import base64
from flask import Flask, render_template, request, jsonify
import google.genai as genai

app = Flask(__name__)

# Configurazione Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY non trovata nelle variabili d'ambiente.")

client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    if "image" not in request.files:
        return jsonify({"error": "Nessuna immagine caricata"}), 400

    file = request.files["image"]
    img_bytes = file.read()
    mime = file.mimetype

    # Controllo dimensione (opzionale, ma consigliato per Render)
    if len(img_bytes) > 5 * 1024 * 1024:  # Limite 5MB
        return jsonify({"error": "Immagine troppo grande (max 5MB)"}), 400

    # Conversione in Base64 (Richiesta dall'SDK Google GenAI)
    encoded_image = base64.b64encode(img_bytes).decode('utf-8')

    prompt = """
    Sei LuxuryVision AI, un assistente esperto in real estate. 
    Analizza questa immagine e genera SOLO il PROMPT professionale finale per migliorare la foto, 
    senza spiegazioni o introduzioni. Se l'immagine non è una foto immobiliare, avvisa gentilmente.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        return jsonify({"prompt": response.text})

    except Exception as e:
        print(f">>> ERRORE GEMINI: {str(e)}")
        return jsonify({"error": "Errore durante l'analisi AI"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)