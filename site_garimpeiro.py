import streamlit as st
import pandas as pd
import os
import base64
import math 
import streamlit.components.v1 as components

# --- 0. [NOVO] CONFIGURAÇÃO DO GOOGLE ANALYTICS ---
# [ESTUDO] NOVA ESTRATÉGIA: Injeção via Componente de HTML
from streamlit.components.v1 import html

def configurar_google_analytics(id_ga):
    # Definimos o código exatamente como o Google quer
    codigo_js = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={id_ga}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{id_ga}');
        </script>
    """
    # [IMPORTANTE] Inserimos o componente. 
    # O segredo: ele precisa estar no código, mas não precisa aparecer.
    html(codigo_js, height=0)

# Chame a função logo após o st.set_page_config
configurar_google_analytics("G-3RBXX5TFM3")

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide", page_icon="💎")

# --- 🎨 CORES AJUSTADAS (CORAL LEVE) ---
COR_PRINCIPAL = "#2E7D32" 
COR_FUNDO = "#F8F9FA"

# --- CONFIGURAÇÃO DE ITENS POR PÁGINA ---
ITENS_POR_PAGINA = 12 

# --- 2. CONTROLE DE ESTADO ---
if 'ordem_preco' not in st.session_state:
    st.session_state.ordem_preco = "asc"
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 1

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
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* [NOVO] Adicionei uma sombra leve no header */
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
        width: 65% !important;
        border-radius: 10px;
    }}

    .discount-tag {{
        background-color: #FFD21E;
        /* [AJUSTE] Cor do texto do desconto para combinar com o Kiwi */
        color: #333; 
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

# --- 6. [NOVO] FUNÇÃO DE RESET DE PÁGINA ---
# Criada para que o site volte à página 1 sempre que o usuário mudar o filtro ou busca
def reset_pag(): 
    st.session_state.pagina_atual = 1

busca = st.text_input("🔍 Procurar #ID ou Nome do produto", on_change=reset_pag)

st.write("### 📊 Organizar por:")
c1, c2, c3 = st.columns(3)
with c1: btn_recentes = st.button("✨ Recentes", use_container_width=True)
with c2: btn_desconto = st.button("📉 Desconto", use_container_width=True)
with c3:
    label_preco = "💰 Preço"
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
        reset_pag()
    elif btn_desconto:
        df = df.sort_values(by="Desconto", ascending=False)
        reset_pag()
    else:
        df = df.iloc[::-1]

    if busca:
        df = df[df['Nome'].str.contains(busca, case=False) | df['ID'].str.contains(busca)]

    # --- LÓGICA DE PAGINAÇÃO ---
    total_itens = len(df)
    total_paginas = math.ceil(total_itens / ITENS_POR_PAGINA)
    
    # Garante que a página não fique fora do limite após um filtro
    if st.session_state.pagina_atual > total_paginas: st.session_state.pagina_atual = total_paginas
    if st.session_state.pagina_atual < 1: st.session_state.pagina_atual = 1

    inicio = (st.session_state.pagina_atual - 1) * ITENS_POR_PAGINA
    fim = inicio + ITENS_POR_PAGINA
    df_pagina = df.iloc[inicio:fim]

    st.write(f"📌 Página {st.session_state.pagina_atual} de {total_paginas} ({total_itens} produtos)")
    
    # --- 8. GRADE DE PRODUTOS ---
    cols = st.columns(3)
    for i, (_, row) in enumerate(df_pagina.iterrows()):
        with cols[i % 3]:
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

    # --- 9. NAVEGAÇÃO ENTRE PÁGINAS ---
    st.divider()
    c_voltar, c_meio, c_avancar = st.columns([1, 2, 1])
    with c_voltar:
        if st.button("⬅️ Anterior") and st.session_state.pagina_atual > 1:
            st.session_state.pagina_atual -= 1
            st.rerun()
    with c_meio:
        st.markdown(f"<p style='text-align:center;'>Página {st.session_state.pagina_atual} de {total_paginas}</p>", unsafe_allow_html=True)
    with c_avancar:
        if st.button("Próxima ➡️") and st.session_state.pagina_atual < total_paginas:
            st.session_state.pagina_atual += 1
            st.rerun()
else:
    st.info("Aguardando garimpo...")