import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration

st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# 2. Sidebar: Dataset Ingestion

st.sidebar.header("Dataset Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    # Read dataset
    df = pd.read_csv(uploaded_file)

    # 3. Dataset Overview

    st.subheader("Dataset Overview")
    st.write("**First 5 Rows:**")
    st.dataframe(df.head())

    st.write("**Shape:**", df.shape)
    st.write("**Column Data Types:**")
    st.dataframe(df.dtypes.astype(str))

    # Missing value summary
    st.write("**Missing Values per Column:**")
    missing = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing %": (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(missing)

    # Basic statistics for numerical columns
    st.write("**Basic Numerical Statistics:**")
    st.dataframe(df.describe())


    # 4. Attribute Selection

    st.sidebar.header("Attribute Selection")
    column = st.sidebar.selectbox("Select Attribute for Visualization", df.columns)

    # Detect column type
    column_type = "Numerical" if pd.api.types.is_numeric_dtype(df[column]) else "Categorical"


    # 5. Visualization Rendering

    st.subheader("Visualization")

    if column_type == "Numerical":
        # Histogram with seaborn
        fig, ax = plt.subplots()
        sns.histplot(df[column].dropna(), kde=True, ax=ax)
        ax.set_title(f"Histogram of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        # Bar chart for categorical
        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind="bar", ax=ax)
        ax.set_title(f"Bar Chart of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
        st.pyplot(fig)

else:
    st.info("Please upload a CSV file to start EDA.")