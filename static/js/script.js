document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("transaction-form");
  const submitButton = document.getElementById("submit-button");
  const submitText = document.getElementById("submit-text");
  const submitSpinner = document.getElementById("submit-spinner");

  const sliders = [
    { input: document.getElementById("transaction_hour"), output: document.getElementById("transaction_hour_value") },
    { input: document.getElementById("merchant_risk_score"), output: document.getElementById("merchant_risk_score_value") },
  ];

  sliders.forEach(({ input, output }) => {
    if (!input || !output) return;
    output.textContent = input.value;
    input.addEventListener("input", () => {
      output.textContent = input.value;
    });
  });

  const validateField = (fieldId, message) => {
    const input = document.getElementById(fieldId);
    const errorBox = document.getElementById(`${fieldId}-error`);
    if (!input || !errorBox) return true;

    const value = input.value.trim();
    if (!value) {
      errorBox.textContent = `${message} is required.`;
      errorBox.classList.remove("hidden");
      return false;
    }

    const numeric = Number(value);
    if (Number.isNaN(numeric)) {
      errorBox.textContent = `${message} must be a valid number.`;
      errorBox.classList.remove("hidden");
      return false;
    }

    if (fieldId === "age" && (numeric < 18 || numeric > 100)) {
      errorBox.textContent = "Age must be between 18 and 100.";
      errorBox.classList.remove("hidden");
      return false;
    }

    if ((fieldId === "transaction_amount" || fieldId === "account_balance" || fieldId === "merchant_distance_km") && numeric < 0) {
      errorBox.textContent = `${message} cannot be negative.`;
      errorBox.classList.remove("hidden");
      return false;
    }

    if (fieldId === "num_transactions_today" && numeric < 0) {
      errorBox.textContent = `${message} cannot be negative.`;
      errorBox.classList.remove("hidden");
      return false;
    }

    if (fieldId === "transaction_hour" && (numeric < 0 || numeric > 23)) {
      errorBox.textContent = "Transaction hour must be between 0 and 23.";
      errorBox.classList.remove("hidden");
      return false;
    }

    if (fieldId === "merchant_risk_score" && (numeric < 1 || numeric > 15)) {
      errorBox.textContent = "Merchant risk score must be between 1 and 15.";
      errorBox.classList.remove("hidden");
      return false;
    }

    errorBox.classList.add("hidden");
    return true;
  };

  const validators = [
    ["age", "Age"],
    ["transaction_amount", "Transaction amount"],
    ["account_balance", "Account balance"],
    ["num_transactions_today", "Transactions today"],
    ["transaction_hour", "Transaction hour"],
    ["merchant_distance_km", "Merchant distance"],
    ["merchant_risk_score", "Merchant risk score"],
  ];

  form.addEventListener("submit", (event) => {
    let valid = true;
    validators.forEach(([fieldId, message]) => {
      if (!validateField(fieldId, message)) {
        valid = false;
      }
    });

    if (!valid) {
      event.preventDefault();
      return;
    }

    submitButton.disabled = true;
    submitText.textContent = "Analyzing Transaction";
    submitSpinner.classList.remove("hidden");
  });

  const progressFill = document.getElementById("prediction-progress");
  if (progressFill) {
    const probability = Number(progressFill.dataset.probability || 0);
    progressFill.style.width = `${probability}%`;
  }
});
