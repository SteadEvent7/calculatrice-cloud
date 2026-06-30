from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

VALID_OPERATIONS = ("add", "subtract", "multiply", "divide")


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


def parse_calculation_request(data):
    if not data:
        return None, None, None, "Données invalides.", 400

    try:
        num1 = float(data.get("num1", ""))
        num2 = float(data.get("num2", ""))
    except (TypeError, ValueError):
        return None, None, None, "Veuillez saisir des nombres valides.", 400

    operation = data.get("operation", "")
    if operation not in VALID_OPERATIONS:
        return None, None, None, "Veuillez sélectionner une opération valide.", 400

    try:
        result = calculate(num1, num2, operation)
    except (ZeroDivisionError, ValueError) as e:
        return num1, num2, operation, str(e), 400

    return num1, num2, operation, result, 200


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate_route():
    if request.is_json:
        data = request.get_json(silent=True)
    else:
        data = request.form

    num1, num2, operation, outcome, status = parse_calculation_request(data)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if status != 200:
            return jsonify({"error": outcome}), status
        return jsonify({"result": outcome})

    return render_template(
        "index.html",
        result=outcome if status == 200 else None,
        error=outcome if status != 200 else None,
        num1=data.get("num1", "") if data else "",
        num2=data.get("num2", "") if data else "",
        operation=data.get("operation", "") if data else "",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
