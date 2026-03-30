import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
# Importante: set_page_config deve ser a primeira linha de comando Streamlit
st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide", page_icon="💎")

# --- ESTILO CSS PARA O VISUAL "SHOPEE" ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    
    /* Cabeçalho Laranja Shopee */
    .header-container {
        background-color: #ee4d2d;
        padding: 20px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    
    .logo-img {
        border-radius: 50%;
        border: 4px solid white;
        margin-bottom: 10px;
    }

    /* Estilo das Redes Sociais */
    .social-btn { 
        display: inline-block; padding: 8px 15px; color: #ee4d2d !important; 
        background-color: white; border-radius: 20px; text-decoration: none; 
        margin: 5px; font-weight: bold; font-size: 14px;
    }

    /* Filtros e Abas */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #ddd;
        background-color: white;
        color: #555;
    }
    .stButton>button:hover {
        border-color: #ee4d2d;
        color: #ee4d2d;
    }
    
    /* Card de Produto */
    .product-card {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
possibilidades = ["logo.png", "logo.jpg", "logo.jpeg", "Logo.png"]
logo_encontrada = None

for nome in possibilidades:
    caminho_teste = os.path.join(diretorio_atual, nome)
    if os.path.exists(caminho_teste):
        logo_encontrada = caminho_teste
        break

if logo_encontrada:
    st.image(logo_encontrada, width=120)
else:
    st.markdown("<h1>💎</h1>", unsafe_allow_html=True)

st.markdown("<h2>ACHADINHOS SHOPEE</h2>", unsafe_allow_html=True)

# Redes Sociais
st.markdown(f"""
    <a href="https://chat.whatsapp.com/BJpDrJNuQKGDQJVgpV7134?mode=gi_t" class="social-btn">🟢 WhatsApp</a>
    <a href="https://t.me/ogarimpoacadinhos" class="social-btn">🚀 Telegram</a>
    <a href="https://www.instagram.com/o_garimpeiro_achadinhos_semana/" class="social-btn">📸 Instagram</a>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- FUNÇÃO DE DADOS ---
def carregar_dados():
    arquivo = os.path.join(diretorio_atual, "historico_postagens_teste.txt")
    if not os.path.exists(arquivo):
        return pd.DataFrame()
    
    lista_produtos = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.count("|") >= 7:
                p = linha.split("|")
                try:
                    p_de = float(p[6].strip())
                    p_por = float(p[7].strip())
                    # Calcula o desconto automaticamente
                    desconto = int(((p_de - p_por) / p_de) * 100) if p_de > 0 else 0
                    
                    lista_produtos.append({
                        "ID": p[0].strip(),
                        "Data": p[1].strip(),
                        "Nome": p[3].strip(),
                        "Link": p[4].strip(),
                        "Foto": p[5].strip(),
                        "PrecoDe": p_de,
                        "PrecoPor": p_por,
                        "Desconto": desconto
                    })
                except:
                    continue
    return pd.DataFrame(lista_produtos)

df = carregar_dados()

# --- INTERFACE DE BUSCA E FILTROS ---
col_busca, col_filtros = st.columns([2, 1])

with col_busca:
    busca = st.text_input("🔍 O que você procura hoje?", placeholder="Busque por nome ou #ID")

# Abas Simbolizadas (Produtos / Categorias)
tab1, tab2 = st.tabs(["📦 Produtos", "📂 Categorias"])

with tab1:
    if not df.empty:
        # Barra de filtros de ordenação
        st.write("---")
        c1, c2, c3, c4 = st.columns([1,1,1,1])
        with c1: f_recente = st.button("✨ Recentes")
        with c2: f_popular = st.button("🔥 Popular")
        with c3: f_desconto = st.button("📉 Desconto")
        with c4: f_preco = st.button("💰 Preço")

        # Lógica de filtros
        if f_desconto:
            df = df.sort_values(by="Desconto", ascending=False)
        elif f_preco:
            df = df.sort_values(by="PrecoPor", ascending=True)
        else:
            df = df.iloc[::-1] # Padrão: mais recentes

        if busca:
            df = df[df['Nome'].str.contains(busca, case=False) | df['ID'].str.contains(busca)]

        # --- GRID DE PRODUTOS ---
        cols = st.columns(3)
        for i, (_, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="position: relative; background-color: white; border-radius: 10px; padding: 5px; border: 1px solid #eee;">
                    <div style="position: absolute; top: 10px; right: 10px; background-color: #ffeb3b; color: #ee4d2d; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 14px; z-index: 1;">
                        -{row['Desconto']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.image(row['Foto'], use_container_width=True)
                st.caption(f"#{row['ID']}")
                st.write(f"**{row['Nome'][:50]}...**")
                st.markdown(f"<span style='color: #888; text-decoration: line-through; font-size: 12px;'>R$ {row['PrecoDe']:.2f}</span>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color: #ee4d2d; margin-top: 0;'>R$ {row['PrecoPor']:.2f}</h3>", unsafe_allow_html=True)
                st.link_button("🛒 VER NA SHOPEE", row['Link'], type="primary")
                st.write("---")
    else:
        st.info("Aguardando o robô garimpar as ofertas...")

with tab2:
    st.write("### 🚧 Em breve: Filtro por categorias!")

# Rodapé simples
st.markdown("<p style='text-align: center; color: #888;'>💎 O Garimpeiro AI - 2026</p>", unsafe_allow_html=True)