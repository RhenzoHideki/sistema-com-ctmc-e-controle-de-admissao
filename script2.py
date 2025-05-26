import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Dados da Comparação Analítica vs Simulada
df = pd.DataFrame({
    'Estado': [
        '(0, 0)', '(0, 1)', '(0, 2)', '(0, 3)',
        '(1, 0)', '(1, 1)', '(1, 2)', '(1, 3)',
        '(2, 0)', '(2, 1)', '(2, 2)', '(2, 3)',
        '(3, 0)', '(3, 1)', '(3, 2)', '(4, 0)',
        '(4, 1)', '(5, 0)'
    ],
    'Analitico': [
        0.2831, 0.1699, 0.0510, 0.0102,
        0.1887, 0.1132, 0.0340, 0.0068,
        0.0629, 0.0377, 0.0113, 0.0023,
        0.0140, 0.0084, 0.0025, 0.0023,
        0.0014, 0.0003
    ],
    'Simulado': [
        0.2820, 0.1689, 0.0509, 0.0101,
        0.1890, 0.1140, 0.0339, 0.0067,
        0.0634, 0.0379, 0.0112, 0.0021,
        0.0146, 0.0085, 0.0027, 0.0023,
        0.0014, 0.0003
    ]
})

# Configuração do gráfico
x = np.arange(len(df))
width = 0.35

plt.figure(figsize=(12, 5))
plt.bar(x - width/2, df['Analitico'], width, label='Analítico')
plt.bar(x + width/2, df['Simulado'], width, label='Simulado')

plt.xticks(x, df['Estado'], rotation=45, ha='right')
plt.xlabel('Estados (i, j)')
plt.ylabel('Probabilidade Estacionária π')
plt.title('Comparação das distribuições estacionárias (Analítico vs Simulado)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
