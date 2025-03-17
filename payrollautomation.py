import streamlit as st
import pandas as pd
import numpy as np

# App Title
st.title("💰 Payroll Processing & Tax Compliance Automation")

# Upload Employee Payroll Data
uploaded_file = st.file_uploader("📂 Upload Employee Payroll Data (CSV)", type=["csv"])

if uploaded_file:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Display Dataset Preview
    st.subheader("📋 Employee Payroll Data")
    st.dataframe(df.head())

    # Ensure required columns exist
    required_columns = {"Employee_ID", "Name", "Basic_Salary", "Deductions", "Allowances"}
    if not required_columns.issubset(df.columns):
        st.error(f"Dataset must contain these columns: {required_columns}")
    else:
        # Tax & Compliance Rules (Example: Flat 10% Tax)
        TAX_RATE = 0.10  # 10% Tax Deduction
        RETIREMENT_RATE = 0.05  # 5% Retirement Fund Contribution

        # Calculate Payroll Details
        df["Tax"] = df["Basic_Salary"] * TAX_RATE
        df["Retirement_Contribution"] = df["Basic_Salary"] * RETIREMENT_RATE
        df["Net_Salary"] = df["Basic_Salary"] + df["Allowances"] - (df["Tax"] + df["Deductions"] + df["Retirement_Contribution"])

        # Display Processed Payroll
        st.subheader("📊 Processed Payroll Data")
        st.dataframe(df)

        # Download Processed Payroll Data
        st.download_button(
            label="📥 Download Processed Payroll (CSV)",
            data=df.to_csv(index=False),
            file_name="processed_payroll.csv",
            mime="text/csv"
        )

        # Summary Metrics
        st.subheader("📈 Payroll Summary")
        total_salary = df["Basic_Salary"].sum()
        total_tax = df["Tax"].sum()
        total_deductions = df["Deductions"].sum()
        total_allowances = df["Allowances"].sum()
        total_net_salary = df["Net_Salary"].sum()

        st.metric("💵 Total Salary Paid", f"${total_salary:,.2f}")
        st.metric("💰 Total Taxes Deducted", f"${total_tax:,.2f}")
        st.metric("🏦 Total Net Salary Paid", f"${total_net_salary:,.2f}")

        # Compliance Check: Employees with High Deductions
        st.subheader("⚠️ Compliance Check: High Deductions")
        high_deductions = df[df["Deductions"] > (df["Basic_Salary"] * 0.3)]
        if not high_deductions.empty:
            st.warning("Employees with deductions greater than 30% of salary:")
            st.dataframe(high_deductions)
        else:
            st.success("✅ No compliance issues detected!")

        # Individual Payroll Calculation
        st.subheader("🔢 Calculate Payroll for an Employee")
        basic_salary = st.number_input("Enter Basic Salary ($)", min_value=0, value=5000)
        deductions = st.number_input("Enter Deductions ($)", min_value=0, value=500)
        allowances = st.number_input("Enter Allowances ($)", min_value=0, value=1000)

        if st.button("Calculate Payroll"):
            tax = basic_salary * TAX_RATE
            retirement = basic_salary * RETIREMENT_RATE
            net_salary = basic_salary + allowances - (tax + deductions + retirement)

            st.write(f"💰 **Net Salary:** ${net_salary:,.2f}")
            st.write(f"💵 **Tax Deduction (10%):** ${tax:,.2f}")
            st.write(f"🏦 **Retirement Fund (5%):** ${retirement:,.2f}")

else:
    st.info("Please upload a payroll CSV file to process.")

