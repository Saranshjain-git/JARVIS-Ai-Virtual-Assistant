from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# COMMAND ROUTE
# =========================

@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()

    user_command = data.get("command", "")

    print("Command:", user_command)

    return jsonify({
        "status": "success",
        "message": f"Command received: {user_command}\n\n⚠ Desktop features work in the local Windows version of JARVIS."
    })

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )