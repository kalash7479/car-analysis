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
    try:
        # Read and clean the data
        df = pd.read_csv(uploaded_file)
        
        # Check if 'MSRP' column exists
        if 'MSRP' not in df.columns or 'Make' not in df.columns:
            st.error("Uploaded CSV must contain at least 'Make' and 'MSRP' columns.")
        else:
            # Clean MSRP column
            df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')

            # Brand selection
            brands = df['Make'].dropna().unique()
            selected_brand = st.selectbox("Select Car Brand", sorted(brands))

            filtered_by_brand = df[df['Make'] == selected_brand]

            if not filtered_by_brand.empty:
                types = filtered_by_brand['Type'].dropna().unique()
                if len(types) > 0:
                    selected_type = st.selectbox("Select Car Type", sorted(types))
                    filtered_by_type = filtered_by_brand[filtered_by_brand['Type'] == selected_type]

                    if not filtered_by_type.empty:
                        categories = filtered_by_type['Category'].dropna().unique()
                        if len(categories) > 0:
                            selected_category = st.selectbox("Select Car Category", sorted(categories))
                            filtered_data = filtered_by_type[filtered_by_type['Category'] == selected_category]

                            # Show data
                            st.dataframe(filtered_data[['Make', 'Model', 'Type', 'Category', 'MSRP']])

                            # Plot
                            st.subheader("MSRP by Model")
                            plt.figure(figsize=(12, 6))
                            sb.barplot(x='Model', y='MSRP', data=filtered_data)
                            plt.xticks(rotation=90)
                            st.pyplot(plt.gcf())
                        else:
                            st.warning("No categories found for this selection.")
                    else:
                        st.warning("No data found for selected type.")
                else:
                    st.warning("No types available for this brand.")
            else:
                st.warning("No data available for the selected brand.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload the `CARS.csv` file to begin.")
