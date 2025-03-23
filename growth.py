# import
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# setup our app
st.set_page_config (page_title = "💿 Data Sweeper", layout='wide')
st.title("💿 Data Sweeper")
st.write ("Transform files between CSV and Excel formats with built-in data cleaning and visualisation")

# upload your file
upload_file = st.file_uploader("Upload your file (CSV or Excel):", type = ["csv", "xlsx"],accept_multiple_files=True)

# logic
if upload_file :
    for file in upload_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
          df = pd.read_csv (file)
        elif file_ext == ".xlsx":
          df = pd.read_excel (file)
        else :
            st.error (f"Unsupported file type :{file_ext}")
            continue

        # display info about file
        st.write (f"File name : {file.name}")
        st.write (f"File size : {file.size / 1024}")

        # show 5 rows of our df
        st.write ("Preview the Head of Dataframe")
        st.dataframe(df.head())

        # option for data cleaning
        st.subheader ("Data Cleaning Options")
        if st.checkbox (f" Clean Data for {file.name}"):
           col1, col2 = st.columns (2)

           with col1:
              if st.button (f"Remove duplicates from {file.name}"):
                 df.drop_duplicates (inplace=True)
                 st.write ("Duplicate removed")

              with col2:
                if st.button (f"Fill missing values for {file.name}"):
                  numeric_cols = df.select_dtypes (include= ['number']).columns
                  df [numeric_cols] = df[numeric_cols].fillna (df[numeric_cols].mean())
                  st.write ("Missing value have been filled")

       # Choose specific columns to keep or convert
        st.subheader ("Select to Convert")
        column = st.multiselect (f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[column]


        # Visualisation
        st.subheader ("📊Data Visualisation")
        if st.checkbox (f"Show Visualisation for {file.name}"):
          st.bar_chart (df.select_dtypes(include='number').iloc [:,:2])

        # Convert the file
        st.subheader ("💿 Conversion option")
        conversion_type = st.radio (f"Convert {file.name} to:", ["CSV", "Excel"], key= file.name)
        if st.button (f"Convert {file.name}"):
           buffer = BytesIO()
           if conversion_type =="CSV":
            df. to_csv (buffer,index=False)
            file_name = file.name.replace (file_ext,".csv")
            mime_type = "txt/csv"

           elif conversion_type =="Excel":
            df. to_excel (buffer,index=False)
            file_name = file.name.replace (file_ext,".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

        # Download button
        st.download_button (
                            label=f"⌛ Download {file.name} as {conversion_type}",
                            data=buffer,
                            file_name = file_name,
                            mime=mime_type,
                            )

        st.success ("All files processed")  








