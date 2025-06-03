import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="Car MSRP Visualizer", layout="wide")

st.title("Car MSRP Visualizer")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CARS.csv", type=["csv"])

if uploaded_file is not None:
    # Read and clean the data
    df = pd.read_csv(uploaded_file)
    df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')

    # Brand selection
    brands = df['Make'].unique()
    selected_brand = st.selectbox("Select Car Brand", sorted(brands))

    filtered_by_brand = df[df['Make'] == selected_brand]

    # Type selection
    types = filtered_by_brand['Type'].unique()
    selected_type = st.selectbox("Select Car Type", sorted(types))

    filtered_by_type = filtered_by_brand[filtered_by_brand['Type'] == selected_type]

    # Category selection
    categories = filtered_by_type['Category'].unique()
    selected_category = st.selectbox("Select Car Category", sorted(categories))

    filtered_data = filtered_by_type[filtered_by_type['Category'] == selected_category]

    # Show the filtered data (optional)
    st.dataframe(filtered_data[['Make', 'Model', 'Type', 'Category', 'MSRP']])

    # Plot
    st.subheader("MSRP by Model")
    plt.figure(figsize=(12, 6))
    sb.barplot(x='Model', y='MSRP', data=filtered_data)
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())

else:
    st.info("Please upload the `CARS.csv` file to begin.")
