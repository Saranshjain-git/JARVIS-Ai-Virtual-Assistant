from flask import Flask, render_template, request, jsonify
import os
import sys
import traceback

# =========================
# IMPORT JARVIS
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)

import main as jarvis

# =========================
# FLASK APP
# =========================

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# =========================
# COMMAND ROUTE
# =========================

@app.route(
    "/command",
    methods=["POST"]
)
def command():

    try:

        data = request.get_json()

        user_command = data.get(
            "command",
            ""
        )

        print("\n====================")

        print(
            "BROWSER COMMAND =",
            user_command
        )

        if user_command:

            print(
                "RAW =",
                user_command
            )

            try:

                result = jarvis.handle_command(
                    user_command.lower()
                )

                print(
                    "RESULT =",
                    result
                )

            except Exception as e:

                print(
                    "\nHANDLE COMMAND ERROR:"
                )

                traceback.print_exc()

                return jsonify({
                    "status": "error",
                    "message": str(e)
                })

        return jsonify({
            "status": "success",
            "message": f"Executed: {user_command}"
        })

    except Exception as e:

        print(
            "\nCOMMAND ERROR:"
        )

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    print(
        "\nFlask server running on:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )