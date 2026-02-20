import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="RegTech Validation Platform", layout="wide")

st.title("Smart Regulatory Validation Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # Column Selection
    st.subheader("Select Columns")

    columns = df.columns.tolist()

    date_col = st.selectbox("Select Date Column", columns)
    amount_col = st.selectbox("Select Amount Column", columns)
    type_col = st.selectbox("Select Transaction Type Column", columns)

    # Convert date
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Date filter
    st.subheader("Select Date Range")
    min_date = df[date_col].min()
    max_date = df[date_col].max()

    start_date, end_date = st.date_input(
        "Choose reporting period",
        [min_date, max_date]
    )

    filtered_df = df[
        (df[date_col] >= pd.to_datetime(start_date)) &
        (df[date_col] <= pd.to_datetime(end_date))
    ]

    # Custom Validation Rules
    st.subheader("Custom Validation Rules")

    min_amount = st.number_input("Minimum Allowed Amount", value=0)
    max_amount = st.number_input("Maximum Allowed Amount", value=10000000)

    allowed_types = st.multiselect(
        "Allowed Transaction Types",
        filtered_df[type_col].unique()
    )

    if st.button("Run Validation"):

        violations = []

        # Rule 1: Amount range
        amount_violation = filtered_df[
            (filtered_df[amount_col] < min_amount) |
            (filtered_df[amount_col] > max_amount)
        ]

        # Rule 2: Type validation
        type_violation = filtered_df[
            ~filtered_df[type_col].isin(allowed_types)
        ]

        if not amount_violation.empty:
            violations.append(amount_violation)

        if not type_violation.empty:
            violations.append(type_violation)

        if violations:
            final_violations = pd.concat(violations)
            st.error(f"{len(final_violations)} Violations Found")
            st.dataframe(final_violations)
        else:
            st.success("Validation PASSED ✅")

        # Monthly Report
        st.subheader("Monthly Summary Report")

        filtered_df["month"] = filtered_df[date_col].dt.to_period("M")

        summary = filtered_df.groupby(
            ["month", type_col]
        )[amount_col].agg(["sum", "count"]).reset_index()

        st.dataframe(summary)

        # Chart
        st.subheader("Transaction Trend")

        monthly_total = filtered_df.groupby("month")[amount_col].sum()

        fig, ax = plt.subplots()
        monthly_total.plot(kind="bar", ax=ax)
        st.pyplot(fig)