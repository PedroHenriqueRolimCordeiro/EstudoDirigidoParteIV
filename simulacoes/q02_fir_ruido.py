# Q2 - Filtro FIR passa-baixa para remoção de ruído branco

import numpy as np
from scipy.signal import firwin, lfilter, freqz
import matplotlib.pyplot as plt
import os

# Parâmetros
fs = 1000
T = 0.5
f0 = 30           # freq do sinal (Hz)
fc = 60           # corte do filtro (Hz)
ordem = 101
np.random.seed(42)

# Sinal limpo + ruído
t = np.arange(0, T, 1/fs)
sinal_limpo = np.sin(2 * np.pi * f0 * t)
ruido = 0.8 * np.random.randn(len(t))
sinal_ruidoso = sinal_limpo + ruido

# Filtro e filtragem
coefs = firwin(ordem, fc, fs=fs)
sinal_filtrado = lfilter(coefs, 1.0, sinal_ruidoso)

# Resposta em frequência
w, H = freqz(coefs, worN=2048, fs=fs)

# Calcula espectro de um sinal
def espectro(sinal, fs):
    N = len(sinal)
    freqs = np.fft.rfftfreq(N, 1/fs)
    magnitudes = 2 * np.abs(np.fft.rfft(sinal)) / N
    return freqs, magnitudes

freq_r, mag_r = espectro(sinal_ruidoso, fs)
freq_f, mag_f = espectro(sinal_filtrado, fs)

# Plots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Q2 – Filtro FIR Passa-Baixa para Remoção de Ruído", fontsize=14, fontweight="bold")

axes[0, 0].plot(t, sinal_ruidoso, color="steelblue", linewidth=0.5, alpha=0.7, label="Ruidoso")
axes[0, 0].plot(t, sinal_limpo, color="gray", linewidth=1.0, linestyle="--", label="Original")
axes[0, 0].set_title("Sinal com ruído branco")
axes[0, 0].set_xlabel("Tempo (s)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(t, sinal_filtrado, color="crimson", linewidth=1.0, label="Filtrado (FIR)")
axes[0, 1].plot(t, sinal_limpo, color="gray", linewidth=1.0, linestyle="--", label="Original")
axes[0, 1].set_title("Sinal após filtragem FIR")
axes[0, 1].set_xlabel("Tempo (s)")
axes[0, 1].set_ylabel("Amplitude")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].stem(freq_r, mag_r, linefmt="steelblue", markerfmt=".", basefmt="gray")
axes[1, 0].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[1, 0].set_title("Espectro do sinal ruidoso")
axes[1, 0].set_xlabel("Frequência (Hz)")
axes[1, 0].set_ylabel("Magnitude")
axes[1, 0].set_xlim(0, 200)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].stem(freq_f, mag_f, linefmt="crimson", markerfmt=".", basefmt="gray")
axes[1, 1].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[1, 1].set_title("Espectro do sinal filtrado")
axes[1, 1].set_xlabel("Frequência (Hz)")
axes[1, 1].set_ylabel("Magnitude")
axes[1, 1].set_xlim(0, 200)
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q02_fir_ruido.png", dpi=150, bbox_inches="tight")
plt.show()

# SNR antes e depois
snr_antes = 10 * np.log10(np.var(sinal_limpo) / np.var(ruido))
erro_filtrado = sinal_filtrado - sinal_limpo
snr_depois = 10 * np.log10(np.var(sinal_limpo) / np.var(erro_filtrado))

print("\n--- Discussão ---")
print(f"SNR antes da filtragem:  {snr_antes:.2f} dB")
print(f"SNR depois da filtragem: {snr_depois:.2f} dB")
print(f"Melhoria de SNR:         {snr_depois - snr_antes:.2f} dB")
print(f"\nO filtro FIR de ordem {ordem} com fc = {fc} Hz removeu efetivamente")
print(f"o ruído branco de alta frequência, preservando a senoide de {f0} Hz.")
