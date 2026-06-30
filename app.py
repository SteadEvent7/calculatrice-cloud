from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def calculate(num1, num2, operation):
    if operation == "add":
        return num1 + num2
    if operation == "subtract":
        return num1 - num2
    if operation == "multiply":
        return num1 * num2
    if operation == "divide":
        if num2 == 0:
            raise ZeroDivisionError("Division par zéro impossible.")
        return num1 / num2
    raise ValueError("Opération invalide.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Données invalides."}), 400

    try:
        num1 = float(data.get("num1", ""))
        num2 = float(data.get("num2", ""))
    except (TypeError, ValueError):
        return jsonify({"error": "Veuillez saisir des nombres valides."}), 400

    operation = data.get("operation", "")
    if operation not in ("add", "subtract", "multiply", "divide"):
        return jsonify({"error": "Veuillez sélectionner une opération valide."}), 400

    try:
        result = calculate(num1, num2, operation)
    except ZeroDivisionError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
