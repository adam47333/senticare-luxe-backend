from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# ✅ Haalt je OpenAI key veilig op uit Render (env var)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        if not message:
            return jsonify({"reply": "Geen bericht ontvangen."}), 400

        prompt = f"Je bent een empathische AI-psycholoog. De gebruiker zegt: '{message}'. Reageer warm, begrijpelijk en stel een reflecterende vraag."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Fout:", e)
        return jsonify({"reply": "Er ging iets mis bij het ophalen van een reactie."}), 500

# ✅ Nodig voor Render om verbinding te maken
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render detecteert poort
    app.run(host="0.0.0.0", port=port)
