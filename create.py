import pandas as pd
import streamlit as st
from io import BytesIO

st.markdown(
    """
    <style>
        .stApp {
            background-image: url('https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/296123869/original/749841b6fe8407b9d3136432086c76acb6d0d59c/solve-your-complex-spreadsheet-problems-as-excel-pro-with-10-years-of-experience.jpg');
            background-size: cover;
            background-position: center;
        }
        .stTitle, .stSubheader, .stHeader, .stDataFrame, .stText, .stMarkdown {
            font-size: 20px;
            color: red;  /* Set text color to red */
        }
        .stButton, .stSelectbox, .stTextInput, .stRadio, .stSlider, .stFileUploader, .stMultiselect {
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



# Title for the app
st.title("Create the Dataset Before Uploading for Analysis")
st.write("""
This application allows you to upload multiple Excel files, process them to include additional details 
(such as region mapping and month), and download the combined data as an Excel file for further analysis.
""")


# File uploader for multiple files
uploaded_files = st.file_uploader(
    "Upload your Excel files (select multiple if needed)", 
    type=["xlsx"], 
    accept_multiple_files=True
)

# List of months for the dropdown
months_list = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# New column names (18 columns + Month)
new_column_names = [
    "POINT OF SALE", "CCY", "ACT -LC", "TGT-LC", "VAR %-LC (ACT vsTGT)", 
    "LYR-LC (2023/24)", "VAR %-LC (ACT vs LYR)", "ACT -USD", "TGT-USD", 
    "VAR %-USD (ACT vsTGT)", "LYR-USD (2023/24)", "VAR %-USD (ACT vs LYR)", 
    "Act. Using-Bgt. ex. Rates", "Exchange - gain/( loss)", 
    "Act. Using- LY. Ex. Rates", "Exchange -gain/(loss)_LY", 
    "REVENUE CONT. % - Actual", "REVENUE CONT. %-LYR", "Month"
]

# List of values to exclude in the 'POINT OF SALE' column
exclude_values = [
    'CHINA TOTAL', 'FAR EAST TOTAL', 'EUROPE TOTAL', 'TOTAL U.A.E.',
    'SAUDI ARABIA TOTAL', 'M.EAST AND S.AFRICA TOTAL', 'INDIA TOTAL',
    'PAKISTAN-TOTAL', 'MALDIVES-TOTAL', 'ISC TOTAL', 'BUDGETD POS TOTAL'
]

# Define the region mapping dictionary (as provided above)
region_mapping = {
    # Far East Region
    'AUSTRALIA': 'FAR EAST', 'CHINA EAST': 'FAR EAST', 'CHINA REST': 'FAR EAST',
    'CHINA SOUTH': 'FAR EAST', 'HONG KONG': 'FAR EAST', 'INDONESIA': 'FAR EAST', 'JAPAN': 'FAR EAST',
    'MALAYSIA': 'FAR EAST', 'NEW ZEALAND': 'FAR EAST', 'PHILIPPINES': 'FAR EAST',
    'SINGAPORE': 'FAR EAST', 'SOUTH KOREA': 'FAR EAST', 'TAIWAN': 'FAR EAST',
    'THAILAND': 'FAR EAST', 'UNION OF MYANMAR': 'FAR EAST', 'VIETNAM': 'FAR EAST',

    # Europe Region
    'AUSTRIA': 'EUROPE', 'BELGIUM': 'EUROPE', 'CANADA': 'EUROPE', 'CYPRUS': 'EUROPE',
    'CZECH REPUBLIC': 'EUROPE', 'DENMARK': 'EUROPE', 'FINLAND': 'EUROPE', 'FRANCE': 'EUROPE',
    'GERMANY': 'EUROPE', 'GREECE': 'EUROPE', 'ICELAND': 'EUROPE', 'IRELAND': 'EUROPE',
    'ISRAEL': 'EUROPE', 'ITALY': 'EUROPE', 'LUXEMBOURG': 'EUROPE', 'NETHERLANDS': 'EUROPE',
    'NORWAY': 'EUROPE', 'POLAND': 'EUROPE', 'PORTUGAL': 'EUROPE', 'RUSSIAN FEDERATION': 'EUROPE',
    'SLOVAKIA': 'EUROPE', 'SPAIN': 'EUROPE', 'SWEDEN': 'EUROPE', 'SWITZERLAND': 'EUROPE',
    'TURKEY': 'EUROPE', 'UNITED KINGDOM': 'EUROPE', 'UNITED STATES OF AMERICA': 'EUROPE',

    # M.EAST AND S.AFRICA Region
    'ABU DHABI & AL AIN': 'M.EAST AND S.AFRICA', 'Dubai': 'M.EAST AND S.AFRICA',
    'Dubai - SHARJAH': 'M.EAST AND S.AFRICA', 'Dubai - NORTHERN EMIRATES': 'M.EAST AND S.AFRICA',
    'BAHRAIN': 'M.EAST AND S.AFRICA', 'KUWAIT': 'M.EAST AND S.AFRICA', 'OMAN': 'M.EAST AND S.AFRICA',
    'QATAR': 'M.EAST AND S.AFRICA', 'SEYCHELLES': 'M.EAST AND S.AFRICA', 'SAUDI CENTRAL': 'M.EAST AND S.AFRICA',
    'SAUDI EASTERN': 'M.EAST AND S.AFRICA', 'SAUDI JEDDAH': 'M.EAST AND S.AFRICA', 'SOUTH AFRICA': 'M.EAST AND S.AFRICA',

    # India Region
    'INDIA AHMEDABAD': 'INDIA', 'INDIA GOA': 'INDIA', 'INDIA HYDERABAD': 'INDIA',
    'INDIA VISHAKHAPATNAM': 'INDIA', 'INDIA KARNATAKA': 'INDIA', 'INDIA KERALA - COCHIN': 'INDIA',
    'INDIA KERALA CALICUT': 'INDIA', 'INDIA EASTERN KOLKATA': 'INDIA', 'INDIA NORTHERN': 'INDIA',
    'INDIA TAMILNADU - CHENNAI': 'INDIA', 'INDIA TAMILNADU COIMBATORE': 'INDIA',
    'INDIA TAMILNADU-MADURAI': 'INDIA', 'INDIA TAMILNADU TIRICHI': 'INDIA',
    'INDIA TRIVANDRUM': 'INDIA', 'INDIA WESTERN': 'INDIA',

    # ISC Region
    'BANGLADESH': 'ISC', 'NEPAL': 'ISC', 'PAKISTAN-LAHORE': 'ISC',
    'MALDIVES-GAN': 'ISC', 'MALDIVES-MALE': 'ISC', 'PAKISTAN-KARACHI': 'ISC',

    # Sri Lanka Region
    'SRI LANKA': 'SRI LANKA'
}

if uploaded_files:
    file_data = {}
    
    for file in uploaded_files:
        st.write(f"File uploaded: {file.name}")
        month = st.selectbox(f"Select the month for {file.name}", months_list, key=file.name)
        
        if month:
            df = pd.read_excel(file, skiprows=4).iloc[:, :18]
            df = df.dropna()
            df['Month'] = month
            df.columns = new_column_names
            df = df[~df['POINT OF SALE'].isin(exclude_values)]
            
            # Map 'POINT OF SALE' to 'Region'
            df['Region'] = df['POINT OF SALE'].map(region_mapping)
            
            # Store processed DataFrame
            file_data[month] = df

    # Combine all dataframes
    if file_data:
        combined_df = pd.concat(file_data.values(), ignore_index=True)
        
        # Display the combined dataframe
        st.write("Combined DataFrame:")
        st.dataframe(combined_df)
        
        # Provide a download link for the combined data as an Excel file
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='Combined Data')
        
        st.download_button(
            label="Download Combined Data as Excel",
            data=excel_buffer.getvalue(),
            file_name="combined_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )




