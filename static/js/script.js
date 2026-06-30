document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("calc-form");
    const resetBtn = document.getElementById("reset-btn");
    const resultPanel = document.getElementById("result-panel");
    const resultValue = document.getElementById("result-value");
    const errorPanel = document.getElementById("error-panel");
    const errorMessage = document.getElementById("error-message");
    const submitBtn = form.querySelector('button[type="submit"]');

    function hideMessages() {
        resultPanel.classList.add("hidden");
        errorPanel.classList.add("hidden");
    }

    function showResult(value) {
        hideMessages();
        resultValue.textContent = value;
        resultPanel.classList.remove("hidden");
    }

    function showError(message) {
        hideMessages();
        errorMessage.textContent = message;
        errorPanel.classList.remove("hidden");
    }

    function formatResult(num) {
        if (Number.isInteger(num)) {
            return num.toString();
        }
        return parseFloat(num.toFixed(10)).toString();
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideMessages();

        const num1 = document.getElementById("num1").value.trim();
        const num2 = document.getElementById("num2").value.trim();
        const operation = document.getElementById("operation").value;

        if (!num1 || !num2) {
            showError("Veuillez saisir les deux nombres.");
            return;
        }

        if (!operation) {
            showError("Veuillez sélectionner une opération.");
            return;
        }

        submitBtn.disabled = true;

        try {
            const response = await fetch("/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({ num1, num2, operation }),
            });

            let data;
            const contentType = response.headers.get("content-type") || "";
            if (contentType.includes("application/json")) {
                data = await response.json();
            } else {
                showError(
                    response.status === 404
                        ? "Route introuvable. Vérifiez que l'application Flask tourne (Web Service sur Render, pas un site statique)."
                        : "Réponse serveur invalide. Lancez l'app avec : python app.py"
                );
                return;
            }

            if (!response.ok) {
                showError(data.error || "Une erreur est survenue.");
                return;
            }

            showResult(formatResult(data.result));
        } catch {
            showError("Impossible de contacter le serveur. Lancez Flask avec : python app.py");
        } finally {
            submitBtn.disabled = false;
        }
    });

    resetBtn.addEventListener("click", () => {
        form.reset();
        hideMessages();
    });
});
