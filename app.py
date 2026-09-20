import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import os
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURAÇÃO E PERSISTÊNCIA DE DADOS
# ---------------------------------------------------------
st.set_page_config(page_title="Daily Water", page_icon="💧", layout="centered")

ARQUIVO_HISTORICO = "historico_agua_detalhado.csv"

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        return pd.read_csv(ARQUIVO_HISTORICO)
    else:
        return pd.DataFrame(columns=["Data", "Nome", "Tipo", "Volume_mL", "Hora"])

def salvar_registro(data_selecionada, nome, tipo, volume_ml, hora):
    df = carregar_historico()
    novo_dado = pd.DataFrame([{
        "Data": str(data_selecionada),
        "Nome": nome,
        "Tipo": tipo,
        "Volume_mL": float(volume_ml),
        "Hora": str(hora)
    }])
    df = pd.concat([df, novo_dado], ignore_index=True)
    df.to_csv(ARQUIVO_HISTORICO, index=False)

# ---------------------------------------------------------
# INICIALIZAÇÃO DE ESTADOS DA SESSÃO
# ---------------------------------------------------------
if "etapa" not in st.session_state:
    st.session_state.etapa = "apresentacao"

if "dados_usuario" not in st.session_state:
    st.session_state.dados_usuario = {}

if "dias_fechados" not in st.session_state:
    st.session_state.dias_fechados = {}

# ---------------------------------------------------------
# ETAPA 1: APRESENTAÇÃO E COLETA DE DADOS BÁSICOS
# ---------------------------------------------------------
if st.session_state.etapa == "apresentacao":
    st.title("💧 Daily Water")
    
    st.markdown("""
    ### Bem vindo ao App Daily Water!
    
    Você sabia que beber pouca água ou em excesso pode trazer malefícios?  
    Beber pouca água pode causar desidratação, cansaço, dor de cabeça e etc, beber água em excesso pode alterar o equilíbrio de sais minerais do organismo.
    
    Por isso, o ideal é consumir uma quantidade de água adequada às necessidades de cada pessoa, evitando tanto a falta quanto o excesso.
    
    Cada pessoa é única, inclusive no consumo de água, e por esse motivo o **App Daily Water** veio com o intuito de nos auxiliar a nos manter hidratados na medida de cada corpo.
    """)
    
    st.write("---")
    st.subheader("📝 Informe seus dados para calcular sua meta")
    
    with st.form("form_cadastro"):
        nome = st.text_input("Seu nome:")
        email = st.text_input("Seu e-mail:")
        peso = st.number_input("Seu peso (kg):", min_value=1.0, max_value=200.0, value=70.0, step=0.5)
        altura = st.number_input("Sua altura (m):", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        
        botao_calcular = st.form_submit_button("Calcular Volume Ideal 🧮")
        
        if botao_calcular:
            if not nome.strip():
                st.error("Por favor, preencha o seu nome para continuar.")
            else:
                meta_ideal_ml = peso * 35       
                limite_maximo_ml = peso * 70    
                
                st.session_state.dados_usuario = {
                    "nome": nome,
                    "email": email,
                    "peso": peso,
                    "altura": altura,
                    "meta_ml": meta_ideal_ml,
                    "limite_max_ml": limite_maximo_ml,
                    "ativo_lembretes": True,
                    "qtd_vezes": 8,
                    "unidade_tempo": "Horas",
                    "valor_intervalo": 2,
                    "volume_dose": meta_ideal_ml / 8
                }
                st.session_state.etapa = "calculo_feito"
                st.rerun()

# ---------------------------------------------------------
# ETAPA 2: EXIBIÇÃO DO CÁLCULO E PERGUNTA DE PROSSEGUIMENTO
# ---------------------------------------------------------
elif st.session_state.etapa == "calculo_feito":
    dados = st.session_state.dados_usuario
    meta_litros = dados["meta_ml"] / 1000
    limite_litros = dados["limite_max_ml"] / 1000
    
    st.title(f"💧 Olá, {dados['nome']}!")
    st.success(f"Com base no seu peso de **{dados['peso']} kg**, o seu volume diário ideal é de **{meta_litros:.2f} L** ({dados['meta_ml']} mL), tendo como limite máximo seguro **{limite_litros:.2f} L** ({dados['limite_max_ml']} mL) por dia.")
    
    st.write("---")
    st.markdown("### ❓ Reflexão")
    st.write("Seu consumo de água diário está adequado para você? Está abaixo do que deveria, ou você não sabe informar? Se quiser, podemos prosseguir para que possamos auxiliá-lo a manter o consumo adequado diário para você.")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Sim, quero prosseguir! 👍", use_container_width=True):
            st.session_state.etapa = "configurar_lembretes"
            st.rerun()
    with col_b2:
        if st.button("Não 🛑", use_container_width=True):
            st.session_state.etapa = "encerrado"
            st.rerun()

# ---------------------------------------------------------
# ETAPA 3: CONFIGURAÇÃO DE ALARME / LEMBRETES
# ---------------------------------------------------------
elif st.session_state.etapa == "configurar_lembretes":
    dados = st.session_state.dados_usuario
    st.title("⏰ Configuração de Alarme e Lembretes")
    st.write("Deseja configurar alertas e lembretes periódicos para te ajudar a lembrar de beber água ao longo do dia?")
    
    ativar_lembretes = st.checkbox("Sim, quero ativar lembretes de rotina", value=dados.get("ativo_lembretes", True))
    
    st.write("---")
    st.markdown("### ⚙️ Detalhes do Alarme")
    qtd_vezes_desejada = st.number_input("Quantas vezes por dia quer ser lembrado de beber água?", min_value=1, max_value=48, value=int(dados.get("qtd_vezes", 8)), step=1)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        unidade_tempo = st.selectbox("Unidade de Intervalo:", ["Horas", "Minutos"], index=0 if dados.get("unidade_tempo", "Horas") == "Horas" else 1)
    with col_t2:
        if unidade_tempo == "Horas":
            valor_intervalo = st.number_input("Intervalo em Horas:", min_value=1, max_value=24, value=int(dados.get("valor_intervalo", 2)), step=1)
        else:
            valor_intervalo = st.number_input("Intervalo em Minutos:", min_value=1, max_value=59, value=int(dados.get("valor_intervalo", 30)), step=1)
    
    st.write("")
    if st.button("Ir para o Painel Principal 🚀", use_container_width=True):
        volume_por_dose_ml = dados["meta_ml"] / qtd_vezes_desejada
        st.session_state.dados_usuario["ativo_lembretes"] = ativar_lembretes
        st.session_state.dados_usuario["qtd_vezes"] = qtd_vezes_desejada
        st.session_state.dados_usuario["unidade_tempo"] = unidade_tempo
        st.session_state.dados_usuario["valor_intervalo"] = valor_intervalo
        st.session_state.dados_usuario["volume_dose"] = volume_por_dose_ml
        st.session_state.etapa = "principal"
        st.rerun()

# ---------------------------------------------------------
# ETAPA 4: ENCERRAMENTO (CASO DIGA NÃO)
# ---------------------------------------------------------
elif st.session_state.etapa == "encerrado":
    nome = st.session_state.dados_usuario.get("nome", "Visitante")
    st.title("💧 Daily Water")
    st.info(f"Nossa jornada termina aqui, foi um prazer lhe receber, **{nome}**! Volte sempre que precisar cuidar da sua saúde e hidratação.")
    
    if st.button("🔄 Recomeçar"):
        st.session_state.etapa = "apresentacao"
        st.rerun()

# ---------------------------------------------------------
# ETAPA 5: APLICATIVO PRINCIPAL (COM ABAS: DIÁRIO E MENSAL)
# ---------------------------------------------------------
elif st.session_state.etapa == "principal":
    dados = st.session_state.dados_usuario
    nome_usuario = dados["nome"]
    meta_diaria_ml = dados["meta_ml"]
    limite_max_ml = dados["limite_max_ml"]
    
    # Barra lateral limpa contendo apenas o Menu e a Navegação Rápida
    with st.sidebar:
        st.header("⚙️ Menu de Navegação")
        pagina_selecionada = st.radio("Escolha a Visualização:", ["🏠 Painel Diário", "📈 Relatório Mensal"])
        
        st.write("---")
        st.markdown("### 🔄 Navegação Rápida")
        
        if st.button("⏰ Voltar para Alarmes", use_container_width=True):
            st.session_state.etapa = "configurar_lembretes"
            st.rerun()
            
        if st.button("🏠 Voltar à Página Inicial", use_container_width=True):
            st.session_state.etapa = "apresentacao"
            st.rerun()

    # =========================================================
    # PÁGINA 1: PAINEL DIÁRIO
    # =========================================================
    if pagina_selecionada == "🏠 Painel Diário":
        st.title(f"💧 Daily Water - Painel de {nome_usuario}")

        # Informações de Perfil e Alertas exibidas diretamente na tela
        st.write("---")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("### 👤 Meu Perfil & Plano")
            st.write(f"**Nome:** {nome_usuario}")
            st.write(f"**Peso:** {dados['peso']} kg")
            st.write(f"**Meta Diária:** {meta_diaria_ml / 1000:.2f} L")
            st.write(f"**Limite Máximo:** {limite_max_ml / 1000:.2f} L")
            
        with col_info2:
            st.markdown("### ⏰ Alertas e Lembretes")
            if dados.get("ativo_lembretes", True):
                st.write("• **Status:** Ativado ✅")
                st.write(f"• **Frequência:** {dados['qtd_vezes']}x ao dia")
                st.write(f"• **Intervalo:** A cada {dados['valor_intervalo']} {dados['unidade_tempo'].lower()}")
                st.write(f"• **Alvo por dose:** ~{dados['volume_dose']:.0f} mL")
            else:
                st.write("• **Status:** Desativado 🔕")

        st.write("---")
        st.subheader("📅 Selecione a Data do Registro")
        data_selecionada = st.date_input("Escolha o dia:", value=date.today())
        
        df_historico = carregar_historico()
        df_dia = pd.DataFrame()
        
        if not df_historico.empty:
            df_usuario = df_historico[df_historico["Nome"].astype(str).str.lower() == nome_usuario.lower()]
            df_dia = df_usuario[df_usuario["Data"] == str(data_selecionada)]

        total_consumido_dia = df_dia["Volume_mL"].sum() if not df_dia.empty else 0.0
        percentual_atingido = min(round((total_consumido_dia / meta_diaria_ml) * 100, 1), 100.0) if meta_diaria_ml > 0 else 0

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Meta do Dia", f"{meta_diaria_ml / 1000:.2f} L")
        col_m2.metric("Total Ingerido", f"{total_consumido_dia / 1000:.2f} L")
        col_m3.metric("Progresso da Meta", f"{percentual_atingido}%")

        st.progress(min(total_consumido_dia / meta_diaria_ml, 1.0))

        if total_consumido_dia > limite_max_ml:
            st.error(f"⚠️ **Atenção ao Excesso!** Você ultrapassou o limite máximo recomendado de **{limite_max_ml / 1000:.2f} L** para o seu peso.")

        if dados.get("ativo_lembretes", True):
            st.info(f"💡 **Lembrete de Hidratação:** Tente beber aproximadamente **{dados['volume_dose']:.0f} mL** a cada **{dados['valor_intervalo']} {dados['unidade_tempo'].lower()}**.")

        chave_dia_str = str(data_selecionada)
        dia_fechado = st.session_state.dias_fechados.get(chave_dia_str, False)

        st.write("---")
        st.subheader("🥤 Registrar Nova Ingestão de Água")

        if dia_fechado:
            st.info("🔒 Este dia está fechado. Reabra o dia no final da página para adicionar registros.")
        else:
            with st.form("form_registro_agua", clear_on_submit=True):
                col_f1, col_f2, col_f3, col_f4 = st.columns(4)
                with col_f1:
                    tipo_recipiente = st.selectbox("Tipo:", ["Copo", "Garrafa", "Jarra", "Outros"])
                with col_f2:
                    unidade_medida = st.selectbox("Volume:", ["mL", "Litros"])
                with col_f3:
                    valor_padrao_dose = float(dados['volume_dose']) if dados.get("ativo_lembretes", True) else 250.0
                    quantidade_valor = st.number_input("Quantidade:", min_value=1.0, max_value=5000.0, value=valor_padrao_dose, step=10.0)
                with col_f4:
                    hora_atual_padrao = datetime.now().strftime("%H:%M")
                    hora_registro = st.text_input("Hora:", value=hora_atual_padrao)
                    
                botao_salvar_copo = st.form_submit_button("➕ Adicionar à Contagem")
                
                if botao_salvar_copo:
                    volume_final_ml = quantidade_valor * 1000 if unidade_medida == "Litros" else quantidade_valor
                    salvar_registro(data_selecionada, nome_usuario, tipo_recipiente, volume_final_ml, hora_registro)
                    st.success(f"Registrado com sucesso: {quantidade_valor} {unidade_medida} ({tipo_recipiente}) às {hora_registro}!")
                    st.rerun()

        st.write("---")
        st.subheader(f"📋 Histórico de Consumo do Dia ({data_selecionada.strftime('%d/%m/%Y')})")
        
        if not df_dia.empty:
            df_exibicao = df_dia[["Hora", "Tipo", "Volume_mL"]].copy()
            df_exibicao.columns = ["Horário", "Recipiente", "Volume (mL)"]
            st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
            
            if not dia_fechado:
                if st.button("🗑️ Limpar registros deste dia"):
                    df_geral = carregar_historico()
                    df_atualizado = df_geral[~((df_geral["Nome"].astype(str).str.lower() == nome_usuario.lower()) & (df_geral["Data"] == str(data_selecionada)))]
                    df_atualizado.to_csv(ARQUIVO_HISTORICO, index=False)
                    st.success("Registros do dia limpos com sucesso!")
                    st.rerun()
        else:
            st.info("Nenhum consumo registrado para esta data ainda.")

        st.write("---")
        st.subheader("🏁 Encerramento do Dia")

        if not dia_fechado:
            st.write("Terminou suas atividades de hoje e quer consolidar o seu progresso?")
            if st.button("🔒 Fechar o Dia", use_container_width=True):
                st.session_state.dias_fechados[chave_dia_str] = True
                st.rerun()
        else:
            if total_consumido_dia >= meta_diaria_ml:
                st.success("🎉 Parabéns, você cumpriu sua meta desse dia, siga assim nos próximos!")
            else:
                st.warning("Que pena! Hoje não conseguiu cumprir a meta do dia, mas amanhã faremos melhor! 💪")
                
            st.write("### 📊 Gráfico Comparativo do Dia (mL)")
            faixa_minima = meta_diaria_ml
            faixa_adicional = max(0.0, limite_max_ml - meta_diaria_ml)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Metas Recomendadas', 'Consumo Real'],
                y=[faixa_minima, total_consumido_dia],
                name='Meta Mínima / Consumido',
                marker_color=['#29b5e8', '#21c354' if total_consumido_dia >= meta_diaria_ml else '#ff4b4b'],
                text=[f"{faixa_minima:.0f} mL", f"{total_consumido_dia:.0f} mL"],
                textposition='auto'
            ))
            fig.add_trace(go.Bar(
                x=['Metas Recomendadas', 'Consumo Real'],
                y=[faixa_adicional, 0],
                name='Margem até o Limite Máximo',
                marker_color=['#ffa15a', 'rgba(0,0,0,0)'],
                text=[f"Limite: {limite_max_ml:.0f} mL", ""],
                textposition='auto'
            ))
            fig.update_layout(barmode='stack', yaxis_title="Volume em (mL)", template="plotly_white", height=350, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
                
            if st.button("🔓 Reabrir o Dia para Edição", use_container_width=True):
                st.session_state.dias_fechados[chave_dia_str] = False
                st.rerun()

    # =========================================================
    # PÁGINA 2: RELATÓRIO MENSAL
    # =========================================================
    elif pagina_selecionada == "📈 Relatório Mensal":
        st.title(f"📈 Relatório Mensal de Hidratação")
        st.write(f"Acompanhe o desempenho consolidado dos meses para manter sua saúde em dia, **{nome_usuario}**.")

        df_geral = carregar_historico()
        
        if df_geral.empty or not ((df_geral["Nome"].astype(str).str.lower() == nome_usuario.lower())).any():
            st.info("Ainda não há registros suficientes no histórico para gerar o relatório mensal.")
        else:
            df_usuario = df_geral[df_geral["Nome"].astype(str).str.lower() == nome_usuario.lower()].copy()
            df_usuario["DataObj"] = pd.to_datetime(df_usuario["Data"])
            df_usuario["AnoMes"] = df_usuario["DataObj"].dt.strftime("%Y-%m")
            
            meses_disponiveis = sorted(df_usuario["AnoMes"].unique(), reverse=True)
            mes_selecionado = st.selectbox("Selecione o Mês/Ano:", meses_disponiveis)
            
            df_mes = df_usuario[df_usuario["AnoMes"] == mes_selecionado]
            resumo_dias = df_mes.groupby("Data")["Volume_mL"].sum().reset_index()
            resumo_dias["DataObj"] = pd.to_datetime(resumo_dias["Data"])
            resumo_dias = resumo_dias.sort_values("DataObj")
            
            mes_atual_str = datetime.now().strftime("%Y-%m")
            mes_fechado_flag = (mes_selecionado != mes_atual_str)
            
            st.write("---")
            if not mes_fechado_flag:
                st.info(f"📊 **Mês Atual ({mes_selecionado}):** Este mês está em andamento (aberto). Acompanhe a evolução diária em tempo real abaixo.")
                
                fig_evo = go.Figure()
                fig_evo.add_trace(go.Bar(
                    x=resumo_dias["Data"],
                    y=resumo_dias["Volume_mL"],
                    marker_color="#29b5e8",
                    text=[f"{v:.0f} mL" for v in resumo_dias["Volume_mL"]],
                    textposition="auto"
                ))
                fig_evo.add_hline(y=meta_diaria_ml, line_dash="dash", line_color="green", annotation_text="Meta Mínima Diária")
                fig_evo.update_layout(title="Evolução Diária do Consumo", yaxis_title="mL", template="plotly_white", height=350)
                st.plotly_chart(fig_evo, use_container_width=True)
                
            else:
                st.success(f"🔒 **Mês Fechado ({mes_selecionado}):** Relatório consolidado concluído.")
                
                dias_bateu = 0
                dias_nao_bateu = 0
                detalhes_status = []
                
                for _, row in resumo_dias.iterrows():
                    vol = row["Volume_mL"]
                    dt_str = row["Data"]
                    bateu = vol >= meta_diaria_ml
                    if bateu:
                        dias_bateu += 1
                    else:
                        dias_nao_bateu += 1
                    detalhes_status.append({"Data": dt_str, "Consumido (mL)": vol, "Meta Atingida?": "Sim ✅" if bateu else "Não ❌"})
                
                df_status_mes = pd.DataFrame(detalhes_status)
                
                col_r1, col_r2 = st.columns(2)
                col_r1.metric("Dias que Bateu a Meta", f"{dias_bateu} dias", delta="Sucesso 🟢")
                col_r2.metric("Dias Abaixo da Meta", f"{dias_nao_bateu} dias", delta="Atenção 🔴" if dias_nao_bateu > 0 else "Excelente")
                
                st.write("#### 📋 Detalhamento Diário do Mês")
                st.dataframe(df_status_mes, use_container_width=True, hide_index=True)
                
                st.write("---")
                st.subheader("💡 Diagnóstico e Atenção para os Próximos Meses")
                taxa_sucesso = (dias_bateu / len(resumo_dias)) * 100 if len(resumo_dias) > 0 else 0
                
                if taxa_sucesso >= 80:
                    st.success(f"Excelente desempenho! Você atingiu a meta em **{taxa_sucesso:.1f}%** dos dias registrados neste mês. Mantenha a constância para o próximo mês!")
                elif taxa_sucesso >= 50:
                    st.warning(f"Desempenho regular (**{taxa_sucesso:.1f}%** de aproveitamento). Atenção redobrada nos horários de pico no próximo mês.")
                else:
                    st.error(f"⚠️ **Atenção Prioritária:** Sua taxa de sucesso foi de **{taxa_sucesso:.1f}%**. Recomendamos ajustar os intervalos de lembrete com mais frequência para o próximo mês.")

            st.write("---")
            st.subheader("📧 Enviar Resumo Mensal por E-mail")
            email_destino = dados.get("email", "")
            input_email = st.text_input("Confirme o e-mail para envio:", value=email_destino)
            
            if st.button("📤 Enviar Relatório por E-mail", use_container_width=True):
                if not input_email.strip():
                    st.error("Por favor, preencha um e-mail válido.")
                else:
                    st.success(f"Sucesso! O resumo consolidado do mês **{mes_selecionado}** foi disparado com sucesso para o e-mail **{input_email}**! 🚀")