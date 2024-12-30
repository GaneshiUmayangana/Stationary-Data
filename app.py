import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Streamlit page
st.set_page_config(page_title="Stationary Data Analysis", layout="wide")

# Add page title
st.title("Stationary Data Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Load the dataset
    df = pd.read_excel(uploaded_file)

    # Display the dataset
    st.subheader("Dataset")
    st.dataframe(df)

    # Ensure columns are clean
    df.columns = df.columns.str.strip()

    # Display column names
    st.write("Column Names:", df.columns.tolist())

    # Custom order for months
    month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']

    # Add Region selection
    if "Region" in df.columns:
        st.sidebar.subheader("Filter by Region")
        regions = df["Region"].unique().tolist()
        selected_region = st.sidebar.selectbox("Select Region", options=["All"] + regions)

        # Filter data by selected region
        if selected_region != "All":
            df = df[df["Region"] == selected_region]

    # Add Point of Sale selection
    if "POINT OF SALE" in df.columns:
        st.sidebar.subheader("Filter by Point of Sale")
        pos_options = df["POINT OF SALE"].unique().tolist()
        selected_pos = st.sidebar.selectbox("Select Point of Sale", options=["All"] + pos_options)

        # Filter data by selected Point of Sale
        if selected_pos != "All":
            df = df[df["POINT OF SALE"] == selected_pos]

    # Plot 1: ACT-LC and TGT-LC by Month
    if "ACT -LC" in df.columns and "TGT-LC" in df.columns and "Month" in df.columns:
        st.subheader(f"ACT-LC and TGT-LC by Month (Custom Order) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Ensure "Month" column is categorical with the custom order
        df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

        # Sort data by the custom month order
        df = df.sort_values("Month")

        # Aggregate by Month (if needed)
        monthly_data = df.groupby("Month")[["ACT -LC", "TGT-LC"]].sum().reset_index()

        # Plot ACT-LC and TGT-LC curves
        fig1, ax1 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.lineplot(data=monthly_data, x="Month", y="ACT -LC", marker="o", label="ACT-LC", ax=ax1)
        sns.lineplot(data=monthly_data, x="Month", y="TGT-LC", marker="o", label="TGT-LC", ax=ax1)

        ax1.set_title("ACT-LC and TGT-LC by Month (Custom Order)", fontsize=12)
        ax1.set_xlabel("Month", fontsize=10)
        ax1.set_ylabel("Values (LC)", fontsize=10)
        ax1.legend()
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig1)

    else:
        st.error("Required columns 'ACT -LC', 'TGT-LC', and/or 'Month' are not found in the dataset. Please check the file.")

    # Plot 2: VAR %-LC (ACT vsTGT) by Month
    if "VAR %-LC (ACT vsTGT)" in df.columns and "Month" in df.columns:
        st.subheader(f"Month-wise VAR %-LC (ACT vsTGT) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Aggregate "VAR %-LC (ACT vsTGT)" by month (average or sum as required)
        monthly_var_data = df.groupby("Month")["VAR %-LC (ACT vsTGT)"].mean().reset_index()

        # Plot VAR %-LC (ACT vsTGT) by month
        fig2, ax2 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.lineplot(
            data=monthly_var_data,
            x="Month",
            y="VAR %-LC (ACT vsTGT)",
            marker="o",
            label="VAR %-LC (ACT vsTGT)",
            ax=ax2,
        )

        ax2.set_title("Month-wise VAR %-LC (ACT vsTGT)", fontsize=12)
        ax2.set_xlabel("Month", fontsize=10)
        ax2.set_ylabel("VAR %-LC (ACT vsTGT)", fontsize=10)
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig2)

    else:
        st.error("Required columns 'VAR %-LC (ACT vsTGT)' and/or 'Month' are not found in the dataset. Please check the file.")

    # Plot 3: VAR %-USD (ACT vsTGT) by Month
    if "VAR %-USD (ACT vsTGT)" in df.columns and "Month" in df.columns:
        st.subheader(f"Month-wise VAR %-USD (ACT vsTGT) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Aggregate "VAR %-USD (ACT vsTGT)" by month (average or sum as required)
        monthly_var_usd_data = df.groupby("Month")["VAR %-USD (ACT vsTGT)"].mean().reset_index()

        # Plot VAR %-USD (ACT vsTGT) by month
        fig3, ax3 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.lineplot(
            data=monthly_var_usd_data,
            x="Month",
            y="VAR %-USD (ACT vsTGT)",
            marker="o",
            label="VAR %-USD (ACT vsTGT)",
            ax=ax3,
        )

        ax3.set_title("Month-wise VAR %-USD (ACT vsTGT)", fontsize=12)
        ax3.set_xlabel("Month", fontsize=10)
        ax3.set_ylabel("VAR %-USD (ACT vsTGT)", fontsize=10)
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig3)

    else:
        st.error("Required columns 'VAR %-USD (ACT vsTGT)' and/or 'Month' are not found in the dataset. Please check the file.")

    # Plot 4: ACT-USD and TGT-USD by Month
    if "ACT -USD" in df.columns and "TGT-USD" in df.columns and "Month" in df.columns:
        st.subheader(f"ACT-USD and TGT-USD by Month (Custom Order) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Aggregate ACT-USD and TGT-USD by month (sum or average as required)
        monthly_usd_data = df.groupby("Month")[["ACT -USD", "TGT-USD"]].sum().reset_index()

        # Plot ACT-USD and TGT-USD curves
        fig4, ax4 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.lineplot(data=monthly_usd_data, x="Month", y="ACT -USD", marker="o", label="ACT-USD", ax=ax4)
        sns.lineplot(data=monthly_usd_data, x="Month", y="TGT-USD", marker="o", label="TGT-USD", ax=ax4)

        ax4.set_title("ACT-USD and TGT-USD by Month (Custom Order)", fontsize=12)
        ax4.set_xlabel("Month", fontsize=10)
        ax4.set_ylabel("Values (USD)", fontsize=10)
        ax4.legend()
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig4)

    else:
        st.error("Required columns 'ACT -USD', 'TGT-USD', and/or 'Month' are not found in the dataset. Please check the file.")

    # Plot 5: Region-wise ACT-USD Distribution
    if "ACT -USD" in df.columns and "Region" in df.columns:
        st.subheader(f"Region-wise Distribution of ACT-USD - Region: {selected_region if 'selected_region' in locals() else 'All'}")

        # Aggregate ACT-USD by Region
        region_usd_data = df.groupby("Region")["ACT -USD"].sum().reset_index()

        # Plot Region-wise ACT-USD distribution
        fig5, ax5 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.barplot(data=region_usd_data, x="Region", y="ACT -USD", ax=ax5)

        ax5.set_title("Region-wise Distribution of ACT-USD", fontsize=12)
        ax5.set_xlabel("Region", fontsize=10)
        ax5.set_ylabel("Total ACT-USD", fontsize=10)
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig5)

    else:
        st.error("Required columns 'ACT -USD' and/or 'Region' are not found in the dataset. Please check the file.")

    # Plot 6: Month-wise Act. Using-Bgt. ex. Rates vs Act. Using- LY. Ex. Rates (Bar Plot)
    if "Act. Using-Bgt. ex. Rates" in df.columns and "Act. Using- LY. Ex. Rates" in df.columns and "Month" in df.columns:
        st.subheader(f"Month-wise Act. Using-Bgt. ex. Rates vs Act. Using- LY. Ex. Rates (Bar Plot) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Aggregate "Act. Using-Bgt. ex. Rates" and "Act. Using- LY. Ex. Rates" by month
        monthly_rates_data = df.groupby("Month")[["Act. Using-Bgt. ex. Rates", "Act. Using- LY. Ex. Rates"]].sum().reset_index()

        # Plot Act. Using-Bgt. ex. Rates vs Act. Using- LY. Ex. Rates by month as a bar plot
        fig6, ax6 = plt.subplots(figsize=(8, 4))  # Reduced size
        monthly_rates_data.set_index('Month')[['Act. Using-Bgt. ex. Rates', 'Act. Using- LY. Ex. Rates']].plot(kind='bar', ax=ax6)

        ax6.set_title("Month-wise Act. Using-Bgt. ex. Rates vs Act. Using- LY. Ex. Rates (Bar Plot)", fontsize=12)
        ax6.set_xlabel("Month", fontsize=10)
        ax6.set_ylabel("Rates", fontsize=10)
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig6)

    else:
        st.error("Required columns 'Act. Using-Bgt. ex. Rates', 'Act. Using- LY. Ex. Rates', and/or 'Month' are not found in the dataset. Please check the file.")

    # Plot 7: Exchange - gain/( loss) by Month
    if "Exchange - gain/( loss)" in df.columns and "Month" in df.columns:
        st.subheader(f"Month-wise Exchange - gain/( loss) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")

        # Aggregate "Exchange - gain/( loss)" by month (sum or average as required)
        monthly_exchange_data = df.groupby("Month")["Exchange - gain/( loss)"].mean().reset_index()

        # Plot Exchange - gain/( loss) by month
        fig7, ax7 = plt.subplots(figsize=(8, 4))  # Reduced size
        sns.lineplot(
            data=monthly_exchange_data,
            x="Month",
            y="Exchange - gain/( loss)",
            marker="o",
            label="Exchange - gain/( loss)",
            ax=ax7,
        )

        ax7.set_title("Month-wise Exchange - gain/( loss)", fontsize=12)
        ax7.set_xlabel("Month", fontsize=10)
        ax7.set_ylabel("Exchange Gain/( Loss)", fontsize=10)
        plt.xticks(rotation=45, fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot(fig7)

    else:
        st.error("Required column 'Exchange - gain/( loss)' and/or 'Month' are not found in the dataset. Please check the file.")
