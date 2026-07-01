# 💳 Credit Card Fraud Detection

A machine learning-powered web application that predicts whether a financial transaction is **fraudulent** or **legitimate** based on transaction details. The project follows a complete end-to-end machine learning workflow, from data preprocessing and model selection to deployment with a Flask web interface.

## 🌐 Live Demo

🔗 **Application:** https://creditcard-fraud-prediction.onrender.com/

---

## ✨ Features

* 🔍 Predicts fraudulent transactions in real time
* 📊 Displays fraud probability
* 🚦 Risk level indicator (Low / Medium / High / Critical)
* 💡 Actionable recommendations based on prediction
* 🎨 Modern responsive UI built with Tailwind CSS
* ⚡ Fast predictions using a trained Logistic Regression model

---

## 📸 Preview



| Dashboard          | Prediction         |
| ------------------ | ------------------ |
|<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/1a8a1ced-f798-4f18-8fc2-fb1316206520" />| <img width="350" height="auto" alt="image" src="https://github.com/user-attachments/assets/ef026cd8-e405-416f-92a9-81d2d8ef30e2" />|

---

## 🧠 Machine Learning Workflow

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Feature Selection
* Train-Test Split
* Data Preprocessing
* Pipeline Creation
* Stratified Cross Validation
* Baseline Model Comparison
* Hyperparameter Tuning using RandomizedSearchCV
* Final Model Selection
* Model Evaluation
* Deployment

---

## 📈 Models Compared

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Decision Tree
* Random Forest
* XGBoost

After evaluation and hyperparameter tuning, **Logistic Regression** achieved the best overall performance and was selected as the final model.

---

## 📊 Final Model Performance

| Metric    | Score      |
| --------- | ---------- |
| Accuracy  | **75.22%** |
| Precision | **75.28%** |
| Recall    | **72.45%** |
| F1 Score  | **73.84%** |
| ROC-AUC   | **82.69%** |

---

## 🛠 Tech Stack

### Machine Learning

* Python
* Pandas
* Scikit-learn
* Joblib

### Web Development

* Flask
* HTML5
* Tailwind CSS
* JavaScript

---

## 📂 Project Structure

```text
CreditCard_Fraud_Prediction/
│
├── app.py
├── fraud_detection_model.pkl
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

---

## 🚀 Run Locally

Clone the repository:

```bash
git clone https://github.com/Xphantom07/CreditCard_Fraud_Prediction.git
```

Go to the project folder:

```bash
cd CreditCard_Fraud_Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 📌 Input Features

* Age
* Transaction Amount
* Account Balance
* Number of Transactions Today
* Foreign Transaction
* Transaction Hour
* Previous Fraud History
* Merchant Distance (km)
* Merchant Risk Score

---

## 🎯 Future Improvements

* Batch CSV prediction
* Interactive analytics dashboard
* Model explainability (SHAP)
* User authentication
* Transaction history
* REST API integration
* Docker support

---

## 👨‍💻 Author

**Bhavik Vavadiya**

* GitHub: https://github.com/Xphantom07
* LinkedIn: https://www.linkedin.com/in/bhavik-vavadiya-602660284/
* Email: [bhavikprajapati28195@gmail.com](mailto:bhavikprajapati28195@gmail.com)

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.
