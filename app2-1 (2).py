import streamlit as st
import pandas as pd
import plotly.express as px
import json
import unicodedata  

st.set_page_config(page_title="Immigration en Tunisie", layout="wide")
st.title("📊 Tableau de bord - Immigration en Tunisie (2020-2021)")

@st.cache_data
def charger_donnees():
    xls = pd.ExcelFile("immigration_tunisie_nettoye (1).xlsx", engine="openpyxl")
    return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

donnees = charger_donnees()
# 🌍 Sidebar
st.sidebar.title("📂 Navigation")
st.sidebar.markdown("**Explorez les données de l'enquête Tunisia-HIMS**")
st.sidebar.markdown("---")

menu = st.sidebar.radio("🔍 Menu :", [
    "Accueil",
    "Répartition par origine",
    "Profil général",
    "Motifs d'immigration",
    "Éducation & emploi",
    "Répartition géographique"
])

st.sidebar.markdown("---")
st.sidebar.caption("Projet DS2 – 1 BI | Syrine Belkhiria, Khadija Naccache, Sameh Kchaou, Nabil Ben Ghalia & Nour Farhat")

if menu == "Accueil":
    st.markdown("## 👋 Bienvenue")
    st.write("""
    Ce tableau de bord interactif vous invite à explorer les résultats de l'enquête nationale Tunisia-HIMS sur l'immigration en Tunisie, réalisée entre 2020 et 2021.  
    Il vise à offrir une vision claire, synthétique et interactive du profil des immigrés vivant en Tunisie, ainsi que de leur répartition géographique, leurs motivations, et leur insertion socio-économique.

    ### 🔍 Objectifs du tableau de bord :
    - Analyser les **origines géographiques** des immigrés.
    - Comprendre leurs **motivations d’installation** en Tunisie.
    - Étudier leurs **caractéristiques démographiques** (âge, sexe, niveau d’instruction, statut matrimonial).
    - Explorer leur **situation professionnelle** (emploi, secteur d’activité, statut).
    - Visualiser leur **répartition sur le territoire tunisien** via une carte interactive.

    > Ce projet s’inscrit dans une démarche d’analyse exploratoire des données pour mieux comprendre les dynamiques migratoires et éclairer les décisions publiques.
    """)

elif menu == "Répartition par origine":
    st.subheader("🌍 Répartition par origine géographique")
    df = donnees["Origine"]
    st.dataframe(df)
    fig = px.pie(df, names="Région d'origine", values="Nombre d'immigrés", hole=0.3)
    st.plotly_chart(fig)
    st.download_button( 
        label="📥 Télécharger les données",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='DonnéesrepartitionParregion.csv',
        mime='text/csv'
    )

elif menu == "Profil général":
    st.subheader("👤 Structure par âge")
    df = donnees["Structure par âge"]
    st.dataframe(df)
    fig = px.bar(df, x="Groupe d'âge", y="Nombre d'immigrés", color="Groupe d'âge", text="Nombre d'immigrés")
    st.plotly_chart(fig)

    st.download_button(  # <-- bien à l'intérieur du bloc
        label="📥 Télécharger les données",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesprofil_general.csv',
        mime='text/csv'
    )



elif menu == "Motifs d'immigration":
    st.subheader("📌 Motifs d'immigration (Hommes vs Femmes)")
    
    df = donnees["Motifs (genre)"]

    # Filtre local par sexe
    sexe_selectionne = st.selectbox("👥 Filtrer par sexe :", ["Tous", "Hommes", "Femmes"])

    # Affichage tableau brut
    st.dataframe(df)

    # Affichage graphique selon filtre
    if sexe_selectionne == "Tous":
        fig = px.bar(
            df,
            y="Motif d'immigration",
            x=["Hommes", "Femmes"],
            orientation='h',
            title="Motifs d'immigration selon le sexe",
            barmode="group"
        )
    else:
        fig = px.bar(
            df,
            y="Motif d'immigration",
            x=sexe_selectionne,
            orientation='h',
            title=f"Motifs d'immigration – {sexe_selectionne}",
            color_discrete_sequence=["#636EFA"] if sexe_selectionne == "Hommes" else ["#EF553B"]
        )

    st.plotly_chart(fig)

    # Bouton de téléchargement
    st.download_button(
        label="📥 Télécharger les données",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesmotifs_immigration.csv',
        mime='text/csv'
    )
elif menu == "Motifs d'immigration":
    st.subheader("📌 Motifs d'immigration (Hommes vs Femmes)")
    
    df = donnees["Motifs (genre)"]

    # Filtre local par sexe
    sexe_selectionne = st.selectbox("👥 Filtrer par sexe :", ["Tous", "Hommes", "Femmes"])

    # Affichage tableau brut
    st.dataframe(df)

    # Affichage graphique selon filtre
    if sexe_selectionne == "Tous":
        fig = px.bar(
            df,
            y="Motif d'immigration",
            x=["Hommes", "Femmes"],
            orientation='h',
            title="Motifs d'immigration selon le sexe",
            barmode="group"
        )
    else:
        fig = px.bar(
            df,
            y="Motif d'immigration",
            x=sexe_selectionne,
            orientation='h',
            title=f"Motifs d'immigration – {sexe_selectionne}",
            color_discrete_sequence=["#636EFA"] if sexe_selectionne == "Hommes" else ["#EF553B"]
        )

    st.plotly_chart(fig)

    # Bouton de téléchargement
    st.download_button(
        label="📥 Télécharger les données",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesmotifs_immigration.csv',
        mime='text/csv'
    )





elif menu == "Éducation & emploi":
    # 🎯 Filtre sexe dans la sidebar
    sexe_selectionne = st.sidebar.selectbox("👥 Filtrer par sexe :", ["Tous", "Hommes", "Femmes"])

    st.subheader("🎓 Niveau d'instruction")
    df = donnees["Instruction"]
    st.dataframe(df)

    # Préparer les données pour le graphe
    df_melted = df.melt(id_vars=["Niveau d'instruction"], var_name="Sexe", value_name="Proportion")

    if sexe_selectionne != "Tous":
        df_melted = df_melted[df_melted["Sexe"] == sexe_selectionne]

    fig = px.line(
        df_melted,
        x="Niveau d'instruction", y="Proportion", color="Sexe",
        markers=True,
        title="Évolution du niveau d’instruction selon le sexe"
    )
    st.plotly_chart(fig)

    # ✅ Télécharger instruction
    st.download_button(
        label="📥 Télécharger les données (instruction)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesinstruction.csv',
        mime='text/csv'
    )

    st.subheader("💼 Activité économique")
    df2 = donnees["Activité"]
    st.dataframe(df2)

    if sexe_selectionne == "Tous":
        fig2 = px.bar(df2, x="Type d'activité", y=["Hommes", "Femmes"], barmode="group")
    else:
        fig2 = px.bar(df2, x="Type d'activité", y=sexe_selectionne, barmode="group")

    st.plotly_chart(fig2)

    # ✅ Télécharger activité
    st.download_button(
        label="📥 Télécharger les données (activité)",
        data=df2.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesactivite_economique.csv',
        mime='text/csv'
    )



elif menu == "Répartition géographique":
    st.subheader("🗺️ Carte des immigrés par gouvernorat")

    

    def normalize(text):
        return unicodedata.normalize('NFKD', text).encode('ascii', errors='ignore').decode('utf-8').lower()

    df_gouv = donnees["Répartition géographique"]
    df_gouv["Gouvernorat_norm"] = df_gouv["Gouvernorat"].apply(normalize)

    with open("TN-gouvernorats.geojson", encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson["features"]:
        feature["properties"]["name_norm"] = normalize(feature["properties"]["gouv_fr"])

    fig = px.choropleth(
        df_gouv,
        geojson=geojson,
        featureidkey="properties.name_norm",
        locations="Gouvernorat_norm",
        color="Nombre D'immigrés", 
        color_continuous_scale="Tealgrn",
        title="Carte des immigrés par gouvernorat"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

    st.download_button(  # <-- ici aussi, bien indenté
        label="📥 Télécharger les données",
        data=df_gouv.to_csv(index=False).encode('utf-8'),
        file_name='Donnéesrepartition_geographique.csv',
        mime='text/csv'
    )


