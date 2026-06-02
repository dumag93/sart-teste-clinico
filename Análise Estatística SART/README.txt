FERRAMENTA: Análise Estatística SART - Padrão Ouro em Neurociência Cognitiva
=============================================================================

DESCRIÇÃO:
Esta ferramenta automatiza o processamento, a filtragem rigorosa, a análise estatística e a geração de relatórios visuais para dados da Tarefa de Atenção Sustentada (SART). A versão atual foi desenvolvida com foco no rigor metodológico exigido para investigação científica de alto impacto e avaliação neuropsicológica clínica avançada. O sistema incorpora agora modelação Ex-Gaussiana, detecção dinâmica de fadiga e efeitos sequenciais (PIS).

O QUE O PROGRAMA REALIZA:

1. Varredura e leitura automática de ficheiros .json na pasta raiz.
2. Identificação automática do participante e organização em pastas com carimbo de data.
3. Auditoria de Amostra: Separação rigorosa entre artefatos temporais (respostas antecipatórias < 100ms) e trials estritamente válidos (Go/No-Go).
4. Modelação Ex-Gaussiana: Extração dos parâmetros Mu (velocidade real de processamento) e Tau (marcador de lapsos atencionais e instabilidade), essenciais como biomarcadores clínicos.
5. Análise de Efeitos Sequenciais (PIS): Cálculo da Lentificação Pós-Inibitória, medindo o custo cognitivo real (em milissegundos) para realocar a atenção após um estímulo de inibição bem-sucedido.
6. Análise de Fadiga Cognitiva (Time-on-Task): Utilização de suavização Gaussiana móvel para detetar, de forma não-arbitrária, o ponto exato de inflexão no declínio do desempenho atencional.

RELATÓRIOS VISUAIS DE ALTA RESOLUÇÃO:

- SART_Fig1_Comportamento.png: Perfil de erros (Comissão, Omissão, Antecipação) com caixa de auditoria de filtros integrada.
- SART_Fig2_TempoReacao.png: Distribuição de RT com histograma KDE, Média, Variabilidade (σ) e anotações dos parâmetros Ex-Gaussianos (Tau e Mu).
- SART_Fig3_FadigaDinamica.png: Curva de decréscimo atencional suavizada com marcação visual do ponto de inflexão de fadiga.
- SART_Fig4_CustoInibicao.png: Boxplot com stripplot (pontos reais) comparando o RT em contexto de "Cruzeiro" vs "Recuperação" (PIS).

SUMÁRIO ANALÍTICO TEXTUAL (Relatorio_SART.txt):

- Estrutura detalhada da amostra auditada (Total vs. Válidos).
- Métricas comportamentais (percentagens calculadas estritamente sobre trials válidos).
- Métricas de RT descritivas (Mín, Máx, μ, σ, CV).
- Marcadores Atencionais Ex-Gaussianos (Tau e Mu).
- Análise de PIS: Delta (em ms) do custo de inibição.
- Dinâmica de Fadiga: Ponto de inflexão e Delta de piora clínica.
- *NOVO*: Notas Metodológicas incluídas diretamente no relatório clínico para garantir transparência científica em cada bloco de cálculo.

ESTRUTURA DE ORGANIZAÇÃO DE SAÍDA:
Para cada ficheiro .json processado:

- Cria a pasta: "Nome_Do_Paciente_DD-MM-AAAA".
- Guarda os 4 gráficos científicos padronizados.
- Guarda o "Relatorio_SART.txt" detalhado.
- Move o ficheiro bruto original para a mesma pasta sob o nome: "SART_DadosBrutos_Nome_Do_Paciente.json".

COMO UTILIZAR:

1. Mova os ficheiros .json brutos gerados pela tarefa SART para a mesma pasta onde este script se encontra.
2. Certifique-se de ter as bibliotecas instaladas no seu ambiente Python (pandas, matplotlib, seaborn, numpy, scipy).
3. Execute o script "Análise Estatística SART.py".
4. Os relatórios e gráficos serão gerados automaticamente dentro das pastas individualizadas.