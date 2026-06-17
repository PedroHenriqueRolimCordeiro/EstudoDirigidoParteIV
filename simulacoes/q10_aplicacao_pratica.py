# Q10 - Aplicação prática: remoção de ruído em sensor de vibração

import numpy as np
from scipy.signal import firwin, butter, lfilter, freqz
import matplotlib.pyplot as plt
import os

fs = 4000          # taxa de amostragem (Hz)
T = 1.0
np.random.seed(42)

# Sinal de vibração: máquina rotativa com fundamental em 60 Hz e harmônicas
t = np.arange(0, T, 1/fs)
vibracao = 2.0 * np.sin(2 * np.pi * 60 * t)             # fundamental
vibracao += 0.8 * np.sin(2 * np.pi * 120 * t + np.pi/4)  # 2ª harmônica
vibracao += 0.3 * np.sin(2 * np.pi * 180 * t + np.pi/3)  # 3ª harmônica

# Ruído: gaussiano + interferência em 1500 Hz
ruido = 1.0 * np.random.randn(len(t))
ruido += 0.5 * np.sin(2 * np.pi * 1500 * t)

sinal_ruidoso = vibracao + ruido

# Filtros com fc = 300 Hz (acima das harmônicas, abaixo do ruído)
fc = 300

b_fir = firwin(101, fc, fs=fs)
y_fir = lfilter(b_fir, 1.0, sinal_ruidoso)

b_iir, a_iir = butter(4, fc, btype='low', fs=fs)
y_iir = lfilter(b_iir, a_iir, sinal_ruidoso)

# SNR
def snr_db(limpo, filtrado):
    erro = filtrado - limpo
    return 10 * np.log10(np.var(limpo) / (np.var(erro) + 1e-12))

snr_antes = snr_db(vibracao, sinal_ruidoso)
snr_fir = snr_db(vibracao, y_fir)
snr_iir = snr_db(vibracao, y_iir)

# Plots
fig, axes = plt.subplots(3, 1, figsize=(14, 10))
fig.suptitle("Q10 – Aplicação Prática: Remoção de Ruído em Sensor de Vibração",
             fontsize=14, fontweight="bold")

axes[0].plot(t, sinal_ruidoso, color="gray", linewidth=0.4, alpha=0.7, label="Ruidoso")
axes[0].plot(t, vibracao, color="steelblue", linewidth=1.0, label="Vibração real")
axes[0].set_title(f"Sinal do sensor (SNR = {snr_antes:.1f} dB)")
axes[0].set_xlabel("Tempo (s)"); axes[0].set_ylabel("Amplitude")
axes[0].legend(); axes[0].grid(True, alpha=0.3)

axes[1].plot(t, y_fir, color="crimson", linewidth=1.0, label="FIR filtrado")
axes[1].plot(t, vibracao, color="steelblue", linewidth=1.0, linestyle="--", alpha=0.5, label="Real")
axes[1].set_title(f"Após FIR passa-baixa (SNR = {snr_fir:.1f} dB)")
axes[1].set_xlabel("Tempo (s)"); axes[1].set_ylabel("Amplitude")
axes[1].legend(); axes[1].grid(True, alpha=0.3)

axes[2].plot(t, y_iir, color="darkorange", linewidth=1.0, label="IIR Butterworth filtrado")
axes[2].plot(t, vibracao, color="steelblue", linewidth=1.0, linestyle="--", alpha=0.5, label="Real")
axes[2].set_title(f"Após IIR Butterworth (SNR = {snr_iir:.1f} dB)")
axes[2].set_xlabel("Tempo (s)"); axes[2].set_ylabel("Amplitude")
axes[2].legend(); axes[2].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q10_aplicacao_pratica.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"SNR antes da filtragem: {snr_antes:.2f} dB")
print(f"SNR após FIR (ordem 101): {snr_fir:.2f} dB")
print(f"SNR após IIR Butterworth (ordem 4): {snr_iir:.2f} dB")
print("\nEm monitoramento de vibração industrial, sensores captam componentes")
print("de vibração (60, 120, 180 Hz) junto com ruído elétrico e mecânico.")
print("Ambos os filtros removem efetivamente o ruído, com o IIR usando")
print("menos coeficientes e o FIR garantindo preservação da forma de onda.")
