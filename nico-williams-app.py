import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Nico Williams - Scouting Report",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le style Barça
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #A50044 0%, #004D98 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #A50044;
        margin: 10px 0;
    }
    .strength-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .barca-colors {
        background: linear-gradient(90deg, #A50044 0%, #004D98 100%);
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    # Lecture du fichier CSV
    df = pd.read_csv('nico_williams_stats.csv')
    
    # Nettoyage des données
    df['Statistic'] = df['Statistic'].str.strip()
    df['Per 90'] = pd.to_numeric(df['Per 90'], errors='coerce')
    df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')
    
    return df

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔴🔵 NICO WILLIAMS - SCOUTING REPORT FC BARCELONA</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar avec informations personnelles
with st.sidebar:
    st.markdown("## 📋 Informations Personnelles")
    
    # Photo du joueur (placeholder)
    st.image("https://via.placeholder.com/300x400/A50044/FFFFFF?text=NICO+WILLIAMS", 
             caption="Nico Williams", use_column_width=True)
    
    st.markdown("""
    **Nom Complet:** Nicolás Williams Arthuer  
    **Âge:** 22 ans (né le 12 juillet 2002)  
    **Nationalité:** 🇪🇸 Espagne  
    **Position:** Ailier Gauche/Droit  
    **Club Actuel:** Athletic Bilbao  
    **Pied Fort:** Droit  
    **Taille:** 1m81  
    **Valeur Marchande:** ~60M€  
    
    ---
    
    ### 🎯 Profil Idéal pour le Barça
    ✅ Vitesse exceptionnelle  
    ✅ Dribbles élite  
    ✅ Créativité offensive  
    ✅ Jeune et en progression  
    ✅ Expérience en Liga  
    """)

# Chargement des données
try:
    df = load_data()
    
    # Métriques clés pour Barcelone
    col1, col2, col3, col4 = st.columns(4)
    
    # Fonction pour obtenir les valeurs
    def get_stat_value(stat_name):
        mask = df['Statistic'].str.contains(stat_name, case=False, na=False)
        if mask.any():
            return df[mask]['Per 90'].iloc[0], df[mask]['Percentile'].iloc[0]
        return 0, 0
    
    with col1:
        goals_val, goals_perc = get_stat_value('Goals')
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚽ Buts</h3>
            <h2>{goals_val}</h2>
            <p>Par 90 min | {goals_perc}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        assists_val, assists_perc = get_stat_value('Assists')
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Passes Décisives</h3>
            <h2>{assists_val}</h2>
            <p>Par 90 min | {assists_perc}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        takeOns_val, takeOns_perc = get_stat_value('Take-Ons Attempted')
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏃 Dribbles Tentés</h3>
            <h2>{takeOns_val}</h2>
            <p>Par 90 min | {takeOns_perc}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        carries_val, carries_perc = get_stat_value('Progressive Carries')
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Courses Progressives</h3>
            <h2>{carries_val}</h2>
            <p>Par 90 min | {carries_perc}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Section principale avec onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Analyse Offensive", "📊 Radar Chart", "⚽ Position sur Terrain", "📈 Métriques Avancées"])
    
    with tab1:
        st.markdown("## 🔥 Points Forts Offensifs - Profil Barcelone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="strength-card">
                <h3>🏃‍♂️ VITESSE ET DRIBBLES (ÉLITE)</h3>
                <p><strong>99e percentile</strong> en tentatives de dribbles (8.62/90)</p>
                <p><strong>98e percentile</strong> en dribbles réussis (3.43/90)</p>
                <p>Capable de déborder n'importe quel défenseur</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="strength-card">
                <h3>📈 PROGRESSION BALLE AU PIED</h3>
                <p><strong>94e percentile</strong> en courses progressives (5.69/90)</p>
                <p><strong>89e percentile</strong> en distance progressive (140.46m/90)</p>
                <p>Idéal pour sortir le ballon et créer du danger</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="strength-card">
                <h3>🎯 CRÉATION D'OCCASIONS</h3>
                <p><strong>89e percentile</strong> en actions créatrices de tirs (5.29/90)</p>
                <p><strong>79e percentile</strong> en passes clés (2.05/90)</p>
                <p>Capable de faire la différence dans les derniers mètres</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="strength-card">
                <h3>⚡ ACTIVITÉ EN SURFACE</h3>
                <p><strong>89e percentile</strong> en entrées dans la surface (2.51/90)</p>
                <p><strong>88e percentile</strong> en passes progressives reçues (11.07/90)</p>
                <p>Toujours disponible pour les dernières passes</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## 📊 Profil Radar - Aptitudes Offensives")
        
        # Sélection des métriques clés pour le radar
        radar_stats = [
            'Goals', 'Assists', 'Take-Ons Attempted', 'Successful Take-Ons',
            'Progressive Carries', 'Shot-Creating Actions', 'Key Passes',
            'Carries into Penalty Area', 'Crosses', 'Progressive Passes Rec'
        ]
        
        radar_data = []
        radar_labels = []
        
        for stat in radar_stats:
            mask = df['Statistic'].str.contains(stat, case=False, na=False)
            if mask.any():
                percentile = df[mask]['Percentile'].iloc[0]
                radar_data.append(percentile)
                radar_labels.append(stat.replace('_', ' ').title())
        
        # Création du radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=radar_data,
            theta=radar_labels,
            fill='toself',
            fillcolor='rgba(165, 0, 68, 0.3)',
            line=dict(color='#A50044', width=3),
            name='Nico Williams'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=['20%', '40%', '60%', '80%', '100%']
                )
            ),
            title="Radar des Performances Offensives (Percentiles)",
            title_x=0.5,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="barca-colors">
            <strong>💡 Analyse:</strong> Nico Williams excelle dans tous les domaines offensifs clés pour un ailier moderne. 
            Ses percentiles élevés en dribbles, courses progressives et création d'occasions en font un profil idéal 
            pour le système de jeu de Barcelone.
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("## ⚽ Position et Zone d'Influence")
        
        # Création du terrain avec mplsoccer
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Terrain
        pitch = Pitch(pitch_color='#2e7d32', line_color='white', linewidth=2)
        pitch.draw(ax=ax)
        
        # Zones d'activité principales (basées sur les stats)
        # Zone ailier gauche
        ax.add_patch(plt.Rectangle((0, 20), 30, 40, 
                                 fill=True, color='red', alpha=0.3, 
                                 label='Zone Principale'))
        
        # Zone de percussion vers le but
        ax.add_patch(plt.Rectangle((70, 25), 25, 30, 
                                 fill=True, color='yellow', alpha=0.4, 
                                 label='Zone de Finition'))
        
        # Trajectoires de course
        ax.arrow(10, 40, 60, 0, head_width=2, head_length=3, 
                fc='white', ec='white', linewidth=3, alpha=0.8)
        ax.arrow(15, 35, 50, 15, head_width=2, head_length=3, 
                fc='white', ec='white', linewidth=3, alpha=0.8)
        
        # Position du joueur
        ax.scatter(15, 40, s=500, c='#A50044', marker='o', 
                  edgecolors='white', linewidth=3, zorder=5)
        ax.text(15, 35, 'NICO\nWILLIAMS', ha='center', va='top', 
               fontsize=10, fontweight='bold', color='white')
        
        ax.set_title('Position et Zones d\'Influence de Nico Williams', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right')
        
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔴 Zone Rouge:** Position principale ailier gauche
            - Réception des ballons de construction
            - Début des actions offensives
            - 85e percentile en touches en zone offensive
            """)
        
        with col2:
            st.markdown("""
            **🟡 Zone Jaune:** Zone de finition
            - 89e percentile entrées en surface
            - 2.51 entrées/90 min
            - Zone de danger maximum
            """)
    
    with tab4:
        st.markdown("## 📈 Métriques Avancées et Comparaisons")
        
        # Graphique des métriques offensives clés
        offensive_metrics = df[df['Statistic'].isin([
            'Goals', 'Assists', 'Shot-Creating Actions', 'Key Passes',
            'Take-Ons Attempted', 'Progressive Carries', 'Crosses'
        ])].copy()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Contribution Offensive', 'Créativité', 'Dribbles et Courses', 'Activité Offensive'),
            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                   [{"secondary_y": True}, {"secondary_y": True}]]
        )
        
        # Graphique 1: Buts + Passes décisives
        goals_assists = df[df['Statistic'].isin(['Goals', 'Assists'])]
        fig.add_trace(
            go.Bar(x=goals_assists['Statistic'], y=goals_assists['Per 90'], 
                   name='Par 90 min', marker_color='#A50044'),
            row=1, col=1
        )
        
        # Graphique 2: Création
        creation = df[df['Statistic'].isin(['Shot-Creating Actions', 'Key Passes'])]
        fig.add_trace(
            go.Bar(x=creation['Statistic'], y=creation['Per 90'], 
                   name='Création', marker_color='#004D98'),
            row=1, col=2
        )
        
        # Graphique 3: Dribbles
        dribbles = df[df['Statistic'].isin(['Take-Ons Attempted', 'Progressive Carries'])]
        fig.add_trace(
            go.Bar(x=dribbles['Statistic'], y=dribbles['Per 90'], 
                   name='Progression', marker_color='#28a745'),
            row=2, col=1
        )
        
        # Graphique 4: Activité
        activity = df[df['Statistic'].isin(['Crosses', 'Touches (Att 3rd)'])]
        if not activity.empty:
            fig.add_trace(
                go.Bar(x=activity['Statistic'], y=activity['Per 90'], 
                       name='Activité', marker_color='#ffc107'),
                row=2, col=2
            )
        
        fig.update_layout(height=600, showlegend=False, 
                         title_text="Profil Offensif Complet de Nico Williams")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau de comparaison avec les standards Barça
        st.markdown("### 🎯 Adéquation avec le Profil Barcelone")
        
        comparison_data = {
            'Critère': [
                'Vitesse/Dribbles', 'Créativité', 'Progression', 
                'Activité Offensive', 'Jeunesse', 'Expérience Liga'
            ],
            'Importance Barça': ['Très Haute', 'Très Haute', 'Haute', 'Haute', 'Moyenne', 'Haute'],
            'Niveau Nico': ['Élite (99%)', 'Très Bon (79%)', 'Élite (94%)', 'Très Bon (85%)', 'Parfait (22 ans)', 'Excellente'],
            'Score': ['10/10', '8/10', '10/10', '8/10', '9/10', '9/10']
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Score final
        st.markdown("""
        <div class="barca-colors">
            <h2 style="text-align: center; margin: 0;">
                🎯 SCORE FINAL D'ADÉQUATION: 9.0/10
            </h2>
            <p style="text-align: center; margin: 10px 0 0 0;">
                <strong>RECOMMANDATION: CIBLE PRIORITAIRE POUR LE MERCATO</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.info("Assurez-vous que le fichier 'nico_williams_stats.csv' est présent dans le répertoire.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>📊 Scouting Report généré pour FC Barcelona | Données saison 2023-24</p>
    <p>🔴🔵 <strong>Visca el Barça!</strong></p>
</div>
""", unsafe_allow_html=True)