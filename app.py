from flask import Flask, render_template, request, jsonify
import sympy as sp
import subprocess
import re
import math

app = Flask(__name__)

# Mathematical symbols
x = sp.Symbol("x")

def calculate(expression):
    try:
        expression = expression.strip()

        # Replace calculator symbols
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")
        expression = expression.replace("π", "pi")
        expression = expression.replace("√", "sqrt")

        # Scientific functions
        allowed = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "sqrt": sp.sqrt,
            "log": sp.log,
            "ln": sp.log,
            "exp": sp.exp,
            "abs": abs,
            "pi": sp.pi,
            "e": sp.E,
            "x": x
        }

        result = sp.sympify(expression, locals=allowed)

        # Numerical result
        numerical = sp.N(result)

        return {
            "success": True,
            "result": str(numerical),
            "exact": str(result)
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def ai_assistant(message):
    text = message.lower().strip()

    # Remove common command words
    cleaned = text

    phrases = [
        "calculate",
        "solve",
        "what is",
        "what's",
        "find",
        "compute",
        "evaluate"
    ]

    for phrase in phrases:
        cleaned = cleaned.replace(phrase, "")

    cleaned = cleaned.strip()

    # Convert spoken mathematics
    replacements = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "divided by": "/",
        "over": "/",
        "power": "^",
        "squared": "^2",
        "cubed": "^3",
        "square root of": "sqrt",
        "sine": "sin",
        "cosine": "cos",
        "tangent": "tan",
        "pi": "pi"
    }

    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    # Greetings
    if any(word in text for word in ["hello", "hi", "hey"]):
        return {
            "answer": "Hello! I am your AI Calculator Assistant. Ask me a mathematics question or tell me a calculation.",
            "calculation": False
        }

    # Help
    if "help" in text or "what can you do" in text:
        return {
            "answer": (
                "I can solve scientific calculations, powers, roots, "
                "trigonometry, logarithms, and mathematical expressions. "
                "You can type or speak a command."
            ),
            "calculation": False
        }

    # Try solving the message
    result = calculate(cleaned)

    if result["success"]:
        return {
            "answer": f"The answer is {result['result']}",
            "calculation": True,
            "result": result["result"]
        }

    return {
        "answer": (
            "I could not understand that command. Try saying "
            "'calculate 25 multiplied by 8' or type a mathematical expression."
        ),
        "calculation": False
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculator():
    data = request.get_json()
    expression = data.get("expression", "")

    return jsonify(calculate(expression))


@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    message = data.get("message", "")

    return jsonify(ai_assistant(message))


@app.route("/voice", methods=["POST"])
def voice():
    try:
        command = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True,
            timeout=30
        )

        spoken_text = command.stdout.strip()

        if spoken_text:
            return jsonify({
                "success": True,
                "text": spoken_text
            })

        return jsonify({
            "success": False,
            "error": "No speech was detected."
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        })


@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    try:
        subprocess.Popen([
            "termux-tts-speak",
            text
        ])

        return jsonify({"success": True})

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
 
