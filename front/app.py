import requests 
import streamlit as st 

st.title("Médiathèque - Observatoire de fréquentation")
st.caption ("Application Streamlit")

if "token" in st.session_state:
    st.sidebar.success(f"Connecté: {st.session_state['username']}")
    if st.sidebar.button ("Deconnexion"):
        st.session_state.clear()
        st.rerun()

#page connexion
st.header("Connexion")
if "token" in st.session_state: 
    st.info("Cous êtes connecté! Utilisez la sidebarà gauche pour naviguer")
else:
    with st.form("form_login"):
        username = st.text_input("Nom utilisateur")
        password = st.text_input("Mot de passe", type="password")
        valider = st.form_submit_button("Se connecter")

        if valider: #appel de l'api si validé
            try: 
                res = requests.post(
                "http://127.0.0.1:8000/auth/login",
                json={"username": username, "password": password},
                )

                if res.status_code == 200:
                    data = res.json()
                    
                    st.session_state["token"] = data["access_token"]
                    st.session_state["role"] = data["role"]
                    st.session_state["username"] = username
                    st.success("Connexion réussie !")
                    st.rerun()

                else:
                    st.error("Identifaiants incorrects")
            
            except requests.exceptions.ConnectionError:
                st.error("Impossible de contacter le serveur. Vérifiez qu'Uvicorn est lancé")