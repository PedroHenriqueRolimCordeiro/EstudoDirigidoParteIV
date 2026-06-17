# Resumo Teórico: Filtros Digitais

## 1. Introdução

Filtros digitais são sistemas discretos no tempo que modificam seletivamente as características espectrais de um sinal. Matematicamente, um filtro digital é descrito por uma equação de diferenças linear com coeficientes constantes:

$$y[n] = \sum_{k=0}^{M} b_k \, x[n-k] \;-\; \sum_{k=1}^{N} a_k \, y[n-k]$$

onde $b_k$ são os coeficientes *feedforward*, $a_k$ são os coeficientes de realimentação (*feedback*), $x[n]$ é a entrada e $y[n]$ é a saída. A presença ou ausência dos coeficientes $a_k$ define a classificação fundamental entre os dois grandes tipos de filtros digitais.

## 2. Filtros FIR vs. IIR

### 2.1 Filtros FIR (Resposta ao Impulso Finita)

Nos filtros FIR, todos os coeficientes $a_k = 0$, de modo que a saída depende exclusivamente de amostras presentes e passadas da entrada:

$$y[n] = \sum_{k=0}^{M} b_k \, x[n-k]$$

A resposta ao impulso $h[n]$ possui duração finita — isto é, $h[n] = 0$ para $n > M$ — e coincide com os próprios coeficientes $b_k$. Como consequência direta da ausência de realimentação, filtros FIR são **sempre estáveis**, pois todos os seus polos estão localizados na origem do plano $z$. Além disso, quando os coeficientes apresentam simetria ($b_k = b_{M-k}$) ou antissimetria ($b_k = -b_{M-k}$), o filtro exibe **fase linear**, o que garante que todas as componentes de frequência sofrem o mesmo atraso temporal. Essa propriedade é essencial em aplicações onde a preservação da forma de onda é crítica, como em sistemas de áudio e comunicações.

A principal desvantagem é que, para obter transições abruptas na resposta em frequência, são necessárias ordens elevadas (muitos coeficientes), o que aumenta o custo computacional.

### 2.2 Filtros IIR (Resposta ao Impulso Infinita)

Nos filtros IIR, os coeficientes $a_k \neq 0$ introduzem realimentação, fazendo com que a resposta ao impulso tenha duração teoricamente infinita. Isso permite obter respostas em frequência com transições muito mais acentuadas utilizando ordens significativamente menores do que filtros FIR equivalentes. As famílias clássicas de projeto incluem:

- **Butterworth:** resposta maximamente plana na banda de passagem, sem *ripple*.
- **Chebyshev Tipo I:** *ripple* controlado na banda de passagem; transição mais abrupta.
- **Chebyshev Tipo II:** *ripple* na banda de rejeição; banda de passagem plana.
- **Elíptico (Cauer):** *ripple* em ambas as bandas; transição mais estreita possível para uma dada ordem.

A desvantagem central é que filtros IIR **não garantem fase linear** e podem ser **instáveis** se os polos da função de transferência estiverem fora do círculo unitário no plano $z$.

### 2.3 Comparativo

| Característica        | FIR                          | IIR                              |
|-----------------------|------------------------------|----------------------------------|
| Resposta ao impulso   | Finita                       | Infinita                         |
| Fase linear           | Garantida (com simetria)     | Não garantida                    |
| Estabilidade          | Sempre estável               | Condicionada (polos em $|z|<1$)  |
| Ordem necessária      | Alta (para transições abruptas) | Baixa                         |
| Custo computacional   | Maior                        | Menor                            |
| Projeto               | Janelamento, Parks-McClellan | Transformação bilinear           |

## 3. Resposta em Frequência e Resposta de Fase

A função de transferência de um filtro digital no domínio $z$ é:

$$H(z) = \frac{\sum_{k=0}^{M} b_k \, z^{-k}}{1 + \sum_{k=1}^{N} a_k \, z^{-k}}$$

Avaliando $H(z)$ sobre o círculo unitário ($z = e^{j\omega}$), obtém-se a **resposta em frequência** $H(e^{j\omega})$, que pode ser decomposta em:

- **Resposta em magnitude:** $|H(e^{j\omega})|$ — determina a atenuação ou ganho para cada frequência.
- **Resposta de fase:** $\angle H(e^{j\omega})$ — determina o deslocamento de fase imposto a cada componente frequencial.

Um filtro com **fase linear** satisfaz $\angle H(e^{j\omega}) = -\alpha\omega$, onde $\alpha$ é uma constante. Isso significa que o atraso é idêntico para todas as frequências, preservando a forma temporal do sinal.

## 4. Atraso de Grupo

O **atraso de grupo** $\tau(\omega)$ é definido como a derivada negativa da fase em relação à frequência:

$$\tau(\omega) = -\frac{d\phi(\omega)}{d\omega}$$

Para filtros com fase linear, $\tau(\omega)$ é constante — cada componente de frequência sofre o mesmo atraso. Em filtros IIR, o atraso de grupo tipicamente varia com a frequência, especialmente próximo às frequências de corte, o que pode causar distorção na forma de onda do sinal. Filtros elípticos, por exemplo, apresentam variações mais acentuadas no atraso de grupo em comparação com filtros Butterworth.

## 5. Estabilidade

Um filtro digital é **BIBO-estável** (Bounded-Input, Bounded-Output) se e somente se toda entrada limitada produz uma saída limitada. Para filtros IIR, a condição necessária e suficiente é que **todos os polos** da função de transferência $H(z)$ estejam **estritamente dentro do círculo unitário** ($|p_k| < 1$ para todo polo $p_k$). 

Para filtros FIR, a estabilidade é garantida de forma incondicional, pois a função de transferência possui apenas zeros (todos os polos estão na origem).

A análise de estabilidade pode ser realizada visualmente por meio do **diagrama de polos e zeros** no plano $z$, onde se verifica se todos os polos (×) estão contidos na região $|z| < 1$.

## 6. Aplicações

Filtros digitais são ferramentas indispensáveis em diversas áreas:

- **Processamento de áudio:** equalização, remoção de ruído, efeitos sonoros.
- **Telecomunicações:** filtragem de canais, modulação/demodulação, cancelamento de eco.
- **Instrumentação e sensores:** suavização de leituras ruidosas em sistemas de aquisição de dados.
- **Processamento de imagens:** filtragem espacial para detecção de bordas e suavização.
- **Sistemas biomédicos:** filtragem de sinais de ECG e EEG para remoção de artefatos.
- **Agricultura de precisão:** monitoramento de variáveis ambientais (temperatura, umidade, pH) com remoção de ruído de sensores em tempo real.

## Referências

- OPPENHEIM, A. V.; SCHAFER, R. W. **Discrete-Time Signal Processing**. 3. ed. Pearson, 2009.
- HAYKIN, S.; VAN VEEN, B. **Signals and Systems**. 2. ed. Wiley, 2002.
- PROAKIS, J. G.; MANOLAKIS, D. G. **Digital Signal Processing: Principles, Algorithms, and Applications**. 4. ed. Pearson, 2006.
