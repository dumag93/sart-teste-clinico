import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import glob
import shutil
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO E LOOP AUTOMÁTICO
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
arquivos_json = glob.glob(os.path.join(base_dir, "*.json"))

if not arquivos_json:
    print(f"ERRO: Nenhum arquivo .json encontrado em: {base_dir}")
    sys.exit()

for input_file in arquivos_json:
    print(f"\n>>> Lendo arquivo bruto: {os.path.basename(input_file)}")
    
    # Lê o arquivo JSON para a memória
    df = pd.read_json(input_file)
    
    # --- PROCURA O NOME DO PARTICIPANTE NO FORMATO OSWEB (JSON) ---
    nome_bruto = None
    
    # Tentativa 1: Verifica se veio como coluna direta (comum em conversões)
    if 'subject_name' in df.columns and not df['subject_name'].dropna().empty:
        nome_bruto = str(df['subject_name'].dropna().iloc[0])
        
    # Tentativa 2: Procura dentro do dicionário da coluna 'vars' (padrão OSWeb/Chrysalis)
    elif 'vars' in df.columns and not df['vars'].dropna().empty:
        primeira_linha_vars = df['vars'].dropna().iloc[0]
        if isinstance(primeira_linha_vars, dict) and 'subject_name' in primeira_linha_vars:
            nome_bruto = str(primeira_linha_vars['subject_name'])
            
    # Tentativa 3: Varre todas as linhas da coluna 'parameter' ou 'value' se existirem
    if not nome_bruto:
        for col in df.columns:
            if df[col].astype(str).str.contains('subject_name').any():
                linha = df[df[col].astype(str).str.contains('subject_name')].iloc[0]
                if 'subject_name' in str(linha):
                    nome_bruto = "Identificado_No_Log"
                    
    # Fallback se realmente não achar nada
    if not nome_bruto:
        nome_bruto = "Participante_Anonimo"
        
    # Limpa o nome para uso seguro em pastas do Windows/Mac (remove caracteres inválidos)
    nome_limpo = "".join([c for c in nome_bruto if c.isalnum() or c in (' ', '_', '-')]).strip()
    nome_sujeito = nome_limpo.replace(" ", "_")
    
    if not nome_sujeito:
        nome_sujeito = "Participante_Anonimo"

    # Captura a data exata em que o script está rodando (Dia-Mês-Ano)
    data_atual = datetime.now().strftime("%d-%m-%Y")
    
    # Base do nome: Nome_Data (ex: Luis_Eduardo_01-06-2026)
    nome_base_pasta = f"{nome_sujeito}_{data_atual}"
    
    # --- LÓGICA DE ENUMERAÇÃO SEQUENCIAL (1, 2, 3...) ---
    output_dir = os.path.join(base_dir, nome_base_pasta)
    nome_final_paciente = nome_base_pasta
    
    if os.path.exists(output_dir):
        contador = 1
        while os.path.exists(os.path.join(base_dir, f"{nome_base_pasta}_{contador}")):
            contador += 1
        nome_final_paciente = f"{nome_base_pasta}_{contador}"
        output_dir = os.path.join(base_dir, nome_final_paciente)

    # Cria a pasta exclusiva enumerada
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"    Paciente identificado: {nome_sujeito}")
    print(f"    Pasta criada com sucesso: {nome_final_paciente}")

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
    trials_validos_total = len(validos)
    
    rt_corretos = validos[validos['trial_type'] == 'go_correto']['response_time']

    # ==========================================
    # 5. GRÁFICOS (ATUALIZADO COM AS INFORMAÇÕES DE FILTRO E EXTREMOS)
    # ==========================================
    sns.set_theme(style="ticks", context="talk")
    plt.rcParams['font.family'] = 'sans-serif'

    # Fig 1 - Perfil Comportamental
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    taxas = {
        'Comissão\n(Impulsividade)': {'pct': (c/n_nogo*100 if n_nogo else 0), 'count': f"{c}/{n_nogo}", 'color': '#d62728'},
        'Omissão\n(Desatenção)': {'pct': (o/n_go_validos*100 if n_go_validos else 0), 'count': f"{o}/{n_go_validos}", 'color': '#ff7f0e'},
        'Antecipação\n(Comportamento Automatizado)': {'pct': (artefatos/n_go_total*100 if n_go_total else 0), 'count': f"{artefatos}/{n_go_total}", 'color': '#7f7f7f'}
    }
    bars = ax1.bar(list(taxas.keys()), [d['pct'] for d in taxas.values()], color=[d['color'] for d in taxas.values()], edgecolor='black', linewidth=1.5, width=0.6)
    for bar, key in zip(bars, taxas.keys()):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.1f}%\n(n={taxas[key]['count']})", ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Adiciona caixa de auditoria de filtros na Fig 1
    pct_desc = (artefatos / len(df_task) * 100) if len(df_task) > 0 else 0
    pct_val = (trials_validos_total / len(df_task) * 100) if len(df_task) > 0 else 0
    filtro_box = f"Total Executado: {len(df_task)}\nDescartados (Artefatos): {artefatos} ({pct_desc:.1f}%)\nVálidos Pós-Filtro: {trials_validos_total} ({pct_val:.1f}%)"
    ax1.text(0.95, 0.95, filtro_box, transform=ax1.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', alpha=0.9, edgecolor='gray'))

    ax1.set_ylim(0, max([d['pct'] for d in taxas.values()]) + 20 if max([d['pct'] for d in taxas.values()]) > 0 else 100)
    ax1.set_ylabel('Taxa de Ocorrência (%)', fontweight='bold')
    ax1.set_title(f'SART - {nome_sujeito}', fontweight='bold', pad=20)
    sns.despine()
    plt.tight_layout()
    fig1.savefig(os.path.join(output_dir, 'SART_Fig1_Comportamento.png'), dpi=300)
    plt.close(fig1)

    # Fig 2 - Distribuição de Tempo de Reação
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if not rt_corretos.empty:
        sns.histplot(rt_corretos, bins=15, kde=True, color='#1f77b4', edgecolor='black', alpha=0.6, ax=ax2)
        mean_rt, sd_rt = rt_corretos.mean(), rt_corretos.std()
        min_rt, max_rt = rt_corretos.min(), rt_corretos.max()
        
        ax2.axvline(mean_rt, color='red', linestyle='--', linewidth=2.5, label='Média')
        ax2.axvline(mean_rt + sd_rt, color='gray', linestyle=':', linewidth=2, label='+1 SD')
        ax2.axvline(mean_rt - sd_rt, color='gray', linestyle=':', linewidth=2, label='-1 SD')
        
        # Caixa de estatísticas atualizada com os limites máximos e mínimos pós-filtro
        stats_box = (
            f"Mínimo (Min): {min_rt:.1f} ms\n"
            f"Máximo (Max): {max_rt:.1f} ms\n"
            f"Média (μ): {mean_rt:.1f} ms\n"
            f"Variabilidade (σ): {sd_rt:.1f} ms\n"
            f"N (Acertos Go): {len(rt_corretos)}"
        )
        ax2.text(0.95, 0.95, stats_box, transform=ax2.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9, edgecolor='gray'))
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
    
    if not rt_corretos.empty:
        rt_medio_texto = f"{rt_corretos.mean():.2f} ms"
        rt_variabilidade_texto = f"{rt_corretos.std():.2f} ms"
        rt_minimo_texto = f"{rt_corretos.min():.2f} ms"
        rt_maximo_texto = f"{rt_corretos.max():.2f} ms"
    else:
        rt_medio_texto = "N/A"
        rt_variabilidade_texto = "N/A"
        rt_minimo_texto = "N/A"
        rt_maximo_texto = "N/A"
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"=== RELATÓRIO CLÍNICO SART: {nome_sujeito} ===\n")
        f.write(f"Data de Processamento: {data_atual}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total de Trials Executados: {len(df_task)}\n")
        f.write(f"  (-) Trials Descartados (Artefatos): {artefatos} ({(artefatos/len(df_task)*100 if len(df_task) > 0 else 0):.2f}%)\n")
        f.write(f"  (=) Trials Válidos Pós-Filtro:       {trials_validos_total} ({(trials_validos_total/len(df_task)*100 if len(df_task) > 0 else 0):.2f}%)\n\n")
        
        f.write("MÉTRICAS COMPORTAMENTAIS:\n")
        f.write(f"  Erros de Comissão (Impulsividade Motora):           {c} / {n_nogo} ({(c/n_nogo*100 if n_nogo > 0 else 0):.2f}%)\n")
        f.write(f"  Erros de Omissão (Lapsos Atencionais):              {o} / {n_go_validos} ({(o/n_go_validos*100 if n_go_validos > 0 else 0):.2f}%)\n")
        f.write(f"  Respostas Antecipadas (Comportamento Automatizado): {artefatos} / {n_go_total} ({(artefatos/n_go_total*100 if n_go_total > 0 else 0):.2f}%)\n\n")
        
        f.write("MÉTRICAS DE TEMPO DE REAÇÃO (RT - TRIALS GO CORRETOS PÓS-FILTRO):\n")
        f.write(f"  Tempo de Reação Mínimo (Min):     {rt_minimo_texto}\n")
        f.write(f"  Tempo de Reação Máximo (Max):     {rt_maximo_texto}\n")
        f.write(f"  Tempo de Reação Médio (μ):        {rt_medio_texto}\n")
        f.write(f"  Variabilidade do RT (σ):          {rt_variabilidade_texto}\n")
        f.write("-" * 60 + "\n")

    # ==========================================
    # 7. ORGANIZAÇÃO FINAL
    # ==========================================
    novo_nome_json = f"SART_DadosBrutos_{nome_final_paciente}.json"
    caminho_json_final = os.path.join(output_dir, novo_nome_json)
    
    # Executa a movimentação física do arquivo original para a pasta final
    shutil.move(input_file, caminho_json_final)
    print(f"    [OK] Arquivo original renomeado e movido para: {novo_nome_json}")

print("\n[SUCESSO] Processamento completo executado com sucesso.")