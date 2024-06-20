# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(layout='wide')
st.title("Geoinformation feedback Portal")
# st.markdown("Enter the details of the new area")

conn = st.connection("gsheets", type=GSheetsConnection)


existing_data = conn.read(worksheet="population", usecols=list(range(18)), ttl=5)
# data = conn.read(spreadsheet=url, usecols=[0, 1])
existing_data= existing_data.dropna(how='all')

st.dataframe(existing_data)
# st.markdown(type(existing_data.columns[0]))

address1 = [
    "Welche Fachbereiche der Stadt Kerpen könnten von dem InfoTool zur Klimaanpassung profitieren und dieses auch nutzen?",
    "Welche Abteilung soll der Ansprechpartner für das InfoTool zur Klimaanpassung sein?",
    "Sollte das InfoTool auch für andere Nutzer/Städtepartner zur Verfügung stehen, z.B. Wasser-/Umweltverbände, Bürgerinitiativen, Universitäten und Schulen?",
    "Was sind Ihrer Meinung nach die größten Herausforderungen/Gefahren in Bezug auf den Klimawandel für die Stadt Kerpen?",
    "Welche sind Ihrer Meinung nach die wichtigsten Sektoren, die sich in der Stadt Kerpen mit Klimaanpassung befassen, z.B. Klima-/Umweltabteilungen, Stadtplaner, Wasserwirtschaft, Landwirtschaft, Bergbau, Industrie, Rettungsdienste, usw.?",
]


qualification1 = [
    "Geography",
    "Geology",
    "Urban Planning",
    "Climate Protection",
    "Disaster Risk Assessment",
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    st.subheader("Department*")
    name = st.text_input(label="answer :")
    address = st.subheader("Q1. Welche Fachbereiche der Stadt Kerpen könnten von dem InfoTool zur Klimaanpassung profitieren und dieses auch nutzen?")#st.selectbox("question1*", options=address1, index=None)
    answer= st.radio('answer',["Statistics","Geodata Management","Climate Protection","Environmental Monitoring","Geology"])#st.text_area(label="answer1")
    address2 = st.subheader("Q2. Welche Abteilung soll der Ansprechpartner für das InfoTool zur Klimaanpassung sein?")#st.selectbox("question2*", options=address1, index=None)
    answer2= st.text_area(label="answer2 :")
    address3 = st.subheader("Q3. Sollte das InfoTool auch für andere Nutzer/Städtepartner zur Verfügung stehen, z.B. Wasser-/Umweltverbände, Bürgerinitiativen, Universitäten und Schulen?") #st.selectbox("question3*", options=address1, index=None)
    answer3= st.text_area(label="answer3 :")
    address4 = st.subheader("Q4.  Was sind Ihrer Meinung nach die größten Herausforderungen/Gefahren in Bezug auf den Klimawandel für die Stadt Kerpen?") #st.selectbox("question4*", options=address1, index=None)
    answer4= st.text_area(label="answer4 :")
    address5 = st.subheader("Q5. Welche sind Ihrer Meinung nach die wichtigsten Sektoren, die sich in der Stadt Kerpen mit Klimaanpassung befassen, z.B. Klima-/Umweltabteilungen, Stadtplaner, Wasserwirtschaft, Landwirtschaft, Bergbau, Industrie, Rettungsdienste, usw. ?")#st.selectbox("question5*", options=address1, index=None)
    answer5= st.text_area(label="answer5 :")
    st.subheader("Products Offered")
    qualification = st.radio("answer6 :",options=qualification1)
    st.subheader("Region/City")
    country = st.text_input(label="answer7 :") 
    st.subheader("Population")
    population = st.number_input(label="answer8 :",min_value=0)
    st.subheader("Years in Business")
    age = st.slider("answer9 :", 0, 50, 5)
    st.subheader("Additional Notes")
    additional_info = st.text_area(label="answer10 :")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Survey Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not name or not address:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data[existing_data.columns[0]].astype(str).str.contains(name).any():
            st.warning("A vendor with this company name already exists.")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "name": name,
                        "address": address1[0],
                        "answer": answer,
                        "address2": address1[1],
                        "answer2": answer2,
                        "address3": address1[2],
                        "answer3": answer3,
                        "address4": address1[3],
                        "answer4": answer4,
                        "address5": address1[4],
                        "answer5": answer4,
                        "qualification": ", ".join(qualification),
                        "answer": answer,
                        "country": country,
                        "population": population,
                        #"OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "age": age,
                        "additional": additional_info
                    }
                ]
            )

            st.dataframe(vendor_data)
            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
            st.dataframe(updated_df)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="population", data=updated_df)

            st.success("Survey details successfully submitted!")