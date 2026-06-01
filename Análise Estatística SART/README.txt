FERRAMENTA: Análise Estatística SART
====================================

DESCRIÇÃO:
Este script automatiza o processamento, limpeza, análise estatística e geração de relatórios visuais para dados da tarefa de atenção sustentada (SART).

O programa realiza:
1. Leitura de arquivos .json de coleta (formato OpenSesame/OSWeb).
2. Classificação automática de trials (Go, No-Go, Omissão, Comissão, Artefatos).
3. Cálculo de métricas clínicas e comportamentais.
4. Geração de gráficos de alta qualidade (Perfil de Erros e Distribuição de RT).
5. Geração de relatório textual (Relatorio_SART.txt) com dados brutos.

ORGANIZAÇÃO:
O script busca todos os arquivos .json na pasta raiz. Para cada arquivo encontrado:
- Cria uma subpasta com o nome do sujeito.
- Gera as figuras e o relatório dentro desta subpasta.
- Move o arquivo .json original para dentro da subpasta, mantendo a raiz organizada.

COMO USAR:
1. Coloque os arquivos .json a serem processados na mesma pasta que este script.
2. Certifique-se de ter as bibliotecas instaladas (pandas, matplotlib, seaborn).
3. Execute o arquivo "Análise Estatística SART_2.py".
4. Os resultados estarão disponíveis nas pastas criadas individualmente para cada sujeito.

REQUISITOS:
- Python 3.x
- Bibliotecas: pandas, matplotlib, seaborn