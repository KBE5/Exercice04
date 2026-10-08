import requests 
import pandas as pd 
import streamlit as st 

st.title ("Consultation de la fréquentation")

if "page_num" not in st.session_state:
    st.session_state["page_num"] = 1

res = requests.get(
    "http://127.0.0.1:8000/frequentations",
    params={"page": st.session_state["page_num"], "page_size": 5},
)

if res.status_code == 200: 
    data = res.json()
    items = data.get("items", [])
    total_pages  = data.get("pages", 1)

    st.write(f"Page{st.session_state['page_num']} sur {total_pages}")

    #affichage tab 
    df = pd.DataFrame(data["items"])
    st.dataframe(df, width="stretch")
    

    col1, col2 = st.columns(2)
    if col1.button("Précédent", disabled=(st.session_state["page_num"] <= 1)):
        st.session_state["page_num"] -= 1
        st.rerun()

    if col2.button("Suivant", disabled=(st.session_state["page_num"] >= total_pages)):
        st.session_state["page_num"] += 1
        st.rerun()
