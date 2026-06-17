# Q7 - Filtro passa-faixa pra isolar uma frequência de um sinal misto

import numpy as np
from scipy.signal import firwin, lfilter, freqz
import matplotlib.pyplot as plt
import os

# Parâmetros
fs = 2000
T = 0.5
f1, f2, f3 = 50, 200, 400     # 3 componentes de frequência
fl, fh = 150, 250              # banda do filtro
ordem = 101

# Sinal composto
t = np.arange(0, T, 1/fs)
x1 = np.sin(2 * np.pi * f1 * t)
x2 = np.sin(2 * np.pi * f2 * t)
x3 = 0.7 * np.sin(2 * np.pi * f3 * t)
x = x1 + x2 + x3

# Filtro passa-faixa e filtragem
coefs = firwin(ordem, [fl, fh], pass_zero=False, fs=fs)
y = lfilter(coefs, 1.0, x)
w, H = freqz(coefs, worN=4096, fs=fs)

def espectro(sinal, fs):
    N = len(sinal)
    freqs = np.fft.rfftfreq(N, 1/fs)
    mags = 2 * np.abs(np.fft.rfft(sinal)) / N
    return freqs, mags

freq_orig, mag_orig = espectro(x, fs)
freq_filt, mag_filt = espectro(y, fs)

# Plots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Q7 – Filtro Passa-Faixa: Seleção de Frequência", fontsize=14, fontweight="bold")

axes[0,0].plot(t, x, color="steelblue", linewidth=0.6)
axes[0,0].set_title(f"Sinal original: {f1}+{f2}+{f3} Hz")
axes[0,0].set_xlabel("Tempo (s)"); axes[0,0].set_ylabel("Amplitude"); axes[0,0].grid(True, alpha=0.3)

axes[0,1].plot(t, y, color="crimson", linewidth=1.0, label="Filtrado")
axes[0,1].plot(t, x2, color="gray", linestyle="--", label=f"{f2} Hz ref.")
axes[0,1].set_title(f"Filtrado: apenas {f2} Hz")
axes[0,1].set_xlabel("Tempo (s)"); axes[0,1].set_ylabel("Amplitude"); axes[0,1].legend(); axes[0,1].grid(True, alpha=0.3)

axes[1,0].stem(freq_orig, mag_orig, linefmt="steelblue", markerfmt=".", basefmt="gray")
axes[1,0].axvspan(fl, fh, alpha=0.15, color="green", label=f"Banda: {fl}-{fh} Hz")
axes[1,0].set_title("Espectro original"); axes[1,0].set_xlabel("Frequência (Hz)")
axes[1,0].set_ylabel("Magnitude"); axes[1,0].set_xlim(0, 600); axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)

axes[1,1].plot(w, 20*np.log10(np.abs(H)+1e-12), color="darkgreen", linewidth=1.5)
axes[1,1].axvspan(fl, fh, alpha=0.15, color="green", label=f"Banda: {fl}-{fh} Hz")
axes[1,1].set_title("Resposta do filtro passa-faixa"); axes[1,1].set_xlabel("Frequência (Hz)")
axes[1,1].set_ylabel("Magnitude (dB)"); axes[1,1].set_xlim(0, 600); axes[1,1].set_ylim(-80, 5)
axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q07_passa_faixa.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"O filtro FIR passa-faixa ({fl}-{fh} Hz) isolou a componente de {f2} Hz.")
print("Filtros passa-faixa são essenciais em aplicações como demodulação e análise espectral.")
