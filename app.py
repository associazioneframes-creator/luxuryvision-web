from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    image = request.files["image"]

    # Per ora solo demo: in futuro qui mettiamo la vera AI
    result = f"Prompt generato per: {image.filename}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()
