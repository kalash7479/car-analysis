import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ==========================
# Streamlit config
# ==========================
st.set_page_config(page_title="Car MSRP Analyzer", layout="wide")
st.title("🚗 Car MSRP Analyzer & Prediction App")

# ==========================
# File Upload
# ==========================
uploaded_file = st.file_uploader("📂 Upload your CARS.csv file", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    # Clean MSRP column
    df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')
    return df

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)

        required_columns = ['Make', 'Model', 'Type', 'MSRP']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ CSV must contain these columns: {required_columns}")
        else:
            # ==========================
            # Sidebar Filters
            # ==========================
            st.sidebar.header("🔎 Filters")

            brands = sorted(df['Make'].dropna().unique())
            selected_brand = st.sidebar.multiselect("Select Car Brand(s)", brands)

            types = sorted(df['Type'].dropna().unique())
            selected_type = st.sidebar.multiselect("Select Car Type(s)", types)

            search_model = st.sidebar.text_input("Search Model")

            # Apply filters
            filtered_df = df.copy()
            if selected_brand:
                filtered_df = filtered_df[filtered_df['Make'].isin(selected_brand)]
            if selected_type:
                filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
            if search_model:
                filtered_df = filtered_df[filtered_df['Model'].str.contains(search_model, case=False, na=False)]

            # ==========================
            # Tabs
            # ==========================
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Visualizations", "⚖️ Comparison", "🤖 Prediction"])

            # --------------------------
            # TAB 1: Overview
            # --------------------------
            with tab1:
                st.subheader("Filtered Car Data")
                st.dataframe(filtered_df[['Make', 'Model', 'Type', 'MSRP']], use_container_width=True)

                st.markdown("**Summary Stats**")
                st.write(filtered_df.describe())

            # --------------------------
            # TAB 2: Visualizations
            # --------------------------
            with tab2:
                st.subheader("Car Price Visualizations")

                col1, col2 = st.columns(2)
                with col1:
                    fig1 = px.histogram(filtered_df, x="MSRP", nbins=30, title="Price Distribution (MSRP)")
                    st.plotly_chart(fig1, use_container_width=True)

                with col2:
                    if "Horsepower" in filtered_df.columns and "EngineSize" in filtered_df.columns:
                        fig2 = px.scatter(filtered_df, x="Horsepower", y="MSRP",
                                          color="Make", size="EngineSize",
                                          hover_data=["Model"], title="Horsepower vs MSRP")
                        st.plotly_chart(fig2, use_container_width=True)

                st.subheader("Correlation Heatmap")
                numeric_cols = filtered_df.select_dtypes(include='number')
                if not numeric_cols.empty:
                    fig3, ax = plt.subplots(figsize=(8, 5))
                    sb.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", ax=ax)
                    st.pyplot(fig3)

                st.subheader("Top 10 Most Expensive Cars")
                top10 = df.nlargest(10, "MSRP")
                fig4 = px.bar(top10, x="Model", y="MSRP", color="Make", title="Top 10 Expensive Cars")
                st.plotly_chart(fig4, use_container_width=True)

            # --------------------------
            # TAB 3: Comparison
            # --------------------------
            with tab3:
                st.subheader("Compare Two Cars")
                col1, col2 = st.columns(2)
                with col1:
                    car1 = st.selectbox("Select Car 1", df['Model'].unique(), key="car1")
                with col2:
                    car2 = st.selectbox("Select Car 2", df['Model'].unique(), key="car2")

                if car1 and car2:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"### {car1}")
                        st.write(df[df['Model'] == car1].iloc[0])
                    with c2:
                        st.markdown(f"### {car2}")
                        st.write(df[df['Model'] == car2].iloc[0])

            # --------------------------
            # TAB 4: Prediction
            # --------------------------
            with tab4:
                st.subheader("Car MSRP Prediction")

                if "Horsepower" in df.columns and "EngineSize" in df.columns:
                    # Use Horsepower + EngineSize + Weight if available
                    features = ['Horsepower', 'EngineSize']
                    if "Weight" in df.columns:
                        features.append("Weight")

                    X = df[features]
                    y = df["MSRP"]

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LinearRegression()
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)

                    st.write(f"📈 Model R² Score: {r2_score(y_test, y_pred):.2f}")

                    st.markdown("### Enter Car Details for Prediction")
                    input_data = {}
                    for feature in features:
                        input_data[feature] = st.number_input(f"Enter {feature}", value=float(X[feature].mean()))

                    if st.button("Predict Price"):
                        input_df = pd.DataFrame([input_data])
                        predicted_price = model.predict(input_df)[0]
                        st.success(f"💰 Predicted MSRP: ${predicted_price:,.2f}")
                else:
                    st.warning("⚠️ Prediction requires columns like Horsepower, EngineSize, Weight.")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("👆 Please upload your `CARS.csv` file to begin.")
