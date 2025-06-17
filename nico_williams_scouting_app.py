import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import io
import base64

# Configuration de la page
st.set_page_config(
    page_title="Scouting Report - Nico Williams",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le design Barcelone
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #004d98 0%, #a50044 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
        border-radius: 10px;
    }
    .player-card {
        background: linear-gradient(135deg, #004d98 0%, #a50044 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #004d98;
        margin: 0.5rem 0;
    }
    .strength-card {
        background: linear-gradient(135deg, #00a650 0%, #007d3c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .weakness-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .barca-colors {
        background: linear-gradient(45deg, #004d98, #a50044);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Données de Nico Williams (extraites du CSV)
nico_stats = {
    'Goals': 0.31, 'Assists': 0.21, 'Goals + Assists': 0.52,
    'Non-Penalty Goals': 0.31, 'xG: Expected Goals': 0.21, 'npxG: Non-Penalty xG': 0.21,
    'xAG: Exp. Assisted Goals': 0.17, 'Progressive Carries': 5.69,
    'Progressive Passes': 3.09, 'Progressive Passes Rec': 11.07,
    'Shots Total': 2.51, 'Shots on Target': 0.92, 'Goals/Shot': 0.12,
    'Average Shot Distance': 16.6, 'Passes Completed': 23.12,
    'Passes Attempted': 33.0, 'Key Passes': 2.05, 'Crosses': 5.05,
    'Shot-Creating Actions': 5.29, 'Goal-Creating Actions': 0.61,
    'Take-Ons Attempted': 8.62, 'Successful Take-Ons': 3.43,
    'Times Tackled During Take-On': 4.53, 'Carries': 31.99,
    'Total Carrying Distance': 258.5, 'Progressive Carrying Distance': 140.46,
    'Carries into Final Third': 2.75, 'Carries into Penalty Area': 2.51,
    'Tackles': 1.07, 'Tackles Won': 0.67, 'Interceptions': 0.37,
    'Fouls Drawn': 1.53, 'Yellow Cards': 0.06, 'Ball Recoveries': 4.4
}

# Percentiles correspondants
percentiles = {
    'Goals': 57, 'Assists': 61, 'Goals + Assists': 59,
    'Non-Penalty Goals': 64, 'xG: Expected Goals': 38, 'npxG: Non-Penalty xG': 43,
    'xAG: Exp. Assisted Goals': 38, 'Progressive Carries': 94,
    'Progressive Passes': 34, 'Progressive Passes Rec': 88,
    'Shots Total': 69, 'Shots on Target': 60, 'Goals/Shot': 52,
    'Average Shot Distance': 64, 'Passes Completed': 27,
    'Passes Attempted': 32, 'Key Passes': 79, 'Crosses': 84,
    'Shot-Creating Actions': 89, 'Goal-Creating Actions': 80,
    'Take-Ons Attempted': 99, 'Successful Take-Ons': 98,
    'Times Tackled During Take-On': 1, 'Carries': 59,
    'Total Carrying Distance': 88, 'Progressive Carrying Distance': 89,
    'Carries into Final Third': 81, 'Carries into Penalty Area': 89,
    'Tackles': 31, 'Tackles Won': 36, 'Interceptions': 36,
    'Fouls Drawn': 56, 'Yellow Cards': 84, 'Ball Recoveries': 66
}

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔴🔵 SCOUTING REPORT - NICO WILLIAMS</h1>
    <h2>Le Profil Idéal pour l'Aile Gauche du FC Barcelone</h2>
</div>
""", unsafe_allow_html=True)

# Sidebar avec informations personnelles
with st.sidebar:
    st.markdown("""
    <div class="player-card">
        <h2>📋 FICHE JOUEUR</h2>
        <hr style="border-color: white;">
        <p><strong>Nom:</strong> Nicholas Williams Arthuer</p>
        <p><strong>Âge:</strong> 22 ans (né le 12/07/2002)</p>
        <p><strong>Nationalité:</strong> 🇪🇸 Espagnol</p>
        <p><strong>Club actuel:</strong> Athletic Bilbao</p>
        <p><strong>Position:</strong> Ailier gauche/droit</p>
        <p><strong>Taille:</strong> 181 cm</p>
        <p><strong>Poids:</strong> 69 kg</p>
        <p><strong>Pied fort:</strong> Droit</p>
        <p><strong>Valeur marchande:</strong> 70M€</p>
        <p><strong>Sélections:</strong> Espagne A</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏆 Palmarès récent:")
    st.write("• Champion d'Europe 2024 avec l'Espagne")
    st.write("• Finaliste Coupe du Roi 2024")
    st.write("• International espagnol depuis 2022")

# Layout principal avec onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Vue d'ensemble", "💪 Forces Offensives", "🛡️ Aspects Défensifs", "📊 Métriques Avancées", "⚽ Position sur Terrain"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #004d98; margin: 0;">⚽ BUTS + PASSES</h3>
            <h2 style="margin: 5px 0;">0.52 /90min</h2>
            <p style="margin: 0; color: #666;">59e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #004d98; margin: 0;">🎭 DRIBBLES</h3>
            <h2 style="margin: 5px 0;">8.62 tentatives</h2>
            <p style="margin: 0; color: #666;">99e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #004d98; margin: 0;">🚀 ACTIONS CRÉATIVES</h3>
            <h2 style="margin: 5px 0;">5.29 /90min</h2>
            <p style="margin: 0; color: #666;">89e percentile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #004d98; margin: 0;">📈 PROGRESSION</h3>
            <h2 style="margin: 5px 0;">5.69 courses</h2>
            <p style="margin: 0; color: #666;">94e percentile</p>
        </div>
        """, unsafe_allow_html=True)

    # Radar Chart Principal
    st.subheader("🕷️ Profil Radar - Comparaison avec les Ailiers Elite")
    
    categories = ['Dribbles', 'Actions Créatives', 'Progression', 'Centres', 'Tirs', 'Passes Clés']
    values_nico = [99, 89, 94, 84, 69, 79]
    values_avg = [50, 50, 50, 50, 50, 50]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_nico,
        theta=categories,
        fill='toself',
        name='Nico Williams',
        line_color='#004d98',
        fillcolor='rgba(0, 77, 152, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values_avg,
        theta=categories,
        fill='toself',
        name='Moyenne des Ailiers',
        line_color='#a50044',
        fillcolor='rgba(165, 0, 68, 0.1)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Comparaison Percentiles - Nico Williams vs Moyenne",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💪 Forces Offensives - Pourquoi il est parfait pour Barcelone")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="strength-card">
            <h3>🎭 DRIBBLES D'ÉLITE MONDIALE</h3>
            <ul>
                <li><strong>8.62 tentatives/90min (99e percentile)</strong></li>
                <li><strong>3.43 réussites/90min (98e percentile)</strong></li>
                <li>Taux de réussite: 40% - Excellent pour un ailier</li>
                <li>Capable de déséquilibrer n'importe quelle défense</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strength-card">
            <h3>🚀 PROGRESSION EXCEPTIONNELLE</h3>
            <ul>
                <li><strong>5.69 courses progressives/90min (94e percentile)</strong></li>
                <li><strong>2.51 courses en surface/90min (89e percentile)</strong></li>
                <li>140.46m de distance progressive par match</li>
                <li>Parfait pour le jeu de possession barcelonais</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strength-card">
            <h3>🎯 CRÉATION D'OCCASIONS</h3>
            <ul>
                <li><strong>5.29 actions créatives/90min (89e percentile)</strong></li>
                <li><strong>2.05 passes clés/90min (79e percentile)</strong></li>
                <li>0.61 actions créatrices de but/90min</li>
                <li>Impact direct sur les statistiques offensives</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strength-card">
            <h3>⚡ VITESSE ET CENTRES</h3>
            <ul>
                <li><strong>5.05 centres/90min (84e percentile)</strong></li>
                <li>Excellent dans les transitions rapides</li>
                <li>Capable de jouer sur les deux flancs</li>
                <li>Profil moderne recherché par Barcelone</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique des forces offensives
    st.subheader("📊 Comparaison des Forces Offensives")
    
    offensive_metrics = ['Take-Ons Attempted', 'Successful Take-Ons', 'Progressive Carries', 
                        'Shot-Creating Actions', 'Key Passes', 'Crosses']
    offensive_values = [8.62, 3.43, 5.69, 5.29, 2.05, 5.05]
    offensive_percentiles = [99, 98, 94, 89, 79, 84]
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Valeurs Absolues (par 90 minutes)', 'Percentiles vs autres ailiers'),
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Graphique des valeurs absolues
    fig.add_trace(
        go.Bar(x=offensive_metrics, y=offensive_values, 
               marker_color=['#004d98' if p >= 90 else '#a50044' if p >= 70 else '#FFA500' for p in offensive_percentiles],
               name="Valeurs"),
        row=1, col=1
    )
    
    # Graphique des percentiles
    fig.add_trace(
        go.Bar(x=offensive_metrics, y=offensive_percentiles,
               marker_color=['#00a650' if p >= 90 else '#FFA500' if p >= 70 else '#ff6b6b' for p in offensive_percentiles],
               name="Percentiles"),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🛡️ Aspects Défensifs - Zones d'Amélioration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="weakness-card">
            <h3>⚠️ ENGAGEMENT DÉFENSIF LIMITÉ</h3>
            <ul>
                <li>1.07 tacles/90min (31e percentile)</li>
                <li>0.37 interceptions/90min (36e percentile)</li>
                <li>Besoin d'améliorer le pressing défensif</li>
                <li>Adaptation nécessaire au système Barça</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="weakness-card">
            <h3>🔄 PERTES DE BALLE</h3>
            <ul>
                <li>4.53 dribbles subis/90min (1er percentile)</li>
                <li>2.02 dépossessions/90min (14e percentile)</li>
                <li>Ratio à améliorer pour le jeu de possession</li>
                <li>Formation tactique recommandée</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Graphique défensif
        defensive_metrics = ['Tackles', 'Interceptions', 'Ball Recoveries', 'Times Tackled During Take-On']
        defensive_values = [1.07, 0.37, 4.4, 4.53]
        defensive_percentiles = [31, 36, 66, 1]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=defensive_metrics,
            y=defensive_percentiles,
            marker_color=['#ff6b6b' if p < 40 else '#FFA500' if p < 70 else '#00a650' for p in defensive_percentiles],
            text=[f"{v:.2f}" for v in defensive_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Métriques Défensives (Percentiles)",
            yaxis_title="Percentile",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Recommandation:** Ces faiblesses défensives sont typiques d'un ailier offensif moderne et peuvent être compensées par le système tactique de Barcelone et un travail spécifique avec l'entraîneur.")

with tab4:
    st.subheader("📊 Métriques Avancées - Analyse Approfondie")
    
    # Métriques de création
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Goals - xG", "+0.09", "Surperforme ses Expected Goals")
        st.metric("📈 Progressive Passes Rec", "11.07", "88e percentile")
        st.metric("🏃 Carries into Final Third", "2.75", "81e percentile")
    
    with col2:
        st.metric("⚽ Goals + Assists", "0.52", "Production offensive solide")
        st.metric("🎭 Successful Take-Ons", "3.43", "98e percentile - Elite")
        st.metric("📊 Shot-Creating Actions", "5.29", "89e percentile")
    
    with col3:
        st.metric("🎯 Key Passes", "2.05", "79e percentile")
        st.metric("🚀 Progressive Carrying Distance", "140.46m", "89e percentile")
        st.metric("⚡ Total Carrying Distance", "258.5m", "88e percentile")
    
    # Graphique de comparaison avec les besoins de Barcelone
    st.subheader("🔄 Adéquation avec le Profil Barcelone")
    
    barca_needs = {
        'Dribbles': {'importance': 95, 'nico_level': 99, 'description': 'Essentiel pour déséquilibrer'},
        'Vitesse': {'importance': 90, 'nico_level': 95, 'description': 'Transitions rapides'},
        'Créativité': {'importance': 85, 'nico_level': 89, 'description': 'Création d\'occasions'},
        'Polyvalence': {'importance': 80, 'nico_level': 85, 'description': 'Joue sur les 2 flancs'},
        'Jeunesse': {'importance': 75, 'nico_level': 100, 'description': '22 ans - Potentiel énorme'},
        'Pressing': {'importance': 70, 'nico_level': 35, 'description': 'À développer'}
    }
    
    categories = list(barca_needs.keys())
    importance = [barca_needs[cat]['importance'] for cat in categories]
    nico_level = [barca_needs[cat]['nico_level'] for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=importance,
        theta=categories,
        fill='toself',
        name='Besoins Barcelone',
        line_color='#a50044',
        fillcolor='rgba(165, 0, 68, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=nico_level,
        theta=categories,
        fill='toself',
        name='Niveau Nico Williams',
        line_color='#004d98',
        fillcolor='rgba(0, 77, 152, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Adéquation Profil Nico Williams / Besoins FC Barcelona",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Score de compatibilité
    compatibility_score = np.mean([min(importance[i], nico_level[i]) for i in range(len(categories))])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #004d98, #a50044); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
        <h2>🎯 SCORE DE COMPATIBILITÉ BARCELONE</h2>
        <h1 style="font-size: 3rem; margin: 1rem 0;">{compatibility_score:.0f}/100</h1>
        <p style="font-size: 1.2rem;">Profil TRÈS COMPATIBLE avec les besoins du FC Barcelona</p>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.subheader("⚽ Position et Mouvements sur le Terrain")
    
    # Création du terrain avec mplsoccer
    fig, ax = plt.subplots(figsize=(12, 8))
    pitch = Pitch(pitch_color='#2d5a2d', line_color='white', linewidth=2)
    pitch.draw(ax=ax)
    
    # Position principale (ailier gauche)
    ax.scatter(20, 15, s=300, c='#004d98', marker='o', edgecolors='white', linewidth=2, label='Position Principale')
    ax.text(20, 12, 'NICO\nWILLIAMS', ha='center', va='top', color='white', fontsize=10, fontweight='bold')
    
    # Zones d'influence
    from matplotlib.patches import Ellipse
    
    # Zone principale d'action
    ellipse1 = Ellipse((25, 20), 30, 25, alpha=0.3, color='#004d98', label='Zone d\'influence principale')
    ax.add_patch(ellipse1)
    
    # Zone de repli défensif
    ellipse2 = Ellipse((15, 25), 20, 15, alpha=0.2, color='#a50044', label='Zone de repli défensif')
    ax.add_patch(ellipse2)
    
    # Mouvements offensifs typiques
    # Vers l'intérieur
    ax.arrow(20, 15, 15, 5, head_width=2, head_length=2, fc='yellow', ec='yellow', alpha=0.8)
    ax.text(28, 22, 'Rentrées\ndans l\'axe', ha='center', color='yellow', fontsize=9)
    
    # Vers la surface
    ax.arrow(20, 15, 25, -5, head_width=2, head_length=2, fc='#00ff00', ec='#00ff00', alpha=0.8)
    ax.text(45, 8, 'Courses\nen surface', ha='center', color='#00ff00', fontsize=9)
    
    # Débordements
    ax.arrow(20, 15, 5, -10, head_width=2, head_length=2, fc='orange', ec='orange', alpha=0.8)
    ax.text(27, 2, 'Débordements', ha='center', color='orange', fontsize=9)
    
    ax.set_title('Nico Williams - Positionnement et Mouvements Tactiques', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.legend(loc='upper left', framealpha=0.8)
    
    # Conversion en image pour Streamlit
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#2d5a2d', dpi=150, bbox_inches='tight')
    buf.seek(0)
    st.image(buf, use_column_width=True)
    plt.close()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Points Forts Tactiques:**
        - Polyvalence sur les deux flancs
        - Excellent dans les un-contre-un
        - Capacité à rentrer dans l'axe
        - Vitesse en transition
        - Bon centreur depuis les côtés
        """)
    
    with col2:
        st.markdown("""
        **🔄 Adaptations pour Barcelone:**
        - Améliorer le pressing haut
        - Travailler les automatismes de possession
        - Développer le jeu sans ballon
        - Renforcer la discipline tactique
        - Optimiser les décrochages
        """)

# Conclusion et recommandations
st.markdown("---")
st.subheader("🎯 Conclusion du Scouting Report")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00a650, #007d3c); padding: 1.5rem; border-radius: 10px; color: white;">
        <h3>✅ RECOMMANDATION FINALE</h3>
        <p><strong>TRANSFERT HAUTEMENT RECOMMANDÉ</strong></p>
        <ul>
            <li>Profil parfait pour l'ailier gauche du Barça</li>
            <li>Qualités techniques d'élite mondiale</li>
            <li>Âge idéal (22 ans) pour un projet long terme</li>
            <li>Expérience internationale confirmée</li>
            <li>Valeur marchande raisonnable (70M€)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFA500, #FF8C00); padding: 1.5rem; border-radius: 10px; color: white;">
        <h3>⚠️ POINTS D'ATTENTION</h3>
        <ul>
            <li>Adaptation défensive nécessaire</li>
            <li>Travail sur la conservation du ballon</li>
            <li>Intégration au système de jeu barcelonais</li>
            <li>Gestion de la pression médiatique</li>
            <li>Concurrence avec Raphinha</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Note finale
st.markdown("""
<div style="background: linear-gradient(45deg, #004d98, #a50044); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 2rem 0;">
    <h2>🏆 VERDICT FINAL</h2>
    <h3>Nico Williams représente le profil idéal pour permettre a l'attaque du FC Barcelone d'atteindre un nouveau milestone en terme de dangerosité et de continuer son chantier de destruction sur le foot Europeen</h3>
    <p>Ses qualités de dribble d'élite mondiale, sa capacité de progression et sa polyvalence en font un investissement stratégique parfait pour les années à venir.</p>
    <p><strong>Score global de recommandation: 9.2/10</strong></p>
</div>
""", unsafe_allow_html=True)
