import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set up Streamlit page
st.set_page_config(page_title="Stationary Data Analysis", layout="wide")

# Add custom CSS for font size adjustments
st.markdown(
    """
    <style>
        .stApp {
            background-image: url('https://www.islandnews.lk/wp-content/uploads/2024/11/Several-Sri-Lankan-Airlines-flights-cancelled.jpg');
            background-size: cover;
            background-position: center;
        }
        .stTitle, .stSubheader, .stHeader, .stDataFrame, .stText {
            font-size: 20px;
        }
        .stMarkdown {
            font-size: 20px;
        }
        .stButton, .stSelectbox, .stTextInput, .stRadio, .stSlider, .stFileUploader, .stMultiselect {
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add page title
st.title("Stationary Data Analysis")

# Add SriLankan Airlines Aircraft Image
st.markdown(
    """
    <h3>SriLankan Airlines</h3>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/SriLankan_Airlines_Airbus_A330-200_%28reg._4R-ALP%29.jpg/1024px-SriLankan_Airlines_Airbus_A330-200_%28reg._4R-ALP%29.jpg" alt="SriLankan Airlines Aircraft" width="500"/>
    """,
    unsafe_allow_html=True,
)

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Load the dataset
    df = pd.read_excel(uploaded_file)
    month_order = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November']

    # Ensure columns are clean
    df.columns = df.columns.str.strip()

    # Display the dataset
    st.subheader("Dataset")
    st.dataframe(df)

    # Create two columns for the side-by-side plots
    col1, col2 = st.columns(2)

    # First plot: Region-wise Distribution of ACT-USD
    with col2:
        fig1 = px.pie(
            df,
            names="Month",
            values="ACT -USD",
            title="Month-wise Distribution of ACT-USD",
            labels={"Month": "Month", "ACT -USD": "Total ACT-USD"},
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Second plot: Region-wise Distribution of TGT-USD
    with col1:
        fig2 = px.bar(
            df,
            x="Region",
            y=["TGT-USD", "ACT -USD"],  # Include both TGT-USD and ACT -USD
            title="Region-wise Stacked Distribution of TGT-USD and ACT-USD",
            labels={"value": "USD Amount", "variable": "Type"},
            barmode="group",  # Stacked bar chart
        )
        st.plotly_chart(fig2, use_container_width=True)


    selected_one = st.selectbox("Select an option", options=["Region wise distribution", "Month wise distribution"])
    
    if selected_one == "Region wise distribution":

    # Step 1: Dropdown to Select Region (Simulating Clicks)
        selected_region = st.selectbox("Select a Region by Clicking on a Bar", options=["All"] + df["Region"].unique().tolist())

    # Step 4: Filter Data by Selected Region
        if selected_region != "All":
            st.write(f"### Data for Selected Region: {selected_region}")
            filtered_data = df[df["Region"] == selected_region]
            st.dataframe(filtered_data)

        # Additional Functionality for Selected Region
            if "POINT OF SALE" in df.columns:
                st.sidebar.subheader("Filter by Point of Sale")
                pos_options = df["POINT OF SALE"].unique().tolist()
                selected_pos = st.sidebar.selectbox("Select Point of Sale", options=["All"] + pos_options)

            # Filter data by selected Point of Sale
                if selected_pos != "All":
                    df = df[df["POINT OF SALE"] == selected_pos]

            # Display the corresponding CCY for the selected POS
                if "CCY" in df.columns:
                    unique_ccy = df["CCY"].unique()
                    if len(unique_ccy) == 1:
                        st.sidebar.write(f"**Currency (CCY) for POS '{selected_pos}':** {unique_ccy[0]}")
                    else:
                        st.sidebar.write(f"**Currencies (CCY) for POS '{selected_pos}':** {', '.join(unique_ccy)}")
                else:
                    st.sidebar.warning("CCY column not found in the dataset.")

    # Create two more columns for additional side-by-side plots
        col3, col4 = st.columns(2)

    # Plot 1: ACT-LC and TGT-LC by Month
        if "ACT -LC" in df.columns and "TGT-LC" in df.columns and "Month" in df.columns:
            with col3:
                st.subheader(f"ACT-LC and TGT-LC by Month - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")
            # Ensure "Month" column is categorical with the custom order
                df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
                df = df.sort_values("Month")

            # Aggregate by Month
                monthly_data = df.groupby("Month")[["ACT -LC", "TGT-LC"]].sum().reset_index()

            # Plot ACT-LC and TGT-LC curves
                fig1, ax1 = plt.subplots(figsize=(8, 4))  # Reduced size
                sns.lineplot(data=monthly_data, x="Month", y="ACT -LC", marker="o", label="ACT-LC", ax=ax1)
                sns.lineplot(data=monthly_data, x="Month", y="TGT-LC", marker="o", label="TGT-LC", ax=ax1)

                ax1.set_title("ACT-LC and TGT-LC by Month", fontsize=12)
                ax1.set_xlabel("Month", fontsize=10)
                ax1.set_ylabel("Values (LC)", fontsize=10)
                ax1.legend()
                plt.xticks(rotation=45, fontsize=9)
                plt.yticks(fontsize=9)
                st.pyplot(fig1)

    # Plot 2: ACT-USD and TGT-USD by Month
        if "ACT -USD" in df.columns and "TGT-USD" in df.columns and "Month" in df.columns:
            with col4:
                st.subheader(f"ACT-USD and TGT-USD by Month - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")
            # Aggregate ACT-USD and TGT-USD by month
                monthly_usd_data = df.groupby("Month")[["ACT -USD", "TGT-USD"]].sum().reset_index()

            # Plot ACT-USD and TGT-USD curves
                fig4, ax4 = plt.subplots(figsize=(8, 4))  # Reduced size
                sns.lineplot(data=monthly_usd_data, x="Month", y="ACT -USD", marker="o", label="ACT-USD", ax=ax4)
                sns.lineplot(data=monthly_usd_data, x="Month", y="TGT-USD", marker="o", label="TGT-USD", ax=ax4)

                ax4.set_title("ACT-USD and TGT-USD by Month", fontsize=12)
                ax4.set_xlabel("Month", fontsize=10)
                ax4.set_ylabel("Values (USD)", fontsize=10)
                ax4.legend()
                plt.xticks(rotation=45, fontsize=9)
                plt.yticks(fontsize=9)
                st.pyplot(fig4)

    # Create two more columns for additional side-by-side plots
        col5, col6 = st.columns(2)

    # Plot 3: VAR %-LC (ACT vsTGT) by Month
        if "VAR %-LC (ACT vsTGT)" in df.columns and "Month" in df.columns:
            with col5:
                st.subheader(f"Month-wise VAR %-LC (ACT vsTGT) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")
            # Aggregate "VAR %-LC (ACT vsTGT)" by month
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

    # Plot 4: VAR %-USD (ACT vsTGT) by Month
        if "VAR %-USD (ACT vsTGT)" in df.columns and "Month" in df.columns:
            with col6:
                st.subheader(f"Month-wise VAR %-USD (ACT vsTGT) - Region: {selected_region if 'selected_region' in locals() else 'All'} - POS: {selected_pos if 'selected_pos' in locals() else 'All'}")
            # Aggregate "VAR %-USD (ACT vsTGT)" by month
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



    if selected_one == "Month wise distribution":

    # Step 1: Dropdown to Select Region (Simulating Clicks)
        selected_month = st.selectbox("Select a Month by Clicking on a Bar", options=["All"] + df["Month"].unique().tolist())

    # Step 4: Filter Data by Selected Region
        if selected_month != "All":
            st.write(f"### Data for Selected Month: {selected_month}")
            filtered_data = df[df["Month"] == selected_month]
            st.dataframe(filtered_data)

            col1, col2 = st.columns([1, 2])  # Adjust column widths as needed

            with col1:
        # Plot Region-wise ACT-USD Pie Chart for the Selected Month
                fig_region_pie = px.pie(
                    filtered_data,
                    names="Region",
                    values="ACT -USD",
                    title=f"Region-wise Distribution of ACT-USD for {selected_month}",
                    labels={"Region": "Region", "ACT -USD": "Total ACT-USD"},
                )
                st.plotly_chart(fig_region_pie, use_container_width=True)

            with col2:
        # Create and Display the Comparative Bar Chart
                fig2 = px.bar(
                    filtered_data,
                    x="Region",
                    y=["TGT-USD", "ACT -USD"],  # Include both TGT-USD and ACT -USD
                    title=f"Region-wise Stacked Distribution of TGT-USD and ACT-USD - {selected_month}",
                    labels={"value": "USD Amount", "variable": "Type"},
                    barmode="group",  # Grouped bar chart for comparison
                )
                st.plotly_chart(fig2, use_container_width=True)

            selected_region = st.selectbox("Select a Region by Clicking on a Bar", options=["All"] + df["Region"].unique().tolist())

            col1, col2 = st.columns([1, 2]) 

            with col1:

                if selected_region != "All":
                    st.write(f"### High-demand Points of Sale in {selected_region} for {selected_month}")
            # Filter the data further based on selected region and sort by 'Sales' to get top 5
                    region_data = filtered_data[filtered_data["Region"] == selected_region]
                    top_5_sales = region_data.nlargest(5, "ACT -USD")  # Get top 5 based on Sales

            # Display the top 5 "POINT OF SALE" with highest sales
                    st.dataframe(top_5_sales[["POINT OF SALE", "ACT -USD"]])


            with col2:     
                if selected_region != "All":
                    fig_pos = px.bar(
                        top_5_sales,
                        x="ACT -USD",
                        y="POINT OF SALE",
                        orientation="h",  # Horizontal bar chart
                        title=f"Top 5 POINT OF SALE with Highest Demand in {selected_region} for {selected_month}",
                        labels={"ACT -USD": "Total ACT-USD", "POINT OF SALE": "Point of Sale"},
                    )
                    st.plotly_chart(fig_pos, use_container_width=True)
