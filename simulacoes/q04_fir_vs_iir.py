# Q4 - Comparação FIR vs IIR com mesma frequência de corte

import numpy as np
from scipy.signal import firwin, butter, freqz
import matplotlib.pyplot as plt
import os

# Parâmetros
fs = 1000
fc = 100
ordem_fir = 51
ordem_iir = 4

# Projetando os dois filtros
b_fir = firwin(ordem_fir, fc, fs=fs)
b_iir, a_iir = butter(ordem_iir, fc, btype='low', fs=fs)

# Respostas em frequência
w_fir, H_fir = freqz(b_fir, worN=2048, fs=fs)
w_iir, H_iir = freqz(b_iir, a_iir, worN=2048, fs=fs)

# Plots
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle("Q4 – Comparação FIR vs IIR (mesma fc)", fontsize=14, fontweight="bold")

# Magnitude
axes[0].plot(w_fir, 20 * np.log10(np.abs(H_fir) + 1e-12),
             color="steelblue", linewidth=1.5, label=f"FIR (ordem {ordem_fir})")
axes[0].plot(w_iir, 20 * np.log10(np.abs(H_iir) + 1e-12),
             color="darkorange", linewidth=1.5, label=f"IIR Butterworth (ordem {ordem_iir})")
axes[0].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[0].axhline(-3, color="gray", linestyle=":", alpha=0.5, label="-3 dB")
axes[0].set_title("Resposta em magnitude")
axes[0].set_xlabel("Frequência (Hz)")
axes[0].set_ylabel("Magnitude (dB)")
axes[0].set_xlim(0, fs/2)
axes[0].set_ylim(-80, 5)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Fase
fase_fir = np.unwrap(np.angle(H_fir))
fase_iir = np.unwrap(np.angle(H_iir))

axes[1].plot(w_fir, np.degrees(fase_fir),
             color="steelblue", linewidth=1.5, label=f"FIR (ordem {ordem_fir})")
axes[1].plot(w_iir, np.degrees(fase_iir),
             color="darkorange", linewidth=1.5, label=f"IIR Butterworth (ordem {ordem_iir})")
axes[1].axvline(fc, color="red", linestyle="--", alpha=0.7, label=f"fc = {fc} Hz")
axes[1].set_title("Resposta de fase")
axes[1].set_xlabel("Frequência (Hz)")
axes[1].set_ylabel("Fase (graus)")
axes[1].set_xlim(0, fs/2)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q04_fir_vs_iir.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print("Ambos os filtros possuem a mesma frequência de corte (fc = 100 Hz).")
print(f"O IIR Butterworth de ordem {ordem_iir} apresenta uma transição mais abrupta")
print(f"que o FIR de ordem {ordem_fir}, utilizando muito menos coeficientes.")
print("Entretanto, o FIR possui fase perfeitamente linear (reta), enquanto")
print("o IIR apresenta fase não-linear, especialmente próximo à frequência de corte.")
print("Essa distorção de fase do IIR pode ser problemática em aplicações onde a")
print("preservação da forma de onda temporal é importante.")
