import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Streamlit config
st.set_page_config(page_title="Car MSRP Visualizer", layout="wide")
st.title("🚗 Car MSRP Visualizer")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your CARS.csv file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Check required columns
        required_columns = ['Make', 'Model', 'Type', 'MSRP']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ CSV must contain these columns: {required_columns}")
        else:
            # Clean MSRP column
            df['MSRP'] = df['MSRP'].replace('[$,]', '', regex=True).astype('int64')

            # Brand selection with searchable dropdown
            brands = sorted(df['Make'].dropna().unique())
            selected_brand = st.selectbox("🔍 Select Car Brand", brands, index=0)

            filtered_brand = df[df['Make'] == selected_brand]

            # Type selection
            types = sorted(filtered_brand['Type'].dropna().unique())
            if len(types) > 0:
                selected_type = st.selectbox("🚘 Select Car Type", types, index=0)
                filtered_type = filtered_brand[filtered_brand['Type'] == selected_type]

                if not filtered_type.empty:
                    # MSRP filter slider
                    min_price = int(filtered_type['MSRP'].min())
                    max_price = int(filtered_type['MSRP'].max())
                    price_range = st.slider("💰 Filter by MSRP Range", min_price, max_price, (min_price, max_price), step=1000)

                    filtered_data = filtered_type[
                        (filtered_type['MSRP'] >= price_range[0]) &
                        (filtered_type['MSRP'] <= price_range[1])
                    ]

                    # Toggle to show raw data
                    if st.checkbox("📊 Show Filtered Data Table"):
                        st.dataframe(filtered_data[['Make', 'Model', 'Type', 'MSRP']])

                    # Plot
                    if not filtered_data.empty:
                        st.subheader("📈 MSRP by Model")
                        fig, ax = plt.subplots(figsize=(12, 6))
                        sb.barplot(x='Model', y='MSRP', data=filtered_data, ax=ax, palette='coolwarm')
                        plt.xticks(rotation=90)
                        st.pyplot(fig)
                    else:
                        st.warning("⚠️ No cars found in the selected price range.")
                else:
                    st.warning("⚠️ No cars found for the selected type.")
            else:
                st.warning("⚠️ No types available for the selected brand.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
else:
    st.info("👆 Please upload your `CARS.csv` file to begin.")
