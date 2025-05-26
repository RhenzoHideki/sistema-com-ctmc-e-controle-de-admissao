import numpy as np
import pandas as pd
import ace_tools_open as tools

# --- Parâmetros ---
# Chegadas (por minuto)
lambda1, lambda2 = 10, 15
# Serviços (por minuto)
mu1, mu2         = 15, 25
# Capacidade e reserva
C, R             = 5, 2
# Simulação
T_total          = 10_000  # minutos
warm_up          = 1_000   # minutos de aquecimento

# --- Estados válidos ---
states = [(n1, n2) 
          for n1 in range(C+1) 
          for n2 in range(C-R+1) 
          if n1 + n2 <= C]
states.sort()
n = len(states)
state_index = {s: i for i, s in enumerate(states)}

# --- 1. Matriz Infinitesimal Q (minutos) ---
Qm = np.zeros((n, n))
for i, (n1, n2) in enumerate(states):
    if (n1+1, n2) in states:
        Qm[i, states.index((n1+1, n2))] = lambda1
    if (n1, n2+1) in states:
        Qm[i, states.index((n1, n2+1))] = lambda2
    if n1 > 0:
        Qm[i, states.index((n1-1, n2))] = n1 * mu1
    if n2 > 0:
        Qm[i, states.index((n1, n2-1))] = n2 * mu2
    Qm[i, i] = -Qm[i].sum()

# --- 2. Solução Analítica ---
A = Qm.T.copy()
A[-1, :] = 1
b = np.zeros(n); b[-1] = 1
pi_analytical = np.linalg.solve(A, b)

# --- 3. Simulação via relógios concorrentes ---
sojourn = np.zeros(n)
t = 0.0
current = (0, 0)

while t < T_total:
    n1, n2 = current
    rates, trans = [], []
    # Chegadas e saídas
    if n1 + n2 < C:
        rates.append(lambda1); trans.append((n1+1, n2))
        if n2 < C - R:
            rates.append(lambda2); trans.append((n1, n2+1))
    if n1 > 0:
        rates.append(n1 * mu1); trans.append((n1-1, n2))
    if n2 > 0:
        rates.append(n2 * mu2); trans.append((n1, n2-1))
    total_rate = sum(rates)
    dt = np.random.exponential(1 / total_rate)
    if t >= warm_up:
        sojourn[state_index[current]] += dt
    choice = np.random.choice(len(trans), p=np.array(rates)/total_rate)
    current = trans[choice]
    t += dt

pi_sim = sojourn / sojourn.sum()

# --- 4. Comparação Analítica vs Simulada ---
df_compare = pd.DataFrame({
    'Estado': states,
    'π (analítica)': np.round(pi_analytical, 4),
    'π̂ (simulação)': np.round(pi_sim, 4)
})
tools.display_dataframe_to_user("Comparação Analítica vs Simulada", df_compare)

# --- 5. Indicadores de Desempenho ---

# Função para calcular indicadores dada uma distribuição pi
def performance_metrics(pi):
    # Probabilidade de bloqueio T1: estados com n1+n2 = C
    p_block1 = sum(pi[i] for i, (n1, n2) in enumerate(states) if n1 + n2 == C)
    # Probabilidade de bloqueio T2: n1+n2=C ou n2=C-R
    p_block2 = sum(pi[i] for i, (n1, n2) in enumerate(states) if (n1 + n2 == C or n2 == C - R))
    # Utilização média
    util = sum(pi[i] * (n1 + n2) for i, (n1, n2) in enumerate(states)) / C
    # Número médio de conexões por classe
    L1 = sum(pi[i] * n1 for i, (n1, n2) in enumerate(states))
    L2 = sum(pi[i] * n2 for i, (n1, n2) in enumerate(states))
    # Fração de tempo em capacidade máxima
    frac_max = sum(pi[i] for i, (n1, n2) in enumerate(states) if n1 + n2 == C)
    return p_block1, p_block2, util, L1, L2, frac_max

metrics_analytical = performance_metrics(pi_analytical)
metrics_sim = performance_metrics(pi_sim)

df_metrics = pd.DataFrame({
    'Indicador': [
        'Prob_bloqueio_classe_1',
        'Prob_bloqueio_classe_2',
        'Utilizacao_media',
        'Media_conexoes_classe_1',
        'Media_conexoes_classe_2',
        'Fracao_tempo_capacidade_maxima'
    ],
    'Valor Analítico': np.round(metrics_analytical, 4),
    'Valor Simulado': np.round(metrics_sim, 4)
})
tools.display_dataframe_to_user("Indicadores de Desempenho", df_metrics)