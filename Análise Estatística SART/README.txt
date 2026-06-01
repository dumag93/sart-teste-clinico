FERRAMENTA: Análise Estatística SART
====================================

DESCRIÇÃO:

Este script automatiza o processamento, limpeza, análise estatística e geração de relatórios visuais para dados da Tarefa de Atenção Sustentada (SART). A versão atual foca em rigor metodológico, oferecendo auditoria completa da amostra e métricas avançadas de variabilidade temporal.

O QUE O PROGRAMA REALIZA:

1. Varredura e leitura automática de arquivos .json na pasta raiz.
2. Identificação automática do nome do participante nos metadados.
3. Criação de pastas individualizadas com carimbo de data (Nome_Do_Paciente_DD-MM-AAAA).
4. Proteção de histórico: numeração sequencial (_1, _2...) para testes realizados no mesmo dia.
5. Triagem e Classificação: Separação rigorosa de Artefatos, Comissão (Impulsividade), Omissão (Desatenção) e Respostas Go.
6. Auditoria de Amostra: Cálculo explícito de N total, N de artefatos e N de trials válidos por condição (Go/No-Go).
7. Relatórios Visuais de Alta Resolução:
   - SART_Fig1_Comportamento.png: Perfil de erros com caixa de auditoria de filtros integrada.
   - SART_Fig2_TempoReacao.png: Histograma de RT com Média, Variabilidade (σ) e Coeficiente de Variação (CV).
8. Sumário Analítico Textual (Relatorio_SART.txt):
   - Estrutura completa da amostra.
   - Métricas comportamentais (porcentagens baseadas em N válidos).
   - Métricas de RT detalhadas (Min, Max, Médio, σ, CV).

ESTRUTURA DE ORGANIZAÇÃO DE SAÍDA:

Para cada arquivo .json processado:
- Cria a pasta: "Nome_Do_Paciente_DD-MM-AAAA".
- Salva o "Relatorio_SART.txt" com o resumo clínico detalhado.
- Salva os gráficos "SART_Fig1_Comportamento.png" e "SART_Fig2_TempoReacao.png".
- Renomeia e move o arquivo bruto original para: "SART_DadosBrutos_Nome_Do_Paciente_Data_Versao.json".

COMO USAR:

1. Baixe o arquivo de dados bruto (formato .json) gerado pelo seu teste.
2. Mova o arquivo bruto para a pasta onde o script "Análise Estatística SART.py" está localizado.
3. Certifique-se de ter as bibliotecas instaladas (pandas, matplotlib, seaborn).
4. Execute o arquivo "Análise Estatística SART.py".
5. A análise será gerada automaticamente dentro da pasta do paciente.

NOTAS CLÍNICAS:

- O Coeficiente de Variação (CV) apresentado é o padrão-ouro para análise de instabilidade da atenção sustentada.
- A auditoria de "N" (tamanho da amostra) em todos os outputs garante total transparência sobre a fidelidade do dado analisado.

REQUISITOS DE SISTEMA:

- Python 3.x
- Bibliotecas: pandas, matplotlib, seaborn.