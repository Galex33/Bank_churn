# from os import chdir
# chdir("..")
import pandas as pd
from utils.visualisation import *
from utils.prediction import *
from utils.pre_processing import *
import streamlit as st
from urllib.error import URLError

st.set_option('deprecation.showPyplotGlobalUse', False)

def get_data():
    df = pd.read_csv("app/data/data_vis.csv")
    return df

def intro():
    df = get_data()
    st.title("Cas pratique : Désengagement client")
    st.write("L'objet du cas présenté ici et d'ouvrir à de nouveaux outils, liés avec l'inteligence articfielle afin d'anticiper la départ des clients, dans le domaine de la banquaire.")
    st.write("Pour ce POC, les données sont issus d'une source libre (Kaggle.com).")
    st.write("Ne disposant pas des données internes ou de données de recettes conformes, les données présentés ici ne reflettent pas les clients de la banque.")
    st.write("Les données se répartissent suivant trois pays, Allemagne, Espagne et France.Les contextes économiques et sociaux de ces trois pays étant différents, nous avons séparés les données en foncitons des pays.")
    vis_general_country(df)
  

def Prediction_churn():
    st.title("Outil de calcul de la probalité de départ d'un client.")
    st.write("L'outil utilise trois modèles différent en fonction des pays (Allemagne, Espagne et France)")
    df = get_data()
    df['Genre'] = df['Genre'].replace(['Female','Male'], ['Femme','Homme'])
    df['MembreActif'] = df['MembreActif'].replace([0,1], ['Non','Oui'])
    with st.form("my_form", clear_on_submit=True):
        Age = st.number_input("Insérer l'age du client", min_value=1, step=1)
        Country = st.selectbox(
                "Choisissez le pays", list(df['Pays'].unique())
            )
        Balance = st.number_input("Insérer la balance du compte courant", min_value=0, step=1)
        MembreActif = st.selectbox(
                "Membre actif", list(df['MembreActif'].unique())
            )
        NbrDeProduit = st.number_input("Insérer le nombre de produit souscrit par le client", min_value=0, step=1)
        Genre = st.selectbox(
                "Choisissez le genre", list(df['Genre'].unique())
            )
        submitted = st.form_submit_button("Valider les informations")
        if submitted :
            dataframe = pre_process(Genre,Balance,NbrDeProduit,MembreActif,Age)
            dataframe = dataframe.drop(columns=['Age'])
            proba = get_prediction(dataframe,Country)
            st.title(f"Résumé des informations :")
            st.info(f"Age : {Age}, Pays : {Country}, Balance : {Balance}, MembreActif : {MembreActif}, NbrDeProduit : {NbrDeProduit}, Genre : {Genre}")
            if proba[0][0] < 0.25:
                st.warning("Risque trés élevé de désengagement du client")
            elif proba[0][0] >= 0.25 and proba[0][0] < 0.50:
                st.warning("Risque élevé de désengagement du client")
            elif proba[0][0] >= 0.50 and proba[0][0] < 0.75:
                st.info("Risque modéré de désengagement du client") 
            elif proba[0][0] >= 0.75:
                st.info("Risque faible de désengagement du client")    
            
def Vis_Country():
    df = get_data()
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        Visualisation des données par Pays
"""
    )
    try:
        Country = st.selectbox(
            "Choisissez le pays", list(df['Pays'].unique())
        )
        if not Country:
            st.error("Une erreur est survenue veuillez relancer la page")
        else:
            st.write(f"Matrice de correlation pour les données issus du pays {Country}")
            matrice_corr_country(df, Country)
            by_Country(df,Country)
            plot_variables(df, Country)
    except URLError as e:
        st.error(
            """
            **Accès internet requiert.**
            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "Accueil": intro,
    "Informations par Pays": Vis_Country,
    "Prédiction": Prediction_churn,
    
}

demo_name = st.sidebar.selectbox("Aller à", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

