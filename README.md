# GoNogo-Task-SART-PTBR

Este repositório contém a suíte completa para a aplicação e análise da **Tarefa de Atenção Sustentada (SART)**, desenvolvida para fins de avaliação neuropsicológica e pesquisa clínica.

O ecossistema é dividido em duas frentes principais:
1. **Coleta de Dados:** `GoNogoTask (SART)_v2.1` (Implementação OpenSesame/OSWeb).
2. **Processamento e Análise:** `Análise Estatística SART.py`.

---

## 🚀 Componentes do Projeto

### 1. GoNogoTask (SART)_v2.1
Esta versão da tarefa foi otimizada para o ambiente clínico/acadêmico. 
- **Estrutura:** Baseada no paradigma SART, com manipulação de estímulos Go/No-Go.
- **Log de Dados:** O sistema captura automaticamente identificadores do participante (`subject_name`), condições experimentais, tempo de reação e flags de artefatos.

### 2. Análise Estatística SART (Motor de Processamento)
Script em Python desenvolvido para transformar dados brutos em laudos clínicos quantitativos. Ele automatiza o ciclo completo de análise:

#### Funcionalidades Principais:
* **Pipeline de Isolamento:** O script lê arquivos `.json` brutos, processa os dados e gera pastas organizadas por participante e data.
* **Filtro Clínico:** Triagem automática de trials ("artefatos" de antecipação vs. trials válidos).
* **Auditoria de Amostra:** Transparência total no cálculo de *N* (Tamanho da amostra), diferenciando o que foi executado, descartado e validado.
* **Métricas Avançadas:**
    * **Comportamentais:** Erros de Comissão (Impulsividade), Omissão (Desatenção) e Antecipação (Automatismo).
    * **Tempo de Reação (RT):** Média (μ), Desvio Padrão (σ), Mínimo e Máximo.
* **Visualização:** Gera gráficos de alta resolução (perfil comportamental e histograma de RT) prontos para compor laudos clínicos.

---

## 📊 Estrutura de Saída (Output)

Para cada processamento, o script gera automaticamente:
1. **`Relatorio_SART.txt`**: Sumário clínico textual detalhado (contendo Ns, métricas de erro e índices de variabilidade).
2. **`SART_Fig1_Comportamento.png`**: Gráfico de barras com auditoria de filtros.
3. **`SART_Fig2_TempoReacao.png`**: Histograma de distribuição de RT com estatísticas descritivas (Min, Max, Média, etc).
4. **`SART_DadosBrutos_[Paciente].json`**: Arquivo de origem renomeado e organizado para backup histórico.

---

## 🛠 Como Utilizar

### Pré-requisitos
Certifique-se de ter o Python instalado e as bibliotecas necessárias:
```bash
pip install pandas matplotlib seaborn
