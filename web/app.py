from flask import Flask, render_template, request, jsonify
import os
import sys
import traceback

app = Flask(__name__)

# =========================
# CHECK IF RUNNING ON RENDER
# =========================

IS_RENDER = os.environ.get("RENDER") == "true"

jarvis = None

if not IS_RENDER:
    try:
        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        sys.path.append(BASE_DIR)

        import main as jarvis
        print("AFTER IMPORT")
        print(jarvis)

        print("Local JARVIS Loaded Successfully")

    except Exception as e:
        print("Jarvis Import Error:")
        traceback.print_exc()

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# COMMAND
# =========================

@app.route("/command", methods=["POST"])
def command():

    try:

        data = request.get_json()

        user_command = data.get("command", "")

        print("Command:", user_command)

        # LOCAL WINDOWS
        if jarvis is not None:

            result = jarvis.handle_command(
                user_command.lower()
            )

            return jsonify({
                "status": "success",
                "message": result if result else "Command Executed"
            })

        # RENDER
        else:

            return jsonify({
                "status": "success",
                "message": f"Command received: {user_command}\n\nDesktop automation works only in the local Windows version."
            })

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# =========================
# RUN
# =========================

if __name__ == "__main__":
    print("STARTING FLASK")

    app.run(
    host="127.0.0.1",
    port=5001,
    debug=False,
    use_reloader=False
)