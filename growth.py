# 🛠️ Import necessary libraries
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 🎨 Set up page configuration
st.set_page_config(page_title=" Data Sweeper",page_icon="📊", layout='wide')

# 🏷️ Title & Description
st.title("📊 Data Sweeper")
st.write("✨ Transform your files between **CSV** and **Excel** formats with built-in **data cleaning** and **visualization**! 🚀")

# 📂 File Uploader: Allows users to upload multiple CSV or Excel files
uploaded_files = st.file_uploader("📂 Upload your file (CSV or Excel) ⬆️", type=["csv", "xlsx"], accept_multiple_files=True)

# 📌 Process each uploaded file
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()  # Extract file extension

        # 🔄 Read file based on extension type
        if file_ext == ".csv":
            df = pd.read_csv(file)  # Read CSV file
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)  # Read Excel file
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")  # Show error for unsupported formats
            continue  # Skip the file

        # 📌 Display file details
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # 👀 Show Data Preview
        st.subheader("👀 Data Preview")
        st.dataframe(df.head())  # Display first few rows of the DataFrame

        # 🧹 Data Cleaning Options
        st.subheader("🧼 Data Cleaning Options")
        if st.checkbox(f"🛠️ Clean Data for {file.name}"):
            col1, col2 = st.columns(2)  # Divide cleaning options into two columns

            # 🗑️ Remove Duplicates
            with col1:
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            # 🔄 Fill Missing Values
            with col2:
                if st.button(f"🔄 Fill Missing Values for {file.name}"):
                    numeric_col = df.select_dtypes(include=['number']).columns  # Select numeric columns
                    df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())  # Fill NaN with mean
                    st.write("✅ Missing values have been filled!")

        # 🎛️ Select Columns to Keep or Convert
        st.subheader("🎛️ Select Columns to Convert")
        columns = st.multiselect(f"📌 Choose Columns for {file.name}", df.columns, default=list(df.columns))
        df = df[columns]  # Keep only selected columns

        # 📊 Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Show bar chart for numeric data

        # 🔄 File Conversion Options
        st.subheader("🔄 File Conversion Options")
        conversion_type = st.radio(f"🔀 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # 💾 Convert File
        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()  # Create an in-memory buffer

            # Convert file based on selected format
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Convert DataFrame to CSV
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)  # Convert DataFrame to Excel
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Move to the beginning of the buffer

            # ⬇️ Download button for the converted file
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            st.success("🎉 All files processed successfully! ✅")
st.markdown("<small>This app is created by ❤,SHAYAN ALI</small>", unsafe_allow_html=True)

