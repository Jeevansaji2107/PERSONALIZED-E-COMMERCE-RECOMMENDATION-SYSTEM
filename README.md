# 🛍️ Personalized E-Commerce Recommendation System

A **full-stack recommendation system** that combines traditional collaborative filtering (SVD) with deep learning (Neural Collaborative Filtering – NCF) to deliver **personalized product suggestions** in real-time using a **MySQL backend** and an interactive **Streamlit frontend**.

---

## 🚀 Project Overview

This project solves the problem of **information overload** in online shopping by intelligently recommending products based on user behavior and past interactions. It blends **machine learning**, **deep learning**, **database engineering**, and **UI development** into a seamless, real-world solution.

---

## 🧠 Features

- 🔍 **Collaborative Filtering (SVD)** using Surprise library
- 🤖 **Neural Collaborative Filtering (NCF)** using TensorFlow/Keras
- 🗃️ **Real-time MySQL data integration**
- 📊 **Evaluation** using RMSE, MAE, and Precision@K
- 💡 **IMDb-style popularity-based ranking**
- 🌐 **Streamlit Web App** with:
  - Login Authentication
  - Top-N Recommendation Slider
  - Rating Threshold Filter
  - Decimal Precision Selector
  - Heatmap and Histogram Visualization

---

## 🧰 Tech Stack

| Layer           | Tools Used                                  |
|----------------|----------------------------------------------|
| 📦 Backend      | Python, Pandas, NumPy, Surprise, Keras       |
| 🧠 ML Models    | SVD (Matrix Factorization), NCF (Deep Learning) |
| 🗃️ Database     | MySQL, dotenv for secure credentials         |
| 🎨 Frontend     | Streamlit (Login, UI, Heatmaps, Charts)      |
| 📈 Visualization| Seaborn, Matplotlib, Plotly, Power BI (optional) |
| 📁 Deployment   | Localhost (future-ready for Heroku/AWS)     |

---

## 📸 Screenshots

| Login Page | Recommendation Dashboard | Evaluation |
|------------|---------------------------|------------|
| ![Login](https://github.com/Jeevansaji2107/PERSONALIZED-E-COMMERCE-RECOMMENDATION-SYSTEM/blob/main/PROJECT%20(2)/Login%20Page.png) | ![UI](https://github.com/Jeevansaji2107/PERSONALIZED-E-COMMERCE-RECOMMENDATION-SYSTEM/blob/main/PROJECT%20(2)/DASHBOARD.png) | ![RATING DISTRIBUTION](https://github.com/Jeevansaji2107/PERSONALIZED-E-COMMERCE-RECOMMENDATION-SYSTEM/blob/main/Screenshot%202025-05-22%20142311.png) |

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/Jeevansaji2107/PERSONALIZED-E-COMMERCE-RECOMMENDATION-SYSTEM.git
cd PERSONALIZED-E-COMMERCE-RECOMMENDATION-SYSTEM
cd ecommerce-recommendation-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up .env file for MySQL
cp .env.example .env
# Add DB_HOST, DB_USER, DB_PASS, DB_NAME

# Run the Streamlit app
streamlit run app.py
