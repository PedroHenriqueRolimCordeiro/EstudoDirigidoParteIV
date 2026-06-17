# Discussão Técnica das Simulações (Q1 a Q10)

Este documento compila as discussões técnicas e conclusões extraídas a partir da execução de cada uma das simulações computacionais.

### Q1 – Filtro passa-baixa em sinal com duas senoides
O sinal original é composto por duas senoides: 5 Hz e 50 Hz. O filtro FIR passa-baixa de ordem 51 com frequência de corte ($f_c$) de 20 Hz atenua a componente de 50 Hz com eficácia, preservando intacta a componente de 5 Hz. Adicionalmente, observa-se o atraso de grupo constante, que é uma característica típica de filtros FIR com fase linear.

### Q2 – FIR passa-baixa para remoção de ruído
Ao aplicar um ruído branco a uma senoide de 30 Hz, a relação sinal-ruído (SNR) cai drasticamente. O filtro FIR de ordem 101 com $f_c$ = 60 Hz removeu efetivamente o ruído de alta frequência distribuído no espectro, elevando a SNR novamente e preservando a senoide fundamental.

### Q3 – IIR Butterworth para remoção de ruído
No mesmo cenário da Q2, o filtro IIR Butterworth atinge uma transição abrupta na banda de corte utilizando apenas 4 coeficientes (contra os 101 necessários no FIR). Porém, como a fase do IIR não é linear, o sinal filtrado sofre uma leve distorção de fase no domínio do tempo, o que demonstra o clássico compromisso entre custo computacional e linearidade.

### Q4 – Comparação FIR vs IIR
Mesmo possuindo a mesma frequência de corte ($f_c$ = 100 Hz), o IIR Butterworth de ordem 4 garante uma transição espectral mais "íngreme" que o FIR de ordem 51. No entanto, o gráfico de fase comprova a grande vantagem do FIR: sua fase é perfeitamente linear (uma reta), enquanto o IIR apresenta distorção não-linear forte na região próxima à banda de transição.

### Q5 – Polos e Zeros e Estabilidade
A teoria nos diz que um filtro IIR é BIBO-estável se, e somente se, todos os seus polos estiverem estritamente dentro do círculo unitário ($|p| < 1$). O diagrama de polos e zeros plotado na simulação valida isso visualmente: o filtro Butterworth manteve todos os polos na parte interna, enquanto o filtro instável proposital possui um polo em $z = 1.2$, que causaria divergência no sinal.

### Q6 – Resposta ao Impulso
A simulação comprova a nomenclatura dos filtros. O FIR (resposta finita) tem sua resposta $h[n]$ indo exatamente a zero após ultrapassar a sua ordem. O IIR (resposta infinita), devido à realimentação, possui uma resposta que decai de forma exponencial de maneira assintótica, mas matematicamente nunca atinge o zero absoluto.

### Q7 – Filtro Passa-Faixa
A partir de um sinal misturado com componentes em 50, 200 e 400 Hz, o filtro FIR passa-faixa desenhado para a banda de 150-250 Hz provou-se altamente seletivo, isolando perfeitamente a componente central (200 Hz). É um princípio base para demodulação de rádio e análise espectral em blocos.

### Q8 – Resposta de Fase Linear
Ao analisar o erro de linearidade na banda de passagem, comprova-se que o FIR simétrico apresenta erro praticamente nulo (fase reta), resultando em um atraso de grupo constante (todas as frequências demoram o mesmo tempo para passar pelo filtro). O IIR, por outro lado, sofreu erros significativos de linearidade, o que "espalharia" as frequências no tempo.

### Q9 – Atraso de Grupo (Butterworth, Chebyshev e Elíptico)
Avaliando as famílias IIR:
- **Elíptico:** Tem a transição mais dura/rápida possível, mas sofre com uma oscilação (ripple) brutal no atraso de grupo.
- **Butterworth:** Possui a transição mais suave, mas garante o atraso de grupo mais plano e constante possível.
- **Chebyshev:** Age como um intermediário entre os dois. Em aplicações onde a preservação temporal importa, o Butterworth se sobressai perante as outras topologias IIR.

### Q10 – Aplicação Prática (Sensor de Vibração)
Em ambientes de monitoramento industrial (máquinas rotativas), componentes fundamentais (60, 120 e 180 Hz) são frequentemente encobertas por ruídos mecânicos e da rede elétrica. A simulação mostra que tanto o FIR quanto o IIR Butterworth limparam efetivamente o sinal (elevando a SNR). A escolha real recairia no hardware: IIR se houver pouco processador disponível, ou FIR se for estritamente necessário não distorcer o "formato" dos picos de vibração para detectar falhas mecânicas sensíveis.
