#import "@preview/klaro-ifsc-sj:0.1.0": report
#import "@preview/codelst:2.0.2": sourcecode
#set text(font: "Arial", size: 12pt)
#set text(lang: "pt")
#set page(
  footer: "Engenharia de Telecomunicações - IFSC-SJ",
)

#show: doc => report(
  title: "Relatório Técnico: Avaliação Analítica e Simulada de um Sistema com CTMC e Controle de Admissão",
  subtitle: "Avaliação de desempenho de sistemas (ASD029009)",
  authors: ("Matheus Pires Salazar","Rhenzo Hideki Silva Kajikawa",),
  date: "22 de maio de 2025",
  doc,
)

= Introdução
Este relatório apresenta a modelagem, simulação e análise de desempenho de um sistema com duas classes de tráfego (prioritário e não prioritário) sob controle de admissão com base em Cadeias de Markov em Tempo Contínuo (CTMC). O sistema admite sessões de tráfego que ocupam recursos limitados, respeitando uma política de reserva mínima para a classe prioritária.


= Especificações do Sistema
- Capacidade total (C): 5 unidades
 
- Reserva mínima para tráfego prioritário (R): 2 unidades
 
- Classe 1 (prioritária):
 
  - Taxa de chegada: λ₁ = 10 requisições/minuto
 
  - Taxa de serviço: μ₁ = 15 requisições/minuto
 
- Classe 2 (não prioritária):
 
  - Taxa de chegada: λ₂ = 15 requisições/minuto
 
  - Taxa de serviço: μ₂ = 25 requisições/minuto
 
- Restrições:
 
  - O número total de sessões ativas (classe 1 + classe 2) não pode exceder 5.
 
  - O número de sessões da classe 2 está limitado a no máximo 3 para garantir a reserva para a classe 1.

= Metodologia
== Metodologia Analítica
O sistema foi modelado como um CTMC, onde os estados representado pelo par $(n_1,n_2)$, indicando o número de sessões ativas da classe 1 e classe 2, respectivamente. A matriz infinitesimal $Q$ foi construída com base nas taxas de chegada e saida. A distribui;áo estacionária $pi$ foi obtida resolvendo o sistema linear $pi dot Q = 0$, com a confição de normalização $sum pi_i = 1$.

== Metodologia Simulada
Para validar o modelo analítico, foi realizada uma simulação estocástica com relógios exponenciais para cada transição possível. A simulação foi executada por 10.000 minutos, desprezando os primeiros 1.000 minutos como período de aquecimento. A distribuição empírica $pi'$ for obtida a partr do tempo de permanência em cada estado.

#pagebreak()
= Resultados
== Tabela Matriz Infinitesimal
#let q = csv("matriz_infinitesimal_Q_truncada.csv")
#table(
  columns: 19,
  inset: 5pt,

  align: center,
  ..q.flatten()
)

== Comparação da Distribuição Estacionária

#let tabela = csv("tabela.csv")

#table(
  columns: 3,
  ..tabela.flatten()
)
#figure(
  image("Figure_3.png",  width: 120%
),
  caption: "Comparação entre a distribuição estacionária analítica e a empírica obtida pela simulação.",
)
#pagebreak()
== Indicadores de Desempenho
#let tabela2 = csv("tabela2.csv")
#table(
  columns: 3,
  ..tabela2.flatten()
)

= Análise de Resultados
- Coerência entre métodos: Os resultados da simulação apresentaram excelente concordância com os valores obtidos analiticamente, validando tanto a modelagem quanto a implementação da simulação.

- Bloqueio: A probabilidade de bloqueio da classe 1 (prioritária) é inferior a 1%, o que atende a requisitos típicos de QoS. A classe 2 possui maior probabilidade de bloqueio (cerca de 2,35%), em razão da reserva mínima para a classe 1.

- Utilização: A utilização média do sistema gira em torno de 25% da capacidade total, o que sugere que há folga na infraestrutura ou que os parâmetros de chegada/serviço estão ajustados para garantir alta disponibilidade.

- Capacidade máxima: O sistema opera em sua capacidade total apenas cerca de 0,65% do tempo.

= Conclusão
O sistema proposto foi modelado e simulado com sucesso, e os resultados obtidos demonstram a eficiência do controle de admissão com reserva. A modelagem CTMC permite uma análise precisa, enquanto a simulação por relógios concorrentes confirma os resultados de forma empírica. A baixa probabilidade de bloqueio para a classe 1 confirma que os parâmetros de projeto são adequados para priorizar tráfego crítico.

