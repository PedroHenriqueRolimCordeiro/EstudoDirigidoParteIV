# Problema PBL – Sistema de Monitoramento Agrícola

## 1. Contextualização do Problema

Uma fazenda de agricultura de precisão utiliza uma rede de sensores para monitorar, em tempo real, três variáveis ambientais críticas para o manejo do solo:

- **Temperatura do solo** (°C)
- **Umidade do solo** (%)
- **pH do solo**

Os sensores realizam amostragem a **10 amostras por minuto** (fs = 10/60 Hz ≈ 0,167 Hz), operando continuamente ao longo de **24 horas**. No entanto, os sinais adquiridos estão contaminados por diversas fontes de ruído:

| Sensor | Tipo de Ruído Predominante |
|--------|---------------------------|
| Temperatura (termopar) | Ruído gaussiano + interferência periódica da rede elétrica |
| Umidade (capacitivo) | Ruído gaussiano de amplitude elevada |
| pH (eletroquímico) | Ruído gaussiano + **spikes impulsivos** esporádicos |

O desafio é **projetar filtros digitais adequados para cada variável**, removendo o ruído sem perder informações relevantes sobre mudanças reais nas condições do solo — como o ciclo diurno de temperatura, os picos de irrigação na umidade e a correção gradual do pH.

---

## 2. Modelagem dos Sinais

### 2.1 Temperatura

O sinal real de temperatura foi modelado como um ciclo diurno senoidal com amplitude de 8°C em torno de 22°C, acrescido de variações menores causadas por nuvens e irrigação:

$$T_{real}(t) = 22 + 8 \cdot \sin\!\left(\frac{2\pi t}{24} - \frac{\pi}{2}\right) + 0{,}5 \cdot \sin\!\left(\frac{2\pi t}{120\text{ min}}\right)$$

O ruído adicionado consiste em componente gaussiana ($\sigma = 0{,}8$ °C) e interferência periódica de 2,5 ciclos/hora.

### 2.2 Umidade do Solo

O sinal de umidade parte de uma base de 60% e inclui dois eventos de irrigação (às 6h e 18h), modelados como exponenciais decrescentes com constante de tempo de 180 minutos, além de um ciclo de evapotranspiração diurno:

$$U_{real}(t) = 60 + \sum_{i} 15 \cdot e^{-(t - t_i)/180} - 5 \cdot \max\!\left(0,\; \sin\!\left(\frac{2\pi t}{24} - \frac{\pi}{6}\right)\right)$$

O ruído é gaussiano com $\sigma = 2{,}0\%$ mais uma interferência periódica.

### 2.3 pH do Solo

O pH apresenta uma deriva lenta modelando a correção por calcário, de 6,5 até ~6,8 ao longo de 24h:

$$pH_{real}(t) = 6{,}5 + 0{,}3 \cdot (1 - e^{-t/12}) + 0{,}1 \cdot \sin\!\left(\frac{2\pi t}{12}\right)$$

O ruído inclui componente gaussiana ($\sigma = 0{,}15$) e **30 spikes impulsivos** aleatórios com amplitude entre 0,5 e 1,5 unidades de pH — característicos de sensores eletroquímicos com mau contato intermitente.

---

## 3. Projeto dos Filtros

### 3.1 Temperatura → Filtro FIR Passa-Baixa

| Parâmetro | Valor |
|-----------|-------|
| Tipo | FIR (janela de Hamming) |
| Ordem | 201 |
| Frequência de corte | 0,01 Hz (10 mHz) |

**Justificativa:** As variações reais de temperatura são extremamente lentas (ciclo diurno de 24h). Um filtro FIR foi escolhido por garantir **fase linear**, o que preserva a temporalidade exata das mudanças — fundamental para correlacionar picos de temperatura com horários do dia. A ordem elevada (201) é necessária para obter uma transição suficientemente estreita na baixa frequência de corte, mas é viável computacionalmente dada a baixa taxa de amostragem.

### 3.2 Umidade → Filtro IIR Butterworth Passa-Baixa

| Parâmetro | Valor |
|-----------|-------|
| Tipo | IIR Butterworth |
| Ordem | 3 |
| Frequência de corte | 0,008 Hz (8 mHz) |

**Justificativa:** As mudanças de umidade são graduais (irrigação e evapotranspiração), e o interesse principal é no **valor estacionário** da umidade, não na forma exata da transição. A distorção de fase do IIR é, portanto, aceitável. A grande vantagem é a **eficiência computacional**: apenas 3 coeficientes de realimentação são necessários, tornando este filtro ideal para implementação em **sistemas embarcados** de baixo custo tipicamente usados em fazendas.

### 3.3 pH → Filtro de Mediana + FIR Passa-Baixa

| Parâmetro | Valor |
|-----------|-------|
| Tipo | Mediana (janela=21) + FIR passa-baixa |
| Ordem FIR | 151 |
| Frequência de corte | 0,005 Hz (5 mHz) |

**Justificativa:** O sensor de pH sofre com **ruído impulsivo** (spikes), que filtros lineares (FIR e IIR) não conseguem remover adequadamente — eles apenas "borram" os spikes, espalhando a perturbação no tempo. A abordagem em duas etapas resolve isso:

1. **Filtro de mediana** (não-linear): remove spikes impulsivos de forma eficaz, pois a mediana é robusta a outliers. A janela de 21 amostras (~2 min) é ampla o suficiente para cobrir spikes isolados sem suavizar excessivamente o sinal.
2. **Filtro FIR passa-baixa**: suaviza o ruído gaussiano residual após a remoção dos spikes, com fase linear para preservar a temporalidade da deriva do pH.

---

## 4. Resultados

### 4.1 Métricas de Qualidade

| Variável | SNR antes | SNR depois | RMSE antes | RMSE depois | Melhoria SNR |
|----------|:---------:|:----------:|:----------:|:-----------:|:------------:|
| Temperatura | 16,51 dB | 21,56 dB | 0,8337 °C | 0,4663 °C | **+5,05 dB** |
| Umidade | 5,59 dB | 11,66 dB | 2,1153 % | 1,0523 % | **+6,07 dB** |
| pH | −6,38 dB | 6,40 dB | 0,1579 | 0,0363 | **+12,78 dB** |

> **Nota:** O pH obteve a maior melhoria (+12,78 dB) justamente por ser o sensor com pior SNR inicial (−6,38 dB, dominado por spikes), demonstrando a eficácia da abordagem mediana + FIR para ruído impulsivo.

### 4.2 Gráficos

Os resultados visuais estão disponíveis em:

- `resultados/pbl_sinais_temporais.png` — Comparação dos sinais ruidosos e filtrados para as 3 variáveis
- `resultados/pbl_respostas_frequencia.png` — Respostas em frequência dos 3 filtros projetados

---

## 5. Conclusão

Os filtros projetados para o sistema de monitoramento agrícola foram eficazes na remoção de ruído dos três sensores, preservando as tendências e variações reais das grandezas monitoradas. As principais conclusões são:

1. **A escolha do filtro deve ser guiada pela natureza do ruído e da aplicação.** Não existe um filtro "universal" — cada variável demandou uma abordagem diferente.

2. **Filtros FIR** são ideais quando a **fase linear** é um requisito (temperatura), garantindo que a temporalidade das mudanças seja preservada sem distorção.

3. **Filtros IIR** são preferíveis em **sistemas com restrição computacional** (umidade em embarcados), onde a baixa ordem compensa a distorção de fase.

4. **Ruído impulsivo exige tratamento não-linear.** O filtro de mediana demonstrou ser indispensável para o sensor de pH, onde filtros lineares falhariam em remover os spikes sem borrar o sinal.

5. As métricas quantitativas (SNR e RMSE) confirmam melhorias significativas em todos os cenários, com destaque para o pH onde a SNR passou de −6,38 dB para +6,40 dB — uma melhoria de quase 13 dB.

---

## Referências

- OPPENHEIM, A. V.; SCHAFER, R. W. **Discrete-Time Signal Processing**. 3. ed. Pearson, 2009.
- HAYKIN, S.; VAN VEEN, B. **Signals and Systems**. 2. ed. Wiley, 2002.
- Documentação SciPy: [scipy.signal](https://docs.scipy.org/doc/scipy/reference/signal.html)
