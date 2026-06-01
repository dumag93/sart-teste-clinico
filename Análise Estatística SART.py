import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ==========================================
# 1. CONFIGURAÇÃO E CARREGAMENTO
# ==========================================
# Substitua pelo nome do seu arquivo atual
input_file = 'G__Meu Drive_OpenSesame_Meus Testes_subject-5_v2.csv'
output_dir = os.getcwd() 

if not os.path.exists(input_file):
    print(f"ERRO: O arquivo '{input_file}' não foi encontrado.")
    sys.exit()

df = pd.read_csv(input_file)

# ==========================================
# 2. LIMPEZA E SEPARAÇÃO DE FASES
# ==========================================
if 'count_Trial_Loop_Task_Phase' in df.columns:
    df_task = df.dropna(subset=['count_Trial_Loop_Task_Phase']).copy()
else:
    df_task = df.copy()

cols_to_numeric = ['response_time', 'correct', 'is_artifact']
for col in cols_to_numeric:
    if col in df_task.columns:
        df_task[col] = pd.to_numeric(df_task[col], errors='coerce')

# ==========================================
# 3. CLASSIFICAÇÃO CLÍNICA
# ==========================================
def categorizar_trial(row):
    if row.get('is_artifact') == 1: return 'artefato'
    if row['condition'] == 'go': return 'go_correto' if row['correct'] == 1 else 'omissao'
    elif row['condition'] == 'nogo': return 'nogo_correto' if row['correct'] == 1 else 'comissao'
    return 'outro'

df_task['trial_type'] = df_task.apply(categorizar_trial, axis=1)

# ==========================================
# 4. CÁLCULO DAS MÉTRICAS (Para Terminal e Gráficos)
# ==========================================
validos = df_task[df_task['trial_type'] != 'artefato']

n_nogo = len(df_task[df_task['condition'] == 'nogo'])
n_go_total = len(df_task[df_task['condition'] == 'go'])
n_go_validos = len(validos[validos['condition'] == 'go'])

c = len(validos[validos['trial_type'] == 'comissao'])
o = len(validos[validos['trial_type'] == 'omissao'])
artefatos = len(df_task[df_task['trial_type'] == 'artefato'])

rt_corretos = validos[validos['trial_type'] == 'go_correto']['response_time']

# Terminal Output
print("\n" + "="*40 + "\n RELATÓRIO CLÍNICO SART \n" + "="*40)
print(f"Total de Trials (Tarefa): {len(df_task)}")
print("\n--- CONTROLE INIBITÓRIO (No-Go) ---")
print(f"Erros de Comissão: {c} de {n_nogo} trials ({(c/n_nogo*100 if n_nogo > 0 else 0):.2f}%)")
print("\n--- ATENÇÃO SUSTENTADA (Go) ---")
print(f"Erros de Omissão: {o} de {n_go_validos} trials válidos ({(o/n_go_validos*100 if n_go_validos > 0 else 0):.2f}%)")
print("\n--- PERFIL DE VELOCIDADE ---")
print(f"RT Médio: {rt_corretos.mean():.2f} ms | SD: {rt_corretos.std():.2f} ms")
print("\n--- COMPORTAMENTO DE ANTECIPAÇÃO ---")
print(f"Artefatos (<100ms): {artefatos} trials ({(artefatos/n_go_total*100 if n_go_total > 0 else 0):.2f}%)")

# ==========================================
# 5. GRÁFICOS CIENTÍFICOS (Alta Qualidade)
# ==========================================
# Configuração de estilo APA-like
sns.set_theme(style="ticks", context="talk")
plt.rcParams['font.family'] = 'sans-serif'

# ---------------------------------------------------------
# FIGURA 1: Perfil Comportamental (Taxas Clínicas)
# ---------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(10, 6))

taxas = {
    'Comissão\n(Impulsividade)': {'pct': (c/n_nogo*100 if n_nogo else 0), 'count': f"{c}/{n_nogo}", 'color': '#d62728'},
    'Omissão\n(Desatenção)': {'pct': (o/n_go_validos*100 if n_go_validos else 0), 'count': f"{o}/{n_go_validos}", 'color': '#ff7f0e'},
    'Antecipação\n(Piloto Automático)': {'pct': (artefatos/n_go_total*100 if n_go_total else 0), 'count': f"{artefatos}/{n_go_total}", 'color': '#7f7f7f'}
}

x_labels = list(taxas.keys())
y_values = [d['pct'] for d in taxas.values()]
colors = [d['color'] for d in taxas.values()]

bars = ax1.bar(x_labels, y_values, color=colors, edgecolor='black', linewidth=1.5, width=0.6)

# Anotações diretas nas barras
for bar, key in zip(bars, taxas.keys()):
    yval = bar.get_height()
    contagem_texto = taxas[key]['count']
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%\n(n={contagem_texto})", 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylim(0, max(y_values) + 20 if max(y_values) > 0 else 100) # Espaço para o texto
ax1.set_ylabel('Taxa de Ocorrência (%)', fontweight='bold')
ax1.set_title('Perfil de Erros e Comportamento (SART)', fontweight='bold', pad=20)
sns.despine() # Remove linhas de topo e direita (padrão científico)

plt.tight_layout()
fig1.savefig(os.path.join(output_dir, 'SART_Fig1_Comportamento.png'), dpi=300)

# ---------------------------------------------------------
# FIGURA 2: Distribuição do Tempo de Reação com KDE e Stats
# ---------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(10, 6))

if not rt_corretos.empty:
    # Histograma com Curva de Densidade
    sns.histplot(rt_corretos, bins=15, kde=True, color='#1f77b4', edgecolor='black', alpha=0.6, ax=ax2)
    
    # Linhas de Média e Desvio Padrão
    mean_rt = rt_corretos.mean()
    sd_rt = rt_corretos.std()
    
    ax2.axvline(mean_rt, color='red', linestyle='--', linewidth=2.5, label='Média')
    ax2.axvline(mean_rt + sd_rt, color='gray', linestyle=':', linewidth=2, label='+1 SD')
    ax2.axvline(mean_rt - sd_rt, color='gray', linestyle=':', linewidth=2, label='-1 SD')

    # Caixa de Texto com todas as métricas embutidas usando símbolos nativos
    stats_box = (
        f"ESTATÍSTICAS DA TAREFA\n"
        f"----------------------\n"
        f"Média (μ): {mean_rt:.1f} ms\n"
        f"Variabilidade (σ): {sd_rt:.1f} ms\n"
        f"Mais Rápido: {rt_corretos.min():.0f} ms\n"
        f"Mais Lento: {rt_corretos.max():.0f} ms\n"
        f"Trials Válidos: N = {len(rt_corretos)}"
    )
    
    props = dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9, edgecolor='gray')
    ax2.text(0.95, 0.95, stats_box, transform=ax2.transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='right', bbox=props)

    ax2.set_xlabel('Tempo de Reação (ms)', fontweight='bold')
    ax2.set_ylabel('Frequência Absoluta', fontweight='bold')
    ax2.set_title('Distribuição da Velocidade de Processamento (Apenas Go Corretos)', fontweight='bold', pad=20)
    ax2.legend(loc='upper left')
    sns.despine()

    plt.tight_layout()
    fig2.savefig(os.path.join(output_dir, 'SART_Fig2_TempoReacao.png'), dpi=300)

print(f"\n[SUCESSO] Imagens padronizadas geradas com sucesso (SART_Fig1_Comportamento.png e SART_Fig2_TempoReacao.png).")