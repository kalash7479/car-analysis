import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(page_title="Car MSRP Visualizer", layout="wide")
st.title("Car MSRP Visualizer")

# Upload CSV file
uploaded_file = st.file_uploader("CARS.csv", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Show column names for debugging
        st.write("Columns in uploaded file:", df.columns.tolist())

        # Check required columns
        required_columns = ['Make', 'Model', 'Type', 'MSRP']
        if not all(col in df.columns for col in required_columns):
            st.error(f"The CSV file must contain the following columns: {required_columns}")
        else:
            # Clean MSRP column
            df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')

            # Brand selection
            brands = df['Make'].dropna().unique()
            selected_brand = st.selectbox("Select Car Brand", sorted(brands))
            filtered_brand = df[df['Make'] == selected_brand]

            # Type selection
            types = filtered_brand['Type'].dropna().unique()
            if len(types) > 0:
                selected_type = st.selectbox("Select Car Type", sorted(types))
                filtered_data = filtered_brand[filtered_brand['Type'] == selected_type]

                # Display filtered data
                st.dataframe(filtered_data[['Make', 'Model', 'Type', 'MSRP']])

                # Plot MSRP by Model
                st.subheader("MSRP by Model")
                plt.figure(figsize=(12, 6))
                sb.barplot(x='Model', y='MSRP', data=filtered_data)
                plt.xticks(rotation=90)
                st.pyplot(plt.gcf())
            else:
                st.warning("No types available for the selected brand.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload your `CARS.csv` file to begin.")
