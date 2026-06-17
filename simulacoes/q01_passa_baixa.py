# Q1 - Filtro passa-baixa em sinal com duas senoides

import numpy as np
from scipy.signal import firwin, lfilter, freqz
import matplotlib.pyplot as plt
import os

# Parâmetros
fs = 500          # taxa de amostragem (Hz)
T = 1.0           # duração (s)
f1 = 5            # freq da senoide 1 (Hz)
f2 = 50           # freq da senoide 2 (Hz)
fc = 20           # corte do filtro (Hz)
ordem = 51

# Sinal: soma de duas senoides
t = np.arange(0, T, 1/fs)
x1 = np.sin(2 * np.pi * f1 * t)
x2 = 0.5 * np.sin(2 * np.pi * f2 * t)
x = x1 + x2

# Filtro FIR passa-baixa
coefs = firwin(ordem, fc, fs=fs)
y = lfilter(coefs, 1.0, x)

# Resposta em frequência
w, H = freqz(coefs, worN=2048, fs=fs)

# Plots
fig, axes = plt.subplots(3, 1, figsize=(12, 9))
fig.suptitle("Q1 – Filtro FIR Passa-Baixa em Sinal com Duas Senoides", fontsize=14, fontweight="bold")

axes[0].plot(t, x, color="steelblue", linewidth=0.8)
axes[0].set_title("Sinal original: sen(5 Hz) + 0.5·sen(50 Hz)")
axes[0].set_xlabel("Tempo (s)")
axes[0].set_ylabel("Amplitude")
axes[0].grid(True, alpha=0.3)

atraso = (ordem - 1) // 2
axes[1].plot(t, x1, color="gray", linewidth=0.8, linestyle="--", label="5 Hz puro (referência)")
axes[1].plot(t, y, color="crimson", linewidth=1.0, label="Sinal filtrado")
axes[1].set_title("Sinal após filtragem passa-baixa (fc = 20 Hz)")
axes[1].set_xlabel("Tempo (s)")
axes[1].set_ylabel("Amplitude")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].plot(w, 20 * np.log10(np.abs(H) + 1e-12), color="darkgreen", linewidth=1.0)
axes[2].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[2].set_title("Resposta em frequência do filtro FIR")
axes[2].set_xlabel("Frequência (Hz)")
axes[2].set_ylabel("Magnitude (dB)")
axes[2].set_xlim(0, fs/2)
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q01_passa_baixa.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"O sinal original é composto por duas senoides: {f1} Hz e {f2} Hz.")
print(f"O filtro FIR passa-baixa de ordem {ordem} com fc = {fc} Hz atenua")
print(f"a componente de {f2} Hz, preservando a componente de {f1} Hz.")
print("Observa-se um atraso de grupo constante típico de filtros FIR com fase linear.")
