💧 Daily Water
Aplicativo web interativo desenvolvido em Python para o monitoramento personalizado da hidratação diária, cálculo de metas hídricas individuais e controle de alarmes de rotina.

🚀 Sobre o Projeto
O Daily Water foi concebido com o objetivo de auxiliar os usuários a manterem um consumo hídrico adequado às necessidades de seus corpos, evitando tanto a desidratação quanto os riscos associados ao consumo excessivo de água. O sistema calcula a faixa ideal e o limite máximo seguro com base no peso corporal do usuário, integrando um painel de controle diário e relatórios mensais consolidados.

✨ Funcionalidades
Cálculo Personalizado de Metas: Definição da meta diária de consumo hídrico e do limite máximo seguro baseados no peso do usuário.

Configuração de Lembretes: Personalização de frequência, intervalos de tempo (horas/minutos) e volume recomendado por dose.

Painel Diário Interativo:

Registro de ingestão de água por tipos de recipientes (copo, garrafa, jarra, etc.).

Acompanhamento de progresso em tempo real com barra de progresso e métricas.

Alertas visuais em caso de extrapolação do limite máximo recomendado.

Gráficos dinâmicos construídos com Plotly.

Funcionalidade de fechamento e reabertura diária.

Relatório Mensal Consolidado: Análise de desempenho por mês, contagem de dias com metas cumpridas e diagnóstico de constância.

Persistência de Dados: Armazenamento local seguro em arquivo estruturado (historico_agua_detalhado.csv).

🛠️ Tecnologias Utilizadas
O projeto foi construído utilizando a seguinte stack tecnológica:

Python (Linguagem principal)

Streamlit (Framework para criação do WebApp interativo)

Pandas & NumPy (Manipulação e estruturação de dados)

Plotly (Visualização avançada de dados e gráficos interativos)

🌐 Acesso ao WebApp
O aplicativo está hospedado e disponível publicamente na nuvem através do Streamlit Community Cloud:
👉 Acesse o Daily Water aqui: https://daily-water-4ktnvczar6caen2hcffvy4.streamlit.app/

💻 Como Executar o Projeto Localmente
Se você deseja clonar e rodar a aplicação na sua máquina, siga os passos abaixo:

Clone o repositório:

Bash
git clone https://github.com/Raquelodaka/daily-water.git
Entre na pasta do projeto:

Bash
cd daily-water
Crie e ative um ambiente virtual (opcional, mas recomendado):

Bash
python -m venv venv
# No Windows:
venv\Scripts\activate
Instale as dependências necessárias:

Bash
pip install -r requirements.txt
Execute a aplicação via Streamlit:

Bash
streamlit run app.py
