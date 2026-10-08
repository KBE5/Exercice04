import requests
import streamlit as st

st.title("Bilan Analytique Global")

if "token" not in st.session_state:
    st.warning("Veuillez vous connecter sur la page d'accueil")
else:
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    res = requests.get("http://127.0.0.1:8000/analytics/bilan", headers=headers)

    if res.status_code == 200:
        data = res.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Observations", data.get("nb_observations"))
        col2.metric("Total Visiteurs", data.get("total_visiteurs"))
        col3.metric("Moyenne", data.get("moyenne_visiteurs"))

    elif res.status_code == 403:
        st.error("Accès refusé : réservé au rôle 'analyst'.")
    else:
        st.error(f"Erreur HTTP {res.status_code} : {res.text}")