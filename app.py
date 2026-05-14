import streamlit as st
from reportlab.pdfgen import canvas
import tempfile
import time

# --- CONFIGURATION DE LA MARQUE ---
ST_NAME = "KIMIA DÉVELOPPEMENT"
ST_WHATSAPP_CS = "+237688684746"
ST_WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbDABTCKGGGQinjJWx0K"
OM_PAYMENT = "+237 688684746 (HONORINE KENDJO)"
MOMO_PAYMENT = "+237 671647378 (HONORINE KENDJO)"

st.set_page_config(page_title=ST_NAME, page_icon="💎", layout="wide")

# --- INITIALISATION ---
if 'credits' not in st.session_state:
    st.session_state.credits = 1000
if 'history' not in st.session_state:
    st.session_state.history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF8C00; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 10px; background-color: #25D366; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION (SIDEBAR) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Boss Dior Studio")
    st.title("☰ MENU")
    st.info(f"💰 Crédits : {st.session_state.credits}")
    
    if st.button("📢 Rejoindre la chaîne WhatsApp"):
        st.markdown(f'<meta http-equiv="refresh" content="0;url={ST_WHATSAPP_LINK}">', unsafe_allow_html=True)
    
    st.divider()
    st.write("📞 **Service Client**")
    st.write(f"WhatsApp: {ST_WHATSAPP_CS}")

# --- CORPS PRINCIPAL ---
st.title(f"💎 {ST_NAME}")
tab1, tab2, tab3 = st.tabs(["🚀 Générateur IA", "👤 Profil & VIP", "📜 Historique"])

with tab1:
    if st.session_state.credits < 100:
        st.error("🚨 Vos crédits sont épuisés !")
        st.markdown(f"### Passez en Mode VIP (2500 FCFA)\n**Orange:** {OM_PAYMENT}\n**MTN:** {MOMO_PAYMENT}")
    else:
        col_in, col_out = st.columns([1, 1])
        with col_in:
            st.subheader("Configuration du projet")
            p_name = st.text_input("Nom de l'article / Service")
            p_desc = st.text_area("Détails (couleur, matière, offre...)")
            p_price = st.number_input("Prix de vente (FCFA)", min_value=0, step=500)
            generate = st.button("Générer ma campagne (100 Crédits)")

        with col_out:
            if generate and p_name:
                with st.spinner("L'IA Kimia travaille..."):
                    time.sleep(2)
                    st.session_state.credits -= 100
                    ad_res = f"🔥 *{p_name.upper()}* 🔥\n\n✅ {p_desc}\n\n💰 *PRIX : {p_price:,} FCFA*\n\n📲 Commandez maintenant !\n🚀 Propulsé par #KimiaDev"
                    st.success("Campagne prête !")
                    st.code(ad_res)
                    
                    # PDF
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        c = canvas.Canvas(tmp.name)
                        c.setFont("Helvetica-Bold", 14)
                        c.drawString(100, 750, f"OFFRE COMMERCIALE : {p_name}")
                        c.setFont("Helvetica", 11)
                        c.drawString(100, 730, f"Détails: {p_desc}")
                        c.drawString(100, 710, f"Prix: {p_price} FCFA")
                        c.save()
                        with open(tmp.name, "rb") as f:
                            st.download_button("📩 Télécharger l'affiche PDF", f, file_name=f"{p_name}_kimia.pdf")
                    st.session_state.history.append({"date": time.ctime(), "name": p_name})

with tab2:
    st.subheader("Gestion du compte")
    st.image("https://via.placeholder.com/150", width=100)
    st.button("Modifier ma photo de profil")
    st.divider()
    st.markdown("### 🔐 Confidentialité")
    st.checkbox("Autoriser l'accès à la galerie pour l'importation de produits")
    st.checkbox("Autoriser le micro pour les commandes vocales")
    st.divider()
    st.write("---")
    if st.button("⭐ PASSER EN MODE PRO (2500 FCFA)"):
        st.info(f"Veuillez effectuer le dépôt sur l'un des numéros affichés dans le menu et contacter le service client.")

with tab3:
    st.subheader("Vos anciens messages")
    if not st.session_state.history:
        st.write("Aucun historique pour le moment.")
    for item in reversed(st.session_state.history):
        st.write(f"📅 {item['date']} - **{item['name']}**")
