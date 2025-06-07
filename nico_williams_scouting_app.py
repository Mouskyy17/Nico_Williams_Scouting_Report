import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
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

# CSS personnalisé pour Barcelone
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #004D98 0%, #A50044 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: linear-gradient(135deg, #004D98 0%, #A50044 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .strength-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .improvement-card {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .barca-colors {
        background: linear-gradient(90deg, #004D98 0%, #A50044 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def load_data():
    try:
        # Lire le fichier CSV uploadé par l'utilisateur
        data = pd.read_csv('nico_williams_stats.csv')
        
        # Nettoyer les noms de colonnes
        data.columns = data.columns.str.strip()
        
        # Créer un dictionnaire des statistiques
        stats_dict = {}
        for index, row in data.iterrows():
            stat_name = row['Statistic']
            per_90 = row['Per 90']
            percentile = row['Percentile']
            stats_dict[stat_name] = {'per_90': per_90, 'percentile': percentile}
        
        return stats_dict
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return {}

# Fonction pour créer un graphique radar
def create_radar_chart(categories, values, title, color_scheme="Barca"):
    fig = go.Figure()
    
    colors = {
        "Barca": ["#004D98", "#A50044"],
        "Green": ["#28a745", "#20c997"],
        "Orange": ["#ffc107", "#fd7e14"]
    }
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=title,
        line=dict(color=colors[color_scheme][0], width=3),
        fillcolor=f"rgba({int(colors[color_scheme][0][1:3], 16)}, {int(colors[color_scheme][0][3:5], 16)}, {int(colors[color_scheme][0][5:7], 16)}, 0.3)"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20,
                gridcolor="lightgray"
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="#333")
            )
        ),
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=16, color="#333")
        ),
        showlegend=False,
        height=400
    )
    
    return fig

# Fonction pour créer un graphique de comparaison
def create_comparison_chart(stats_dict, categories, title):
    values = [stats_dict.get(cat, {'percentile': 0})['percentile'] for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=['#28a745' if v >= 70 else '#ffc107' if v >= 40 else '#dc3545' for v in values],
            text=[f"{v}%" for v in values],
            textposition='auto',
        )
    ])
    
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Médiane")
    fig.add_hline(y=75, line_dash="dash", line_color="green", annotation_text="Excellent (75%)")
    
    fig.update_layout(
        title=title,
        xaxis_title="Statistiques",
        yaxis_title="Percentile",
        yaxis=dict(range=[0, 100]),
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

# Fonction pour créer le terrain avec position
def create_pitch_position():
    fig, ax = plt.subplots(figsize=(10, 6))
    pitch = Pitch(pitch_color='#2d5a3d', line_color='white', linewidth=2)
    pitch.draw(ax=ax)
    
    # Position d'ailier gauche
    x_pos, y_pos = 25, 80  # Position approximative d'ailier gauche
    
    # Ajouter le joueur
    ax.scatter(x_pos, y_pos, s=500, color='#A50044', edgecolor='#004D98', linewidth=3, zorder=10)
    ax.text(x_pos, y_pos-8, 'NICO WILLIAMS\nAilier Gauche', 
            ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    
    # Zone d'influence
    circle = plt.Circle((x_pos, y_pos), 15, color='#A50044', alpha=0.3)
    ax.add_patch(circle)
    
    ax.set_title('Position et Zone d\'Influence sur le Terrain', 
                fontsize=16, color='white', pad=20, fontweight='bold')
    
    return fig

# Interface principale
def main():
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🔴🔵 NICO WILLIAMS - SCOUTING REPORT</h1>
        <h2>FC BARCELONE | AILIER GAUCHE | MERCATO 2025</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    stats_dict = load_data()
    
    if not stats_dict:
        st.error("Impossible de charger les données. Veuillez vérifier le fichier CSV.")
        return
    
    # Sidebar avec informations personnelles
    with st.sidebar:
        st.markdown("### 📋 INFORMATIONS PERSONNELLES")
        
        # Photo du joueur (placeholder)
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <div style="width: 200px; height: 200px; background: linear-gradient(135deg, #004D98, #A50044); 
                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 24px; font-weight: bold;">NICO<br>WILLIAMS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Nom Complet:** Nico Williams Arthuer  
        **Âge:** 22 ans (28/07/2002)  
        **Nationalité:** 🇪🇸 Espagne  
        **Club Actuel:** Athletic Bilbao  
        **Position:** Ailier Gauche  
        **Pied Fort:** Droit  
        **Taille:** 1m81  
        **Poids:** 70 kg  
        **Valeur Marchande:** ~60M€  
        
        ---
        
        **🏆 PALMARÈS**
        - Euro 2024 : 🏆 Vainqueur
        - Nations League 2023 : 🏆 Vainqueur
        - Coupe du Roi 2024 : 🏆 Vainqueur
        """)
    
    # Métriques principales
    st.markdown("## 📊 MÉTRIQUES CLÉS POUR BARCELONE")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        goals_assists = stats_dict.get('Goals + Assists', {'per_90': 0, 'percentile': 0})
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚽ BUTS + PASSES</h3>
            <h2>{goals_assists['per_90']}</h2>
            <p>Par 90 min | {goals_assists['percentile']}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        take_ons = stats_dict.get('Successful Take-Ons', {'per_90': 0, 'percentile': 0})
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏃 DRIBBLES RÉUSSIS</h3>
            <h2>{take_ons['per_90']}</h2>
            <p>Par 90 min | {take_ons['percentile']}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        prog_carries = stats_dict.get('Progressive Carries', {'per_90': 0, 'percentile': 0})
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 PORTÉES PROGRESSIVES</h3>
            <h2>{prog_carries['per_90']}</h2>
            <p>Par 90 min | {prog_carries['percentile']}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sca = stats_dict.get('Shot-Creating Actions', {'per_90': 0, 'percentile': 0})
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 ACTIONS CRÉATRICES</h3>
            <h2>{sca['per_90']}</h2>
            <p>Par 90 min | {sca['percentile']}e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌟 PROFIL OFFENSIF - PARFAIT POUR LE BARÇA")
        
        offensive_categories = [
            'Take-Ons Attempted', 'Successful Take-Ons', 'Progressive Carries',
            'Shot-Creating Actions', 'Goal-Creating Actions', 'Carries into Penalty Area',
            'Progressive Passes Rec', 'Crosses'
        ]
        
        offensive_values = [stats_dict.get(cat, {'percentile': 0})['percentile'] for cat in offensive_categories]
        
        fig_offensive = create_radar_chart(
            [cat.replace(' ', '\n') for cat in offensive_categories],
            offensive_values,
            "Profil Offensif - Élite Mondiale",
            "Green"
        )
        
        st.plotly_chart(fig_offensive, use_container_width=True)
    
    with col2:
        st.markdown("### ⚖️ PROFIL DÉFENSIF - ZONE D'AMÉLIORATION")
        
        defensive_categories = [
            'Tackles', 'Tackles Won', 'Interceptions', 'Blocks',
            'Clearances', 'Ball Recoveries', 'Fouls Committed', 'Aerials Won'
        ]
        
        defensive_values = [stats_dict.get(cat, {'percentile': 0})['percentile'] for cat in defensive_categories]
        
        fig_defensive = create_radar_chart(
            [cat.replace(' ', '\n') for cat in defensive_categories],
            defensive_values,
            "Profil Défensif - Amélioration Nécessaire",
            "Orange"
        )
        
        st.plotly_chart(fig_defensive, use_container_width=True)
    
    # Analyse détaillée
    st.markdown("## 🔍 ANALYSE DÉTAILLÉE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="strength-card">
            <h3>✅ POINTS FORTS POUR BARCELONE</h3>
            <ul>
                <li><strong>Dribbles Elite (98e percentile)</strong> - Capacité unique à éliminer les défenseurs</li>
                <li><strong>Progression Balle au Pied (94e percentile)</strong> - Parfait pour le jeu de transition</li>
                <li><strong>Création d'Occasions (89e percentile)</strong> - Génère du danger constant</li>
                <li><strong>Pénétration Surface (89e percentile)</strong> - Menace directe sur le but</li>
                <li><strong>Centres de Qualité (84e percentile)</strong> - Service précis pour les attaquants</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="improvement-card">
            <h3>⚠️ ZONES D'AMÉLIORATION</h3>
            <ul>
                <li><strong>Passes Courtes (27e percentile)</strong> - Développement nécessaire pour le jeu Barça</li>
                <li><strong>Efficacité Technique</strong> - Réduire les pertes de balle (14e percentile)</li>
                <li><strong>Engagement Défensif (31e percentile)</strong> - Pressing et récupération</li>
                <li><strong>Jeu Collectif</strong> - Améliorer la connexion avec les coéquipiers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Position sur le terrain
    st.markdown("## 🏟️ POSITION ET ZONE D'INFLUENCE")
    
    fig_pitch = create_pitch_position()
    st.pyplot(fig_pitch, use_container_width=True)
    
    # Comparaisons avec d'autres ailiers
    st.markdown("## 📈 COMPARAISON AVEC LES MEILLEURS AILIERS")
    
    elite_stats = [
        'Take-Ons Attempted', 'Successful Take-Ons', 'Progressive Carries',
        'Shot-Creating Actions', 'Carries into Penalty Area', 'Goals + Assists'
    ]
    
    fig_comparison = create_comparison_chart(stats_dict, elite_stats, "Nico Williams vs Élite Mondiale")
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Conclusion
    st.markdown("## 🎯 CONCLUSION : POURQUOI NICO WILLIAMS POUR BARCELONE ?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔥 PROFIL PARFAIT
        - **Dribbleur d'élite mondiale** (Top 2%)
        - **Créateur de danger constant**
        - **Jeune et évolutif** (22 ans)
        - **Expérience internationale**
        """)
    
    with col2:
        st.markdown("""
        ### 🎪 STYLE BARCELONE
        - **Technique individuelle exceptionnelle**
        - **Progression rapide vers l'avant**
        - **Création d'espaces pour les autres**
        - **Menace constante sur le flanc**
        """)
    
    with col3:
        st.markdown("""
        ### 💰 VALEUR MARCHÉ
        - **Âge optimal** pour investissement
        - **Potentiel de revente élevé**
        - **Impact immédiat possible**
        - **Complément parfait à Lamine Yamal**
        """)
    
    # Recommandation finale
    st.markdown("""
    <div style="background: linear-gradient(135deg, #004D98, #A50044); padding: 30px; border-radius: 15px; color: white; text-align: center; margin: 30px 0;">
        <h2>🏆 RECOMMANDATION FINALE</h2>
        <h3>NICO WILLIAMS représente le profil IDEAL pour renforcer l'aile gauche de Barcelone</h3>
        <p style="font-size: 18px; margin: 20px 0;">
            Ses qualités techniques exceptionnelles, sa jeunesse et son potentiel d'évolution 
            en font un investissement stratégique parfait pour l'avenir du club.
        </p>
        <h2 style="color: #FFD700;">⭐ PRIORITÉ ABSOLUE MERCATO 2025 ⭐</h2>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
