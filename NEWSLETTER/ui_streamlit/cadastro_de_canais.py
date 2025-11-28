#!/usr/bin/env python3
"""
UI Streamlit para Cadastro e Gestão de Canais
Permite visualizar, filtrar, editar categorias, subcategorias e prioridades
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Cadastro de Canais - IANIA",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminhos
BASE_DIR = Path(__file__).parent.parent
CHANNELS_FILE = BASE_DIR / "newsletter_channels.json"

# Categorias disponíveis
CATEGORIES = ["empresa", "comunidade", "pessoa", "não considerado"]
PRIORITIES = ["alta", "média", "baixa"]

# Mapeamento de tipos (inglês ↔ português)
TYPE_MAP = {
    "person": "pessoa",
    "company": "empresa",
    "community": "comunidade"
}

# Mapeamento reverso (português → inglês)
TYPE_MAP_REVERSE = {v: k for k, v in TYPE_MAP.items()}
TYPE_MAP_REVERSE["não considerado"] = "not_considered"

def load_channels():
    """Carrega dados dos canais"""
    try:
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        channels = data.get("channels", [])
        
        # Garantir que todos os canais têm os campos necessários
        for channel in channels:
            # Mapear type de inglês para português
            if "type" in channel:
                channel["type"] = TYPE_MAP.get(channel["type"], "não considerado")
            else:
                channel["type"] = "não considerado"
            
            if "subcategory" not in channel:
                channel["subcategory"] = ""
            if "priority" not in channel:
                channel["priority"] = "média"
            
            # Converter campos numéricos para int (podem estar como string)
            numeric_fields = ["subscriber_count", "video_count", "view_count"]
            for field in numeric_fields:
                if field in channel:
                    try:
                        channel[field] = int(channel[field])
                    except (ValueError, TypeError):
                        channel[field] = 0
        
        return channels
    except Exception as e:
        st.error(f"❌ Erro ao carregar canais: {e}")
        return []

def save_channels(channels):
    """Salva dados dos canais"""
    try:
        # Converter types de volta para inglês antes de salvar
        channels_to_save = []
        for channel in channels:
            channel_copy = channel.copy()
            if "type" in channel_copy:
                channel_copy["type"] = TYPE_MAP_REVERSE.get(channel_copy["type"], "not_considered")
            channels_to_save.append(channel_copy)
        
        data = {
            "channels": channels_to_save,
            "updated_at": datetime.now().isoformat(),
            "total_channels": len(channels_to_save)
        }
        
        with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar canais: {e}")
        return False

def format_number(num):
    """Formata números grandes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def main():
    # Header
    st.title("📺 Cadastro de Canais - IANIA IA NEWS")
    st.markdown("---")
    
    # Carregar dados
    if "channels" not in st.session_state:
        st.session_state.channels = load_channels()
    
    channels = st.session_state.channels
    
    if not channels:
        st.warning("⚠️ Nenhum canal encontrado!")
        return
    
    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por categoria
    selected_categories = st.sidebar.multiselect(
        "Categoria",
        options=CATEGORIES,
        default=CATEGORIES,
        help="Selecione as categorias para visualizar"
    )
    
    # Filtro por prioridade
    selected_priorities = st.sidebar.multiselect(
        "Prioridade",
        options=PRIORITIES,
        default=PRIORITIES,
        help="Selecione as prioridades para visualizar"
    )
    
    # Filtro por texto
    search_text = st.sidebar.text_input(
        "🔎 Buscar",
        placeholder="Nome do canal...",
        help="Buscar por nome do canal"
    )
    
    st.sidebar.markdown("---")
    
    # Estatísticas
    st.sidebar.header("📊 Estatísticas")
    total = len(channels)
    by_category = {}
    for cat in CATEGORIES:
        count = sum(1 for c in channels if c.get("type") == cat)
        by_category[cat] = count
        st.sidebar.metric(cat.title(), count, f"{count/total*100:.1f}%")
    
    # Coletar subcategorias existentes (para autocomplete)
    existing_subcategories = sorted(set(
        c.get("subcategory", "").strip() 
        for c in channels 
        if c.get("subcategory", "").strip()
    ))
    
    # Filtrar canais
    filtered_channels = [
        c for c in channels
        if c.get("type") in selected_categories
        and c.get("priority") in selected_priorities
        and (not search_text or search_text.lower() in c.get("channel_title", "").lower())
    ]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Canais", len(channels))
    with col2:
        st.metric("Filtrados", len(filtered_channels))
    with col3:
        avg_subs = sum(c.get("subscriber_count", 0) for c in filtered_channels) / len(filtered_channels) if filtered_channels else 0
        st.metric("Média de Inscritos", format_number(int(avg_subs)))
    with col4:
        high_priority = sum(1 for c in filtered_channels if c.get("priority") == "alta")
        st.metric("Alta Prioridade", high_priority)
    
    st.markdown("---")
    
    # Ações em massa
    st.subheader("⚙️ Ações em Massa")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        bulk_category = st.selectbox(
            "Alterar categoria de selecionados para:",
            options=[""] + CATEGORIES,
            key="bulk_category"
        )
    
    with col2:
        bulk_priority = st.selectbox(
            "Alterar prioridade de selecionados para:",
            options=[""] + PRIORITIES,
            key="bulk_priority"
        )
    
    st.markdown("---")
    
    # Tabela de canais
    st.subheader(f"📋 Canais ({len(filtered_channels)})")
    
    if not filtered_channels:
        st.info("ℹ️ Nenhum canal encontrado com os filtros selecionados.")
        return
    
    # Criar tabela editável
    for idx, channel in enumerate(filtered_channels):
        with st.expander(
            f"**{channel.get('channel_title', 'Sem nome')}** | "
            f"{channel.get('type', 'N/A').title()} | "
            f"Prioridade: {channel.get('priority', 'média').title()} | "
            f"{format_number(channel.get('subscriber_count', 0))} inscritos",
            expanded=False
        ):
            # Criar colunas para edição
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**ID:** `{channel.get('channel_id', 'N/A')}`")
                st.markdown(f"**URL:** {channel.get('channel_url', 'N/A')}")
                st.markdown(f"**Descrição:** {channel.get('description', 'N/A')[:200]}...")
            
            with col2:
                st.markdown(f"**Inscritos:** {format_number(channel.get('subscriber_count', 0))}")
                st.markdown(f"**Vídeos:** {channel.get('video_count', 0)}")
                st.markdown(f"**Views:** {format_number(channel.get('view_count', 0))}")
            
            with col3:
                st.markdown(f"**País:** {channel.get('country', 'N/A')}")
                st.markdown(f"**Criado:** {channel.get('published_at', 'N/A')[:10]}")
            
            st.markdown("---")
            
            # Campos editáveis
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                new_category = st.selectbox(
                    "Categoria",
                    options=CATEGORIES,
                    index=CATEGORIES.index(channel.get("type", "não considerado")),
                    key=f"cat_{idx}"
                )
            
            with col2:
                # Subcategoria com autocomplete
                current_subcat = channel.get("subcategory", "")
                subcat_options = [""] + existing_subcategories + ["➕ Nova subcategoria..."]
                
                # Determinar índice inicial
                if current_subcat in existing_subcategories:
                    subcat_index = existing_subcategories.index(current_subcat) + 1
                elif current_subcat:
                    subcat_index = len(subcat_options) - 1  # "Nova subcategoria"
                else:
                    subcat_index = 0
                
                selected_subcat = st.selectbox(
                    "Subcategoria",
                    options=subcat_options,
                    index=subcat_index,
                    key=f"subcat_select_{idx}"
                )
                
                # Se escolheu "Nova subcategoria", mostrar campo de texto
                if selected_subcat == "➕ Nova subcategoria...":
                    new_subcategory = st.text_input(
                        "Digite a nova subcategoria:",
                        value=current_subcat if current_subcat not in existing_subcategories else "",
                        placeholder="Ex: Tech News, AI Tools, etc.",
                        key=f"subcat_text_{idx}"
                    )
                else:
                    new_subcategory = selected_subcat
            
            with col3:
                new_priority = st.selectbox(
                    "Prioridade",
                    options=PRIORITIES,
                    index=PRIORITIES.index(channel.get("priority", "média")),
                    key=f"prior_{idx}"
                )
            
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.checkbox("Selecionar", key=f"select_{idx}"):
                    channel["_selected"] = True
                else:
                    channel["_selected"] = False
            
            # Atualizar dados se mudou
            if (new_category != channel.get("type") or 
                new_subcategory != channel.get("subcategory") or 
                new_priority != channel.get("priority")):
                
                # Encontrar canal original na lista completa
                for c in st.session_state.channels:
                    if c.get("channel_id") == channel.get("channel_id"):
                        c["type"] = new_category
                        c["subcategory"] = new_subcategory
                        c["priority"] = new_priority
                        break
    
    st.markdown("---")
    
    # Botões de ação
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
            if save_channels(st.session_state.channels):
                st.success("✅ Alterações salvas com sucesso!")
                st.balloons()
            else:
                st.error("❌ Erro ao salvar alterações!")
    
    with col2:
        if st.button("🔄 Recarregar Dados", use_container_width=True):
            st.session_state.channels = load_channels()
            st.rerun()
    
    # Aplicar ações em massa
    if bulk_category or bulk_priority:
        selected_channels = [c for c in filtered_channels if c.get("_selected")]
        
        if selected_channels:
            st.info(f"ℹ️ {len(selected_channels)} canais selecionados")
            
            if st.button("✨ Aplicar Ações em Massa", type="secondary"):
                for channel in selected_channels:
                    for c in st.session_state.channels:
                        if c.get("channel_id") == channel.get("channel_id"):
                            if bulk_category:
                                c["type"] = bulk_category
                            if bulk_priority:
                                c["priority"] = bulk_priority
                            break
                
                st.success(f"✅ Ações aplicadas a {len(selected_channels)} canais!")
                st.rerun()

if __name__ == "__main__":
    main()
