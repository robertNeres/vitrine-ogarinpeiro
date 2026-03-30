import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide", page_icon="💎")

# --- ESTILO CSS PARA BOTÕES E LOGO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .product-card {
        border: 1px solid #e0e0e0; padding: 20px; border-radius: 15px;
        background-color: white; margin-bottom: 25px; text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .preco-de { color: #888; text-decoration: line-through; font-size: 0.9em; }
    .preco-por { color: #ff4b4b; font-size: 1.4em; font-weight: bold; margin-top: -10px; }
    .social-btn {
        display: block; width: 100%; padding: 12px; color: white !important; 
        border-radius: 8px; text-decoration: none; margin-bottom: 10px;
        font-weight: bold; text-align: center;
    }
    .whatsapp { background-color: #25D366; }
    .telegram { background-color: #0088cc; }
    .instagram { background-color: #E1306C; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO (LOGO E REDES SOCIAIS) ---
col_logo, col_links = st.columns([1, 2])
                                                        

                   
                                
                                     
     
                                 

with col_logo:
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de possíveis nomes que você pode ter dado
    possibilidades = ["logo.png", "logo.jpg", "logo.jpeg", "Logo.png", "LOGO.PNG"]
    logo_encontrada = None

    for nome in possibilidades:
        caminho_teste = os.path.join(diretorio_atual, nome)
        if os.path.exists(caminho_teste):
            logo_encontrada = caminho_teste
            break

    if logo_encontrada:
        st.image(logo_encontrada, width=200)
    else:
        st.markdown("<h1 style='text-align: center; margin:0;'>💎</h1>", unsafe_allow_html=True)
        st.error(f"⚠️ Nenhuma logo achada em: {diretorio_atual}")
        st.write("Arquivos na pasta:", os.listdir(diretorio_atual)) # Isso vai listar tudo o que o Python vê

with col_links:
    st.write("### 🚀 Fique por dentro das ofertas!")
    # SUBSTITUA PELOS SEUS LINKS REAIS ABAIXO
    st.markdown(f"""
        <a href="https://chat.whatsapp.com/BJpDrJNuQKGDQJVgpV7134?mode=gi_t" class="social-btn whatsapp">🟢 WhatsApp</a>
        <a href="https://t.me/ogarimpoacadinhos" class="social-btn telegram">🔵 Telegram</a>
        <a href="https://www.instagram.com/o_garimpeiro_achadinhos_semana/" class="social-btn instagram">📸 Instagram</a>
    """, unsafe_allow_html=True)

st.divider()

# 1. Configuração de GPS (Acha o arquivo na mesma pasta do script)
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_txt = os.path.join(diretorio_atual, "historico_postagens_teste.txt")

st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide")
st.title("💎 Vitrine")


def carregar_dados():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    arquivo = os.path.join(diretorio_atual, "historico_postagens_teste.txt")
                                                             
    
    if not os.path.exists(arquivo):
        return pd.DataFrame()
    
    lista_produtos = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.count("|") >= 7: # Agora esperamos 7 barras por causa dos preços
                p = linha.split("|")
                lista_produtos.append({
                    "ID": p[0].strip(),
                    "Data": p[1].strip(),
                    "Nome": p[3].strip(),
                    "Link": p[4].strip(),
                    "Foto": p[5].strip(),
                    "PrecoDe": p[6].strip(),
                    "PrecoPor": p[7].strip()
                })
    return pd.DataFrame(lista_produtos)

df = carregar_dados()

if not df.empty:
    # Inverte para mostrar os mais novos no topo
    df = df.iloc[::-1]
    
    busca = st.text_input("🔍 Procure por #ID ou Nome do produto")
    if busca:
        df = df[df['Nome'].str.contains(busca, case=False) | df['ID'].str.contains(busca)]

    # Exibição em Grade
    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
                                                                             
            st.image(row['Foto'], use_container_width=True)
            st.subheader(f"#{row['ID']}")
            st.write(f"**{row['Nome'][:60]}...**")
            st.markdown(f"~~R$ {float(row['PrecoDe']):.2f}~~")
            st.markdown(f"### **R$ {float(row['PrecoPor']):.2f}** 🔥")
            st.link_button("🛒 VER NA LOJA", row['Link'])
            st.divider()
else:
    st.info("Aguardando o robô postar o primeiro produto no novo formato...")
    # Mostra o caminho para você conferir se o arquivo existe mesmo
    st.caption(f"Procurando em: {caminho_txt}")