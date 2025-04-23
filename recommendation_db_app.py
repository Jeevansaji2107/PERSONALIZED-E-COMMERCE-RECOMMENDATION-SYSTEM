import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split

import streamlit as st

st.set_page_config(page_title="Product Recommendation Login", page_icon="🔐", layout="centered")
# Set valid login credentials (replace with your own)
VALID_USERNAME = "admin"
VALID_PASSWORD = "123456"


# Custom CSS for centering and styling
st.markdown("""
    <style>
        .login-container {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .login-box {
            background-color: rgba(30, 30, 30, 0.85);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }

        .login-title {
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 0.5em;
            color: white;
        }

        .small-note {
            font-size: 0.9em;
            color: gray;
        }
    </style>

    <video autoplay muted loop class="video-background">
        <source src="login_page.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div class="overlay"></div>
    <div class="login-container">
""", unsafe_allow_html=True)

# Login check
def check_login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:

        st.image("https://imgs.search.brave.com/Z3_NYn_-5RTfPpwCDGJROUzyLnUZgjxgjFQ8rWPc3co/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzEyLzY3LzQxLzY0/LzM2MF9GXzEyNjc0/MTY0NTVfbzNPTUI5/MUFGWXgzbFJvdjM5/cDlOY25xMUR1cFNa/ZWcuanBn", width=60)
        st.markdown('<div class="login-title">🔐 Login to Continue</div>', unsafe_allow_html=True)
        st.write("Welcome to the **Product Recommendation System**. Please log in to proceed.")

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        if st.button("🚀 Login"):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.warning("⚠️ Invalid credentials. Please try again.")

        #st.markdown('<br><hr><span class="small-note">Don\'t have an account? <a href="#">Contact Admin</a></span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)  # Close login-container div

        return False

    return True



# --- MySQL Connection ---
def fetch_ratings_from_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # Change if needed
        database="ecommerce_recommendation"
    )
    query = "SELECT user_id, prod_id, rating FROM user_rating"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# --- Train Model with Caching ---
@st.cache_resource
def train_model(_trainset):
    model = SVD()
    model.fit(_trainset)
    return model

# --- App Logic ---
if check_login():
    st.markdown("## 🛒 Product Recommendation System")
    st.markdown("### 💡 Collaborative Filtering | Real-time MySQL Data")

    with st.spinner("Fetching data and training model..."):
        ratings_df = fetch_ratings_from_mysql()

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings_df[['user_id', 'prod_id', 'rating']], reader)
        trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
        svd = train_model(trainset)

    st.success("Model trained and ready!")

    users = ratings_df['user_id'].unique().tolist()
    products = ratings_df['prod_id'].unique().tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        user_id = st.selectbox("👤 Select User ID", users)
    with col2:
        top_n = st.slider("🎯 Number of Recommendations", 1, 20, 5)
    with col3:
        threshold = st.slider("⭐ Minimum Rating Threshold", 0.0, 5.0, 3.5, 0.1)

    decimal_precision = st.selectbox("🔢 Decimal Precision", [2, 4], index=0)

    def get_unrated_predictions(predictions, user_id, ratings_df):
        rated_items = ratings_df[ratings_df['user_id'] == user_id]['prod_id'].tolist()
        return [pred for pred in predictions if pred.iid not in rated_items]

    predictions = [svd.predict(user_id, iid) for iid in products]
    unrated_preds = get_unrated_predictions(predictions, user_id, ratings_df)
    filtered_preds = [p for p in unrated_preds if p.est >= threshold]
    top_preds = sorted(filtered_preds, key=lambda x: x.est, reverse=True)[:top_n]

    st.markdown(f"### 🔍 Top {top_n} Recommendations for `{user_id}`")
    if top_preds:
        rec_df = pd.DataFrame({
            'Product ID': [pred.iid for pred in top_preds],
            'Predicted Rating': [round(pred.est, decimal_precision) for pred in top_preds]
        })
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.warning("No recommendations found above the selected threshold.")

    with st.expander("📊 Show Heatmap"):
        st.subheader("Zoomed-in Heatmap of Predicted Ratings")
        heat_users = users[:20]
        heat_items = products[:20]
        heat_matrix = np.zeros((len(heat_users), len(heat_items)))
        for i, uid in enumerate(heat_users):
            for j, iid in enumerate(heat_items):
                heat_matrix[i, j] = svd.predict(uid, iid).est

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heat_matrix, xticklabels=heat_items, yticklabels=heat_users, cmap="YlGnBu", annot=False, ax=ax)
        st.pyplot(fig)

    with st.expander("📈 Rating Distribution"):
        st.subheader("Distribution of Predicted Ratings")
        all_predicted_ratings = [round(p.est, decimal_precision) for p in unrated_preds]
        fig = px.histogram(all_predicted_ratings, nbins=20, title="Predicted Rating Distribution")
        st.plotly_chart(fig, use_container_width=True)