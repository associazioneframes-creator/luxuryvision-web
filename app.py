from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "LuxuryVision Online è attivo."

@app.route("/prompt", methods=["POST"])
def genera_prompt():
    # qui in futuro puoi usare la logica reale di LuxuryVision
    return jsonify({
        "positivo": "Riordina la stanza, aumenta la luminosità del 50%, mantieni mobili e struttura intatti.",
        "negativo": "Non aggiungere oggetti nuovi, non cambiare colori o materiali, non modificare la geometria."
    })

if __name__ == "__main__":
    app.run()
