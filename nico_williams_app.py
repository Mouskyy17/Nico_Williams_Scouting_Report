import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# Configuration de la page
st.set_page_config(
    page_title="Nico Williams - Scouting Report",
    page_icon="⚽",
    layout="wide"
)

# Données de Nico Williams (intégrées directement)
data = {
    'Statistic': [
        'Goals', 'Assists', 'Goals + Assists', 'Non-Penalty Goals', 'xG: Expected Goals', 
        'npxG: Non-Penalty xG', 'xAG: Exp. Assisted Goals', 'Progressive Carries', 
        'Progressive Passes', 'Progressive Passes Rec', 'Shots Total', 'Shots on Target',
        'Key Passes', 'Passes into Final Third', 'Passes into Penalty Area', 
        'Crosses into Penalty Area', 'Crosses', 'Shot-Creating Actions', 'Goal-Creating Actions',
        'Take-Ons Attempted', 'Successful Take-Ons', 'Carries into Final Third', 
        'Carries into Penalty Area', 'Touches (Att 3rd)', 'Touches (Att Pen)', 
        'Progressive Carrying Distance', 'Total Carrying Distance'
    ],
    'Per 90': [
        0.31, 0.21, 0.52, 0.31, 0.21, 0.21, 0.17, 5.69, 3.09, 11.07, 2.51, 0.92,
        2.05, 1.07, 1.41, 0.4, 5.05, 5.29, 0.61, 8.62, 3.43, 2.75, 2.51, 31.16, 5.05,
        140.46, 258.5
    ],
    'Percentile': [
        57, 61, 59, 64, 38, 43, 38, 94, 34, 88, 69, 60, 79, 14, 50, 66, 84, 89, 80,
        99, 98, 81, 89, 85, 68, 89, 88
    ]
}

df = pd.DataFrame(data)

# Titre principal avec style
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #004D9F; font-size: 3rem; margin-bottom: 0.5rem;">⚽ NICO WILLIAMS</h1>
    <h2 style="color: #DC143C; font-size: 1.5rem; margin-bottom: 1rem;">Scouting Report - Ailier Gauche</h2>
    <h3 style="color: #666; font-size: 1.2rem;">Profil Idéal pour le FC Barcelone</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar avec informations du joueur
st.sidebar.markdown("## 📊 Informations Joueur")
st.sidebar.markdown("""
**Nom:** Nico Williams  
**Poste:** Ailier Gauche  
**Club Actuel:** Athletic Bilbao  
**Nationalité:** Espagne  
**Âge:** 22 ans
""")

st.sidebar.markdown("## 🎯 Points Clés")
st.sidebar.markdown("""
- **Dribbleur exceptionnel** (99e percentile)
- **Créateur de danger** (89e percentile)
- **Porteur de balle prolifique** (94e percentile)
- **Polyvalence offensive** confirmée
""")

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🥅 Buts + Passes", "0.52/90min", "59e percentile")
    
with col2:
    st.metric("🎯 Actions Créatrices", "5.29/90min", "89e percentile")
    
with col3:
    st.metric("🏃‍♂️ Dribbles Tentés", "8.62/90min", "99e percentile")
    
with col4:
    st.metric("📈 Portées Progressives", "5.69/90min", "94e percentile")

# Section principale avec onglets
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Analyse Offensive", "📊 Comparaison Elite", "🔥 Points Forts", "📈 Recommandations"])

with tab1:
    st.header("🎯 Profil Offensif Complet")
    
    # Graphique radar des capacités offensives
    categories_offensives = [
        'Goals + Assists', 'Shot-Creating Actions', 'Goal-Creating Actions',
        'Take-Ons Attempted', 'Successful Take-Ons', 'Progressive Carries',
        'Crosses', 'Key Passes', 'Progressive Passes Rec'
    ]
    
    percentiles_offensifs = []
    valeurs_offensives = []
    
    for cat in categories_offensives:
        idx = df[df['Statistic'] == cat].index[0]
        percentiles_offensifs.append(df.loc[idx, 'Percentile'])
        valeurs_offensives.append(df.loc[idx, 'Per 90'])
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=percentiles_offensifs,
        theta=categories_offensives,
        fill='toself',
        name='Nico Williams',
        line_color='#DC143C',
        fillcolor='rgba(220, 20, 60, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                ticktext=['20e', '40e', '60e', '80e', '100e']
            )
        ),
        showlegend=True,
        title="Percentiles des Capacités Offensives",
        height=600
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Graphiques comparatifs
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique des actions créatrices
        creation_data = df[df['Statistic'].isin(['Shot-Creating Actions', 'Goal-Creating Actions'])]
        
        fig_creation = px.bar(
            creation_data, 
            x='Statistic', 
            y='Per 90',
            color='Percentile',
            color_continuous_scale='Reds',
            title="Actions Créatrices par 90 minutes"
        )
        fig_creation.update_layout(height=400)
        st.plotly_chart(fig_creation, use_container_width=True)
    
    with col2:
        # Graphique des dribbles
        dribble_data = df[df['Statistic'].isin(['Take-Ons Attempted', 'Successful Take-Ons'])]
        
        fig_dribbles = px.bar(
            dribble_data,
            x='Statistic',
            y='Per 90',
            color='Percentile',
            color_continuous_scale='Blues',
            title="Capacités de Dribble par 90 minutes"
        )
        fig_dribbles.update_layout(height=400)
        st.plotly_chart(fig_dribbles, use_container_width=True)

with tab2:
    st.header("📊 Comparaison avec l'Elite Européenne")
    
    # Métriques clés pour un ailier de Barcelone
    metriques_barca = [
        'Progressive Carries', 'Progressive Passes Rec', 'Take-Ons Attempted',
        'Successful Take-Ons', 'Shot-Creating Actions', 'Key Passes', 'Crosses'
    ]
    
    # Graphique en barres horizontales
    barca_data = df[df['Statistic'].isin(metriques_barca)].copy()
    
    fig_comparison = px.bar(
        barca_data,
        x='Percentile',
        y='Statistic',
        orientation='h',
        color='Percentile',
        color_continuous_scale='RdYlGn',
        title="Position de Nico Williams vs Ailiers Européens (Percentiles)"
    )
    
    # Ajouter des lignes de référence
    fig_comparison.add_vline(x=75, line_dash="dash", line_color="green", 
                           annotation_text="Niveau Elite (75e percentile)")
    fig_comparison.add_vline(x=90, line_dash="dash", line_color="gold", 
                           annotation_text="Niveau Exceptionnel (90e percentile)")
    
    fig_comparison.update_layout(height=500)
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Analyse des percentiles élevés
    st.subheader("🌟 Domaines d'Excellence")
    percentiles_eleves = df[df['Percentile'] >= 80].sort_values('Percentile', ascending=False)
    
    for idx, row in percentiles_eleves.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{row['Statistic']}**")
        with col2:
            st.write(f"{row['Per 90']}/90min")
        with col3:
            if row['Percentile'] >= 95:
                st.write(f"🔥 {row['Percentile']}e")
            elif row['Percentile'] >= 85:
                st.write(f"⭐ {row['Percentile']}e")
            else:
                st.write(f"✅ {row['Percentile']}e")

with tab3:
    st.header("🔥 Points Forts pour Barcelone")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏃‍♂️ Qualités de Dribble")
        st.markdown("""
        **Dribbles tentés: 8.62/90min (99e percentile)**
        - Le plus haut niveau européen
        - Capacité à éliminer plusieurs adversaires
        - Créateur de surnombre offensif
        
        **Dribbles réussis: 3.43/90min (98e percentile)**
        - Efficacité remarquable (40% de réussite)
        - Déstabilise les défenses organisées
        - Libère des espaces pour les coéquipiers
        """)
        
        st.subheader("📈 Progression du Jeu")
        st.markdown("""
        **Portées progressives: 5.69/90min (94e percentile)**
        - Transport de balle exceptionnel
        - 140.46m de distance progressive/90min
        - Transition défense-attaque rapide
        """)
    
    with col2:
        st.subheader("🎯 Création d'Occasions")
        st.markdown("""
        **Actions créatrices de tir: 5.29/90min (89e percentile)**
        - Danger permanent sur son flanc
        - Multiplication des occasions d'équipe
        - Intelligence de jeu développée
        
        **Passes clés: 2.05/90min (79e percentile)**
        - Vision du jeu remarquable
        - Précision dans le dernier geste
        - Complément parfait aux meneurs catalans
        """)
        
        st.subheader("🎲 Polyvalence Offensive")
        st.markdown("""
        **Centres: 5.05/90min (84e percentile)**
        - Qualité de centre élevée
        - Variété dans les trajectoires
        - Danger aérien pour l'équipe
        """)
    
    # Graphique synthèse des forces
    forces_data = pd.DataFrame({
        'Domaine': ['Dribble', 'Progression', 'Création', 'Polyvalence'],
        'Score_Moyen': [98.5, 91.5, 84, 82],
        'Impact_Barca': [10, 9, 9, 8]
    })
    
    fig_forces = px.scatter(
        forces_data,
        x='Score_Moyen',
        y='Impact_Barca',
        size='Impact_Barca',
        color='Domaine',
        title="Impact des Forces de Nico Williams pour le Système Barcelone"
    )
    fig_forces.update_layout(
        xaxis_title="Niveau Européen (Percentile Moyen)",
        yaxis_title="Impact Potentiel pour Barcelone (1-10)",
        height=400
    )
    st.plotly_chart(fig_forces, use_container_width=True)

with tab4:
    st.header("📈 Recommandations Scouting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Arguments PRO")
        st.markdown("""
        **🔥 Profil Unique**
        - Dribbleur dans le top 1% européen
        - Progression balle au pied exceptionnelle
        - Créativité offensive confirmée
        
        **🎯 Adéquation Système Barcelone**
        - Jeu de position et mouvement
        - Capacité à jouer dans les espaces restreints
        - Intelligence tactique développée
        
        **💪 Potentiel de Développement**
        - Âge idéal (22 ans)
        - Marge de progression en finition
        - Adaptabilité démontrée
        
        **🏆 Impact Immédiat**
        - Solution au flanc gauche
        - Complément parfait à Lamine Yamal
        - Danger permanent en 1v1
        """)
    
    with col2:
        st.subheader("⚠️ Points d'Attention")
        st.markdown("""
        **📊 Efficacité Devant le But**
        - xG légèrement en dessous (38e percentile)
        - Marge d'amélioration en finition
        - Travail spécifique nécessaire
        
        **🎯 Création Pure**
        - xAG perfectible (38e percentile)
        - Développement de la passe décisive
        - Synchronisation avec les attaquants
        
        **⚡ Adaptabilité**
        - Transition Athletic Bilbao → Barcelone
        - Niveau de pression différent
        - Intégration système de jeu
        """)
    
    # Score global recommandation
    st.subheader("🎯 Score de Recommandation")
    
    # Calcul du score basé sur les percentiles clés
    percentiles_cles = df[df['Statistic'].isin([
        'Take-Ons Attempted', 'Progressive Carries', 'Shot-Creating Actions',
        'Progressive Passes Rec', 'Successful Take-Ons'
    ])]['Percentile'].mean()
    
    score_final = min(percentiles_cles, 95)  # Cap à 95 pour rester réaliste
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score Technique", f"{score_final:.1f}/100", "⭐ Excellent")
    
    with col2:
        st.metric("Adéquation Barça", "85/100", "✅ Très Bonne")
    
    with col3:
        st.metric("Recommandation", "FORTE", "🔥 Priorité Mercato")
    
    # Graphique final de synthèse
    fig_final = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score_final,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score Global Nico Williams"},
        delta = {'reference': 70, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#DC143C"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "yellow"},
                {'range': [70, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_final.update_layout(height=400)
    st.plotly_chart(fig_final, use_container_width=True)
    
    # Conclusion
    st.markdown("""
    ---
    ### 🎯 Conclusion Scouting
    
    **Nico Williams représente une opportunité exceptionnelle pour le FC Barcelone au poste d'ailier gauche.**
    
    Ses statistiques placent dans le top européen pour les qualités essentielles d'un ailier moderne :
    - **Dribble et élimination** (99e percentile)
    - **Progression balle au pied** (94e percentile) 
    - **Création d'occasions** (89e percentile)
    
    **Recommandation : PRIORITÉ ABSOLUE** pour le mercato estival.
    """)

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;">
    📊 Scouting Report basé sur les données de performance par 90 minutes<br>
    🔍 Percentiles calculés vs ailiers des 5 grands championnats européens
</div>
""", unsafe_allow_html=True)
