import streamlit as st
import pandas as pd
import os
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide", page_icon="💎")

# --- 🎨 CORES AJUSTADAS (CORAL LEVE) ---
COR_PRINCIPAL = "#FF5733" 
COR_FUNDO = "#F8F9FA"

# --- 2. CONTROLE DE ESTADO ---
if 'ordem_preco' not in st.session_state:
    st.session_state.ordem_preco = "asc"

# --- 3. CAMINHOS E LOGO ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_TXT = os.path.join(DIRETORIO_ATUAL, "historico_postagens_teste.txt")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_image_base64(os.path.join(DIRETORIO_ATUAL, "logo.png"))

# --- 4. ESTILO CSS COMPLETO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COR_FUNDO}; }}
    
    .header-box {{
        background-color: {COR_PRINCIPAL};
        padding: 30px 10px;
        text-align: center;
        color: white;
        border-radius: 0 0 25px 25px;
        margin: -65px -20px 25px -20px;
    }}

    .logo-circular {{
        width: 100px; height: 100px;
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
    }}

    .btn-social {{
        display: inline-block;
        background-color: white;
        color: {COR_PRINCIPAL} !important;
        padding: 6px 12px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: bold;
        font-size: 13px;
        margin: 5px;
    }}

    /* Estilo do Card */
    .product-card {{
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #eee;
        text-align: center;
        margin-bottom: 5px;
    }}

    .img-produto {{
        width: 65% !important; /* Força os 30% a menos */
        border-radius: 10px;
    }}

    .discount-tag {{
        background-color: #FFD21E;
        color: {COR_PRINCIPAL};
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 12px;
        margin: 10px 0;
        display: inline-block;
    }}

    #MainMenu, header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. CABEÇALHO ---
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-circular">' if logo_b64 else '<h1>💎</h1>'
st.markdown(f"""
    <div class="header-box">
        {logo_html}
        <h2 style="margin: 5px 0;">Vitrine do Garimpeiro</h2>
        <div>
            <a href="https://chat.whatsapp.com/BJpDrJNuQKGDQJVgpV7134" class="btn-social">🟢 WhatsApp</a>
            <a href="https://t.me/ogarimpoacadinhos" class="btn-social">🔵 Telegram</a>
            <a href="https://www.instagram.com/o_garimpeiro_achadinhos_semana/" class="btn-social">📸 Instagram</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. BUSCA E FILTROS ---
busca = st.text_input("🔍 Procurar #ID ou Nome do produto")

st.write("### 📊 Organizar por:")
c1, c2, c3 = st.columns(3)
with c1: btn_recentes = st.button("✨ Recentes", use_container_width=True)
with c2: btn_desconto = st.button("📉 Desconto", use_container_width=True)
with c3:
    label_preco = "💰 Preço" if st.session_state.ordem_preco == "asc" else "💰 Preço"
    btn_preco = st.button(label_preco, use_container_width=True)

# --- 7. CARREGAMENTO ---
def carregar():
    if not os.path.exists(CAMINHO_TXT): return pd.DataFrame()
    lista = []
    with open(CAMINHO_TXT, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.count("|") >= 7:
                p = linha.split("|")
                try:
                    p_de = float(p[6].strip()); p_por = float(p[7].strip())
                    desc = int(((p_de - p_por)/p_de)*100) if p_de > 0 else 0
                    lista.append({
                        "ID": p[0].strip(), "Data": p[1].strip(), "Nome": p[3].strip(),
                        "Link": p[4].strip(), "Foto": p[5].strip(), "PrecoDe": p_de,
                        "PrecoPor": p_por, "Desconto": desc
                    })
                except: continue
    return pd.DataFrame(lista)

df = carregar()

if not df.empty:
    if btn_preco:
        st.session_state.ordem_preco = "desc" if st.session_state.ordem_preco == "asc" else "asc"
        df = df.sort_values(by="PrecoPor", ascending=(st.session_state.ordem_preco == "asc"))
    elif btn_desconto:
        df = df.sort_values(by="Desconto", ascending=False)
    else:
        df = df.iloc[::-1]

    if busca:
        df = df[df['Nome'].str.contains(busca, case=False) | df['ID'].str.contains(busca)]

    # --- 8. GRADE DE PRODUTOS CORRIGIDA ---
    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            # Criando o HTML do card como uma string única para evitar erros
            card_html = f"""
                <div class="product-card">
                    <img src="{row['Foto']}" class="img-produto">
                    <br>
                    <div class="discount-tag">-{row['Desconto']}% OFF</div>
                    <div style="font-size:12px; color:#888;">#ID {row['ID']}</div>
                    <div style="font-size:15px; font-weight:bold; color:#333; height:45px; overflow:hidden; margin:5px 0;">{row['Nome'][:55]}...</div>
                    <div style="text-decoration:line-through; color:#aaa; font-size:13px;">R$ {row['PrecoDe']:.2f}</div>
                    <div style="color:{COR_PRINCIPAL}; font-size:20px; font-weight:bold;">R$ {row['PrecoPor']:.2f}</div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.link_button("🛒 VER NA LOJA", row['Link'], use_container_width=True, type="primary")
            st.write(" ")
else:
    st.info("Aguardando garimpo...")