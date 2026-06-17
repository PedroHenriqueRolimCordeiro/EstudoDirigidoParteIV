# Q3 - Filtro IIR Butterworth para remoção de ruído
# Mesmo cenário da Q2, agora com Butterworth pra comparar

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import os

# Mesmos parâmetros da Q2
fs = 1000
T = 0.5
f0 = 30
fc = 60
ordem_iir = 4
np.random.seed(42)

# Mesmo sinal da Q2
t = np.arange(0, T, 1/fs)
sinal_limpo = np.sin(2 * np.pi * f0 * t)
ruido = 0.8 * np.random.randn(len(t))
sinal_ruidoso = sinal_limpo + ruido

# Filtro IIR Butterworth
b, a = butter(ordem_iir, fc, btype='low', fs=fs)
sinal_filtrado = lfilter(b, a, sinal_ruidoso)

# Resposta em frequência
w, H = freqz(b, a, worN=2048, fs=fs)

def espectro(sinal, fs):
    N = len(sinal)
    freqs = np.fft.rfftfreq(N, 1/fs)
    magnitudes = 2 * np.abs(np.fft.rfft(sinal)) / N
    return freqs, magnitudes

freq_r, mag_r = espectro(sinal_ruidoso, fs)
freq_f, mag_f = espectro(sinal_filtrado, fs)

# Plots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Q3 – Filtro IIR Butterworth para Remoção de Ruído", fontsize=14, fontweight="bold")

axes[0, 0].plot(t, sinal_ruidoso, color="steelblue", linewidth=0.5, alpha=0.7, label="Ruidoso")
axes[0, 0].plot(t, sinal_limpo, color="gray", linewidth=1.0, linestyle="--", label="Original")
axes[0, 0].set_title("Sinal com ruído branco")
axes[0, 0].set_xlabel("Tempo (s)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(t, sinal_filtrado, color="darkorange", linewidth=1.0, label="Filtrado (IIR Butterworth)")
axes[0, 1].plot(t, sinal_limpo, color="gray", linewidth=1.0, linestyle="--", label="Original")
axes[0, 1].set_title(f"Sinal após filtragem IIR Butterworth (ordem {ordem_iir})")
axes[0, 1].set_xlabel("Tempo (s)")
axes[0, 1].set_ylabel("Amplitude")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(w, 20 * np.log10(np.abs(H) + 1e-12), color="darkorange", linewidth=1.5)
axes[1, 0].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[1, 0].axhline(-3, color="gray", linestyle=":", alpha=0.5, label="-3 dB")
axes[1, 0].set_title("Resposta em frequência do filtro Butterworth")
axes[1, 0].set_xlabel("Frequência (Hz)")
axes[1, 0].set_ylabel("Magnitude (dB)")
axes[1, 0].set_xlim(0, 200)
axes[1, 0].set_ylim(-60, 5)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].stem(freq_f, mag_f, linefmt="darkorange", markerfmt=".", basefmt="gray")
axes[1, 1].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[1, 1].set_title("Espectro do sinal filtrado")
axes[1, 1].set_xlabel("Frequência (Hz)")
axes[1, 1].set_ylabel("Magnitude")
axes[1, 1].set_xlim(0, 200)
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q03_iir_butterworth.png", dpi=150, bbox_inches="tight")
plt.show()

# SNR
snr_antes = 10 * np.log10(np.var(sinal_limpo) / np.var(ruido))
erro_filtrado = sinal_filtrado - sinal_limpo
snr_depois = 10 * np.log10(np.var(sinal_limpo) / np.var(erro_filtrado))

print("\n--- Discussão ---")
print(f"SNR antes da filtragem:  {snr_antes:.2f} dB")
print(f"SNR depois da filtragem: {snr_depois:.2f} dB")
print(f"Melhoria de SNR:         {snr_depois - snr_antes:.2f} dB")
print(f"\nO filtro IIR Butterworth de ordem {ordem_iir} atingiu uma transição mais")
print(f"abrupta na banda de corte com apenas {ordem_iir} coeficientes, em contraste")
print("com a ordem 101 necessária no FIR da Q2. Porém, a fase não é linear,")
print("introduzindo distorção de fase no sinal filtrado.")
