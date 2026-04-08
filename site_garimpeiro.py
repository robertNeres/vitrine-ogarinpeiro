import streamlit as st
import pandas as pd
import os
import base64
import math 
import streamlit.components.v1 as components

# --- 0. [NOVO] CONFIGURAÇÃO DO GOOGLE ANALYTICS ---
# Função que injeta a tag que o Google te passou
def configurar_google_analytics(id_ga):
    # O código abaixo é exatamente o que o Google te forneceu
    # Usamos f-string para colocar o seu ID (G-3RBXX5TFM3) lá dentro
    codigo_js = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={id_ga}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{id_ga}');
        </script>
    """
    # Injetamos o código de forma invisível (height=0) no início do carregamento
    components.html(codigo_js, height=0)


# [NOVO] FUNÇÃO PARA FORÇAR O SCROLL PARA O TOPO
												   
def scroll_ao_topo():
    # Este script procura a área principal de conteúdo e joga ela para o topo
    js = """
        <script>
            const topElement = window.parent.document.getElementById("topo");
            if (topElement) {
                topElement.scrollIntoView({behavior: "auto"});
            }
        </script>
    """
    components.html(js, height=0)


# Ativamos o rastreio com o seu ID oficial

configurar_google_analytics("G-3RBXX5TFM3")

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vitrine O Garimpeiro", layout="wide", page_icon="💎")

# --- 🎨 CORES AJUSTADAS (CORAL LEVE) ---
COR_PRINCIPAL = "#2E7D32" 
COR_FUNDO = "#F8F9FA"

# --- CONFIGURAÇÃO DE ITENS POR PÁGINA ---
ITENS_POR_PAGINA = 15 

# --- 2. CONTROLE DE ESTADO (MEMÓRIA) ---
										 
										
if 'pagina_atual' not in st.session_state: st.session_state.pagina_atual = 1
									 
																
										  
if 'filtro_ativo' not in st.session_state: st.session_state.filtro_ativo = "recentes"

# Estados para alternar ordem (ascendente/descendente)
if 'ordem_preco' not in st.session_state: st.session_state.ordem_preco = "asc"
if 'ordem_recentes' not in st.session_state: st.session_state.ordem_recentes = "novos"
if 'ordem_desconto' not in st.session_state: st.session_state.ordem_desconto = "maior"
if "scroll_top" not in st.session_state: st.session_state.scroll_top = False

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

# --- 5. CABEÇALHO --- # --- TOPO ---
st.markdown('<div id="topo"></div>', unsafe_allow_html=True)
								

# 🔥 EXECUTA SCROLL APÓS RERUN
if st.session_state.scroll_top:
    scroll_ao_topo()
    st.session_state.scroll_top = False

# --- HEADER ---               
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


def reset_pag(): 
    st.session_state.pagina_atual = 1
    st.session_state.scroll_top = True
    

busca = st.text_input("🔍 Procurar #ID ou Nome do produto", on_change=reset_pag)

# --- 6. BOTÕES DE ORGANIZAÇÃO DINÂMICOS ---                                                
st.write("### 📊 Organizar por:")
c1, c2, c3 = st.columns(3)

# Lógica de clique nos botões para salvar o estado do filtro
with c1: 
    label_rec = "✨ Recentes " if st.session_state.ordem_recentes == "novos" else "✨ Recentes "
    if st.button(label_rec, use_container_width=True):
        if st.session_state.filtro_ativo == "recentes":
            st.session_state.ordem_recentes = "antigos" if st.session_state.ordem_recentes == "novos" else "novos"
        st.session_state.filtro_ativo = "recentes"
        reset_pag()
with c2:
    label_desc = "📉 Desconto " if st.session_state.ordem_desconto == "maior" else "📉 Desconto "
    if st.button(label_desc, use_container_width=True):
        if st.session_state.filtro_ativo == "desconto":
            st.session_state.ordem_desconto = "menor" if st.session_state.ordem_desconto == "maior" else "maior"
        st.session_state.filtro_ativo = "desconto"
        reset_pag()
with c3:
    # Mostra se a próxima ordenação de preço será crescente ou decrescente no botão
    label_pre = "💰 Preço " if st.session_state.ordem_preco == "asc" else "💰 Preço "
    if st.button(label_pre, use_container_width=True):
        if st.session_state.filtro_ativo == "preco":
            st.session_state.ordem_preco = "desc" if st.session_state.ordem_preco == "asc" else "asc"
        st.session_state.filtro_ativo = "preco"
																								 
        reset_pag()
        
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
    # APLICAÇÃO DA ORDENAÇÃO BASEADA NO ESTADO
    # Agora a ordenação acontece sempre, baseada no que está salvo no session_state
    if st.session_state.filtro_ativo == "preco":
        df = df.sort_values(by="PrecoPor", ascending=(st.session_state.ordem_preco == "asc"))
    elif st.session_state.filtro_ativo == "desconto":
					  
        df = df.sort_values(by="Desconto", ascending=(st.session_state.ordem_desconto == "menor"))
				   
    else: # Recentes
       if st.session_state.ordem_recentes == "novos":
           df = df.iloc[::-1]

    # Busca (Filtra o DataFrame já ordenado)                                            
    if busca:
        df = df[df['Nome'].fillna('').str.contains(busca, case=False) | df['ID'].fillna('').str.contains(busca)]

    # --- LÓGICA DE PAGINAÇÃO ---
    total_itens = len(df)
    total_paginas = max(1, math.ceil(total_itens / ITENS_POR_PAGINA))
    
    # Garante que a página não fique fora do limite após um filtro
    if st.session_state.pagina_atual > total_paginas: st.session_state.pagina_atual = total_paginas
    if st.session_state.pagina_atual < 1: st.session_state.pagina_atual = 1

    inicio = (st.session_state.pagina_atual - 1) * ITENS_POR_PAGINA
    df_pagina = df.iloc[inicio:inicio + ITENS_POR_PAGINA]

    st.write(f"📌 Filtro: **{st.session_state.filtro_ativo.upper()}** | Página {st.session_state.pagina_atual} de {total_paginas}")
    
    # --- 8. GRADE DE PRODUTOS ---
    cols = st.columns(3)
    for i, (_, row) in enumerate(df_pagina.iterrows()):
        with cols[i % 3]:
            card_html = f"""
                <div class="product-card">
                    <img src="{row['Foto']}" class="img-produto">
                    <br><div class="discount-tag">-{row['Desconto']}% OFF</div>
                    <div style="font-size:12px; color:#888;">#ID {row['ID']}</div>
                    <div style="font-size:15px; font-weight:bold; color:#333; height:45px; overflow:hidden; margin:5px 0;">{row['Nome'][:55]}...</div>
                    <div style="text-decoration:line-through; color:#aaa; font-size:13px;">R$ {row['PrecoDe']:.2f}</div>
                    <div style="color:{COR_PRINCIPAL}; font-size:20px; font-weight:bold;">R$ {row['PrecoPor']:.2f}</div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            st.link_button("🛒 VER NA LOJA", row['Link'], use_container_width=True, type="primary")
            st.write(" ")


    # --- 9. NAVEGAÇÃO ENTRE PÁGINAS COMPLETA ---
    st.divider()
				
    c_prim, c_ant, c_pag, c_prox, c_ult = st.columns([1, 1, 2, 1, 1])
    
    with c_prim:
        if st.button("⏪ Primeira", use_container_width=True):
            st.session_state.pagina_atual = 1
            st.session_state.scroll_top = True
            st.rerun()
    with c_ant:
        if st.button("⬅️ Anterior", use_container_width=True) and st.session_state.pagina_atual > 1:
            st.session_state.pagina_atual -= 1
            st.session_state.scroll_top = True
            st.rerun()

    with c_pag:
        st.markdown(f"<p style='text-align:center; padding-top:10px;'>Página {st.session_state.pagina_atual} de {total_paginas}</p>", unsafe_allow_html=True)

    with c_prox:
        if st.button("Próxima ➡️", use_container_width=True) and st.session_state.pagina_atual < total_paginas:
															 
            st.session_state.pagina_atual += 1
            st.session_state.scroll_top = True
            st.rerun()
    with c_ult:
        if st.button("Última ⏩", use_container_width=True):
            st.session_state.pagina_atual = total_paginas
            st.session_state.scroll_top = True
            st.rerun()

else:
    st.info("Aguardando garimpo...")