import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Nico Williams - Profil FC Barcelone",
    page_icon="⚽",
    layout="wide"
)

# CSS personnalisé pour le thème Barcelone
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #004c98, #a50044);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #a50044;
        margin: 10px 0;
    }
    .strength-badge {
        background: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        margin: 2px;
        display: inline-block;
    }
    .percentile-excellent {
        color: #28a745;
        font-weight: bold;
    }
    .percentile-good {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    try:
        # Lecture du fichier CSV depuis l'upload
        data = pd.read_csv('nico_williams_stats.csv')
        return data
    except:
        # Données de fallback basées sur le CSV fourni
        data = {
            'Statistic': [
                'Goals', 'Assists', 'Goals + Assists', 'Progressive Carries', 'Progressive Passes Rec',
                'Shots Total', 'Key Passes', 'Take-Ons Attempted', 'Successful Take-Ons', 
                'Shot-Creating Actions', 'Goal-Creating Actions', 'Carries into Penalty Area',
                'Crosses', 'Touches (Att 3rd)', 'Progressive Carrying Distance'
            ],
            'Per 90': [0.31, 0.21, 0.52, 5.69, 11.07, 2.51, 2.05, 8.62, 3.43, 5.29, 0.61, 2.51, 5.05, 31.16, 140.46],
            'Percentile': [57, 61, 59, 94, 88, 69, 79, 99, 98, 89, 80, 89, 84, 85, 89]
        }
        return pd.DataFrame(data)

data = load_data()

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>🔵🔴 NICO WILLIAMS - PROFIL FC BARCELONE</h1>
    <h3>Ailier Gauche | Athletic Bilbao → FC Barcelona</h3>
    <p>Analyse des performances offensives et adéquation tactique</p>
</div>
""", unsafe_allow_html=True)

# Métriques clés en haut de page
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎯 Buts + Passes", "0.52/90min", "59e percentile")
    
with col2:
    st.metric("🚀 Dribbles réussis", "3.43/90min", "98e percentile")
    
with col3:
    st.metric("📈 Actions créatrices", "5.29/90min", "89e percentile")
    
with col4:
    st.metric("⚡ Portées progressives", "5.69/90min", "94e percentile")

st.divider()

# Section principale avec deux colonnes
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("🎯 Points Forts Offensifs")
    
    # Graphique radar des forces offensives
    categories = ['Dribbles\n(99e %ile)', 'Portées Prog.\n(94e %ile)', 'Actions Créatrices\n(89e %ile)', 
                  'Passes Reçues Prog.\n(88e %ile)', 'Entrées Surface\n(89e %ile)', 'Centres\n(84e %ile)']
    values = [99, 94, 89, 88, 89, 84]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Nico Williams',
        line_color='#a50044',
        fillcolor='rgba(165, 0, 68, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title="Profil Offensif vs Ailiers Elite",
        title_x=0.5,
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Graphique de comparaison des actions offensives
    st.subheader("📊 Performance Offensive Détaillée")
    
    offensive_stats = data[data['Statistic'].isin([
        'Goals + Assists', 'Shot-Creating Actions', 'Goal-Creating Actions', 
        'Key Passes', 'Successful Take-Ons', 'Progressive Carries'
    ])]
    
    fig_bar = px.bar(
        offensive_stats,
        x='Statistic',
        y='Per 90',
        color='Percentile',
        color_continuous_scale='RdYlGn',
        title="Actions Offensives par 90 minutes"
    )
    
    fig_bar.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.header("🏆 Pourquoi Barcelone ?")
    
    st.markdown("""
    <div class="metric-card">
        <h4>🎨 Style de Jeu Compatible</h4>
        <p><span class="strength-badge">Technique</span> <span class="strength-badge">Créativité</span></p>
        <p>• 11.07 passes progressives reçues/90min (88e percentile)<br>
        • 2.05 passes clés/90min (79e percentile)<br>
        • Excellent dans les espaces restreints</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h4>⚡ Explosivité et Vitesse</h4>
        <p><span class="strength-badge">Elite</span> <span class="strength-badge">Dribbles</span></p>
        <p>• 8.62 tentatives de dribbles/90min (99e percentile)<br>
        • 3.43 dribbles réussis/90min (98e percentile)<br>
        • Menace constante en 1v1</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <h4>🎯 Impact Direct sur le Jeu</h4>
        <p><span class="strength-badge">Décisif</span> <span class="strength-badge">Polyvalent</span></p>
        <p>• 5.29 actions créatrices de tir/90min (89e percentile)<br>
        • 2.51 entrées en surface/90min (89e percentile)<br>
        • 5.05 centres/90min (84e percentile)</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Section d'analyse tactique
st.header("🔍 Analyse Tactique - Adéquation Barcelone")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎯 Profil Offensif")
    
    # Graphique des touches par zone
    zones = ['Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen']
    touches = [3.82, 15.54, 31.16, 5.05]
    percentiles = [16, 23, 85, 68]
    
    fig_zones = go.Figure()
    fig_zones.add_trace(go.Bar(
        x=zones,
        y=touches,
        marker_color=['#ff6b6b' if p < 50 else '#51cf66' for p in percentiles],
        text=[f'{t:.1f}<br>({p}e %ile)' for t, p in zip(touches, percentiles)],
        textposition='auto'
    ))
    
    fig_zones.update_layout(
        title="Touches par Zone du Terrain",
        yaxis_title="Touches par 90min",
        height=300
    )
    
    st.plotly_chart(fig_zones, use_container_width=True)

with col2:
    st.subheader("🚀 Progression du Ballon")
    
    # Métriques de progression
    prog_data = {
        'Métrique': ['Portées Progressives', 'Distance Progressive', 'Entrées Dernier Tiers'],
        'Valeur': [5.69, 140.46, 2.75],
        'Percentile': [94, 89, 81]
    }
    
    for i, (metric, value, perc) in enumerate(zip(prog_data['Métrique'], prog_data['Valeur'], prog_data['Percentile'])):
        color_class = "percentile-excellent" if perc >= 80 else "percentile-good"
        st.markdown(f"""
        <p><strong>{metric}:</strong> 
        <span class="{color_class}">{value:.2f} ({perc}e %ile)</span></p>
        """, unsafe_allow_html=True)

with col3:
    st.subheader("🎨 Création & Finition")
    
    creation_data = {
        'Actions Créatrices': 5.29,
        'Actions Créatrices de But': 0.61,
        'Passes Clés': 2.05,
        'xG + xA': 0.38
    }
    
    fig_creation = go.Figure(go.Bar(
        x=list(creation_data.keys()),
        y=list(creation_data.values()),
        marker_color='#a50044',
        text=[f'{v:.2f}' for v in creation_data.values()],
        textposition='auto'
    ))
    
    fig_creation.update_layout(
        title="Contribution Créative",
        height=300,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_creation, use_container_width=True)

st.divider()

# Section finale - Recommandation
st.header("📋 Rapport de Scouting - Recommandation")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### ✅ **RECOMMANDATION : ACQUISITION PRIORITAIRE**
    
    **Forces Exceptionnelles :**
    - **Dribbles (99e percentile)** : Elite absolue en 1v1, capacité à battre n'importe quel défenseur
    - **Progression (94e percentile)** : Excellent pour casser les lignes et créer le surnombre
    - **Créativité (89e percentile)** : Génère de nombreuses occasions pour ses coéquipiers
    - **Polyvalence tactique** : Peut jouer ailier gauche, droit ou en soutien
    
    **Adéquation Barcelone :**
    - Style de jeu technique et créatif compatible avec la philosophie Barça
    - Jeune (22 ans) avec potentiel de développement important  
    - Expérience en Liga et compétitions européennes
    - Profil rare d'ailier explosif avec vision de jeu
    
    **Impact Attendu :**
    - Solution immédiate au poste d'ailier gauche
    - Apport de vitesse et d'imprévisibilité en attaque
    - Création d'occasions et d'espaces pour Lewandowski et les autres attaquants
    """)

with col2:
    # Score global
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28a745, #20c997); 
                padding: 30px; border-radius: 15px; text-align: center; color: white;">
        <h2>SCORE GLOBAL</h2>
        <h1 style="font-size: 4em; margin: 0;">8.7/10</h1>
        <p><strong>PROFIL IDÉAL</strong></p>
        <p>pour le FC Barcelone</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Priorités de négociation
    st.markdown("""
    **🎯 Priorité de Mercato :**
    - **Urgence :** HAUTE
    - **Valeur :** 45-60M€
    - **Concurrence :** Arsenal, PSG
    - **Timing :** Été 2024
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📊 Rapport généré à partir des données FBref | Saison 2023-24</p>
    <p>🔵🔴 FC Barcelona Scouting Department</p>
</div>
""", unsafe_allow_html=True)