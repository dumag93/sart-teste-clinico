import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import glob
import shutil # Necessário para mover os arquivos

# ==========================================
# 1. CONFIGURAÇÃO E LOOP AUTOMÁTICO
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
arquivos_json = glob.glob(os.path.join(base_dir, "*.json"))

if not arquivos_json:
    print(f"ERRO: Nenhum arquivo .json encontrado em: {base_dir}")
    sys.exit()

for input_file in arquivos_json:
    nome_sujeito = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(base_dir, nome_sujeito)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n>>> Processando: {os.path.basename(input_file)}")
    
    df = pd.read_json(input_file)

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
    # 4. CÁLCULO DAS MÉTRICAS
    # ==========================================
    validos = df_task[df_task['trial_type'] != 'artefato']
    n_nogo = len(df_task[df_task['condition'] == 'nogo'])
    n_go_total = len(df_task[df_task['condition'] == 'go'])
    n_go_validos = len(validos[validos['condition'] == 'go'])

    c = len(validos[validos['trial_type'] == 'comissao'])
    o = len(validos[validos['trial_type'] == 'omissao'])
    artefatos = len(df_task[df_task['trial_type'] == 'artefato'])
    rt_corretos = validos[validos['trial_type'] == 'go_correto']['response_time']

    # ==========================================
    # 5. GRÁFICOS
    # ==========================================
    sns.set_theme(style="ticks", context="talk")
    plt.rcParams['font.family'] = 'sans-serif'

    # Fig 1
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    taxas = {
        'Comissão\n(Impulsividade)': {'pct': (c/n_nogo*100 if n_nogo else 0), 'count': f"{c}/{n_nogo}", 'color': '#d62728'},
        'Omissão\n(Desatenção)': {'pct': (o/n_go_validos*100 if n_go_validos else 0), 'count': f"{o}/{n_go_validos}", 'color': '#ff7f0e'},
        'Antecipação\n(Piloto Automático)': {'pct': (artefatos/n_go_total*100 if n_go_total else 0), 'count': f"{artefatos}/{n_go_total}", 'color': '#7f7f7f'}
    }
    bars = ax1.bar(list(taxas.keys()), [d['pct'] for d in taxas.values()], color=[d['color'] for d in taxas.values()], edgecolor='black', linewidth=1.5, width=0.6)
    for bar, key in zip(bars, taxas.keys()):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%\n(n={taxas[key]['count']})", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax1.set_ylim(0, max([d['pct'] for d in taxas.values()]) + 20 if max([d['pct'] for d in taxas.values()]) > 0 else 100)
    ax1.set_ylabel('Taxa de Ocorrência (%)', fontweight='bold')
    ax1.set_title(f'SART - {nome_sujeito}', fontweight='bold', pad=20)
    sns.despine()
    plt.tight_layout()
    fig1.savefig(os.path.join(output_dir, 'SART_Fig1_Comportamento.png'), dpi=300)
    plt.close(fig1)

    # Fig 2
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if not rt_corretos.empty:
        sns.histplot(rt_corretos, bins=15, kde=True, color='#1f77b4', edgecolor='black', alpha=0.6, ax=ax2)
        mean_rt, sd_rt = rt_corretos.mean(), rt_corretos.std()
        ax2.axvline(mean_rt, color='red', linestyle='--', linewidth=2.5, label='Média')
        ax2.axvline(mean_rt + sd_rt, color='gray', linestyle=':', linewidth=2, label='+1 SD')
        ax2.axvline(mean_rt - sd_rt, color='gray', linestyle=':', linewidth=2, label='-1 SD')
        stats_box = (f"Média (μ): {mean_rt:.1f} ms\nVariabilidade (σ): {sd_rt:.1f} ms\nN: {len(rt_corretos)}")
        ax2.text(0.95, 0.95, stats_box, transform=ax2.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9, edgecolor='gray'))
        ax2.set_xlabel('Tempo de Reação (ms)', fontweight='bold')
        ax2.set_title(f'Distribuição RT - {nome_sujeito}', fontweight='bold', pad=20)
        ax2.legend(loc='upper left')
        sns.despine()
        plt.tight_layout()
        fig2.savefig(os.path.join(output_dir, 'SART_Fig2_TempoReacao.png'), dpi=300)
        plt.close(fig2)

    # ==========================================
    # 6. EXPORTAÇÃO TXT
    # ==========================================
    log_path = os.path.join(output_dir, 'Relatorio_SART.txt')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"=== RELATÓRIO: {nome_sujeito} ===\n")
        f.write(f"Total de Trials: {len(df_task)}\n")
        f.write(f"Erros de Comissão: {c} ({(c/n_nogo*100 if n_nogo > 0 else 0):.2f}%)\n")
        f.write(f"Erros de Omissão: {o} ({(o/n_go_validos*100 if n_go_validos > 0 else 0):.2f}%)\n")
        f.write(f"RT Médio: {rt_corretos.mean():.2f} ms\n")
        f.write(f"Artefatos: {artefatos} ({(artefatos/n_go_total*100 if n_go_total > 0 else 0):.2f}%)\n")

    # ==========================================
    # 7. ORGANIZAÇÃO: MOVER JSON PARA PASTA
    # ==========================================
    destino_json = os.path.join(output_dir, os.path.basename(input_file))
    shutil.move(input_file, destino_json)
    
    print(f"Concluído: {nome_sujeito} | JSON movido para: {output_dir}")

print("\n[SUCESSO] Processamento total de arquivos concluído.")