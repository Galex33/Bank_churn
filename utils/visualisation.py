import pandas as pd
import numpy as np
#Visualizations library
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def matrice_corr_country(df, Country):
    df_cor_country = df[df['Pays']==Country]
    upp_mat = np.triu(df_cor_country.corr(method='pearson'))
    fig = plt.figure(figsize=(8,6))
    sns.heatmap(df_cor_country.corr(method='spearman'), vmin = -1, vmax = +1, annot = True, cmap = 'coolwarm', mask=upp_mat)
    return st.write(fig)

def vis_general(df):
    labels = 'Désengagés', 'Clients'
    sizes = [df.Desabonnement[df['Desabonnement']=="Oui"].count(), df.Desabonnement[df['Desabonnement']=="Non"].count()]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots(figsize=(2, 1))
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title("Proportion clients/désengagés", size = 5)
    fig = plt.show()
    return st.pyplot(fig)

def vis_general_country(df):
    sns.set_palette("Paired")
    fig = plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    label = df.Pays.value_counts().index
    label_count = df.Pays.value_counts().values
    plt.pie(data=df, x=label_count, labels=label, autopct='%1.1f%%', shadow=True, radius=1)
    plt.title("Répartition des données par pays")
    #Target feature distribution with Gender feature
    plt.subplot(1,2,2)
    sns.countplot(x='Desabonnement', data=df ,hue='Pays').set(title='Distribution des clients par pays')
    return st.pyplot(fig)
    
def by_Country(df,Country):
    sns.set_palette("Paired")
    df = df[df['Pays']==Country]
    df = df.astype({"Ancienneté" : 'object',"Genre": 'object','NbrDeProduit' : 'object','CarteDeCredit' : 'object','MembreActif':'object','Desabonnement':'object'})
    df_cat = df.select_dtypes(include='object').columns.drop(["Desabonnement"])
    plt.figure(figsize=(35,39))
    for i,cat_fea in enumerate(df_cat):
        plt.subplot(5,2,i+1)
        sns.countplot(x=cat_fea,hue='Desabonnement',data=df,edgecolor="black")
        plt.title("Histogramme de {} en fonction de la souscription".format(cat_fea))
        plt.legend(labels=['Client', 'Désengagé'])
        fig = plt.tight_layout() 
        st.set_option('deprecation.showPyplotGlobalUse', False)   
    return st.pyplot(fig)


    
def plot_variables(df,Country):  
    df = df[df['Pays']==Country]
    df = df.astype({"Ancienneté" : 'object',"Genre": 'object','NbrDeProduit' : 'object','CarteDeCredit' : 'object','MembreActif':'object','Desabonnement':'object'})
    sns.set()
    list_var_num = df.select_dtypes(exclude='object').columns
    fig, axes = plt.subplots(nrows=len(list_var_num), ncols=2, figsize = (14, 8), constrained_layout=True)
    for i, variable in enumerate(list_var_num): 
        sns.histplot(data = df, x=variable, kde = True, hue=df["Desabonnement"], ax=axes[i,0])
        sns.boxplot(data = df, x=variable, ax=axes[i,1])
    fig.suptitle('Histogrammes et boxplots des variables numériques', size=20)
    fig = plt.tight_layout() 
    st.set_option('deprecation.showPyplotGlobalUse', False)   
    return st.pyplot(fig)

