# Estudo Dirigido – Parte 4: Filtros Digitais

**Disciplina:** Processamento Digital de Sinais (PDS)  
**Instituição:** IFPB  
**Semestre:** 2026.1

---

## 📖 Descrição

Este repositório contém a resolução do Estudo Dirigido – Parte 4 da disciplina de Processamento Digital de Sinais. O tema central é **Filtros Digitais**, abordando conceitos teóricos, simulações computacionais e uma aplicação prática baseada em aprendizado por problemas (PBL).

---

## 📂 Estrutura do Repositório

```
EstudoDirigido4/
├── teoria/
│   └── resumo_teorico.md          # Resumo teórico sobre filtros digitais
├── simulacoes/
│   ├── q01_passa_baixa.py         # Q1  – Filtro passa-baixa em sinal com senoides
│   ├── q02_fir_ruido.py           # Q2  – FIR passa-baixa para remoção de ruído
│   ├── q03_iir_butterworth.py     # Q3  – IIR Butterworth para remoção de ruído
│   ├── q04_fir_vs_iir.py          # Q4  – Comparação FIR vs IIR
│   ├── q05_polos_zeros.py         # Q5  – Polos e zeros de filtro IIR
│   ├── q06_resposta_impulso.py    # Q6  – Resposta ao impulso FIR vs IIR
│   ├── q07_passa_faixa.py         # Q7  – Filtro passa-faixa
│   ├── q08_resposta_fase.py       # Q8  – Resposta de fase FIR vs IIR
│   ├── q09_atraso_grupo.py        # Q9  – Atraso de grupo
│   └── q10_aplicacao_pratica.py   # Q10 – Aplicação prática (remoção de ruído)
├── resultados/
│   └── (gráficos e figuras gerados pelas simulações)
├── README.md
└── requirements.txt
```

---

## 🔧 Requisitos

- Python 3.10+
- Bibliotecas: `numpy`, `scipy`, `matplotlib`

### Instalação das dependências

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

Para rodar uma simulação individual:

```bash
python simulacoes/q01_passa_baixa.py
```

Para rodar todas as simulações de uma vez:

```bash
for script in simulacoes/q*.py; do python "$script"; done
```

Os gráficos gerados serão salvos automaticamente na pasta `resultados/`.

---

## 📝 Conteúdo

### 1. Resumo Teórico (`teoria/`)

Resumo de 1-2 páginas cobrindo:
- Tipos de filtros digitais: **FIR** (Resposta ao Impulso Finita) vs **IIR** (Resposta ao Impulso Infinita)
- Resposta em frequência e resposta de fase
- Atraso de grupo e fase linear
- Estabilidade de filtros digitais
- Aplicações práticas em processamento de sinais

### 2. Simulações (`simulacoes/`)

| Questão | Tema | Descrição |
|:-------:|------|-----------|
| Q1 | Passa-baixa | Sinal com duas senoides (5 Hz e 50 Hz) → filtro FIR passa-baixa |
| Q2 | FIR + ruído | Sinal senoidal + ruído branco → filtro FIR passa-baixa |
| Q3 | IIR Butterworth | Mesmo cenário da Q2 com filtro IIR Butterworth |
| Q4 | FIR vs IIR | Comparação de respostas em frequência com mesma fc |
| Q5 | Polos e zeros | Diagrama de polos/zeros de filtro IIR → estabilidade |
| Q6 | Resposta ao impulso | Comparação de resposta ao impulso FIR (finita) vs IIR (infinita) |
| Q7 | Passa-faixa | Filtro para selecionar frequência específica de um sinal misto |
| Q8 | Resposta de fase | Fase linear (FIR) vs não-linear (IIR) |
| Q9 | Atraso de grupo | Atraso de grupo de filtros Butterworth, Chebyshev e Elíptico |
| Q10 | Aplicação prática | Remoção de ruído em contexto real (áudio, sensores ou vibrações) |

### 3. Problema PBL

Projeto de filtros para um **sistema de monitoramento agrícola**:
- Sensores de temperatura, umidade e pH do solo
- Remoção de ruído sem perder informações relevantes
- Justificativa técnica da escolha de filtro e parâmetros

---

## 📊 Resultados

Os gráficos e figuras gerados pelas simulações são salvos na pasta `resultados/`. Cada simulação produz visualizações que incluem:

- Sinais no domínio do tempo (original, ruidoso, filtrado)
- Respostas em frequência (magnitude e fase)
- Diagramas de polos e zeros
- Comparações entre filtros

---

## 📚 Referências

- Oppenheim, A. V., & Schafer, R. W. *Discrete-Time Signal Processing*. Pearson.
- Haykin, S., & Van Veen, B. *Signals and Systems*. Wiley.
- Documentação SciPy: [scipy.signal](https://docs.scipy.org/doc/scipy/reference/signal.html)
