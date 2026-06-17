# Q8 - Resposta de fase: fase linear (FIR) vs não-linear (IIR)

import numpy as np
from scipy.signal import firwin, butter, freqz
import matplotlib.pyplot as plt
import os

fs = 1000
fc = 100
ordem_fir = 51
ordem_iir = 4

# Filtros
b_fir = firwin(ordem_fir, fc, fs=fs)
b_iir, a_iir = butter(ordem_iir, fc, btype='low', fs=fs)

# Respostas em frequência
w_fir, H_fir = freqz(b_fir, worN=2048, fs=fs)
w_iir, H_iir = freqz(b_iir, a_iir, worN=2048, fs=fs)

fase_fir = np.unwrap(np.angle(H_fir))
fase_iir = np.unwrap(np.angle(H_iir))

# Checa linearidade na banda de passagem (até fc)
mask_bp = w_fir <= fc
if len(w_fir[mask_bp]) > 2:
    coefs_fit = np.polyfit(w_fir[mask_bp], fase_fir[mask_bp], 1)
    fase_linear_ideal = np.polyval(coefs_fit, w_fir)
    erro_lin_fir = fase_fir[mask_bp] - np.polyval(coefs_fit, w_fir[mask_bp])
    coefs_fit_iir = np.polyfit(w_iir[mask_bp], fase_iir[mask_bp], 1)
    erro_lin_iir = fase_iir[mask_bp] - np.polyval(coefs_fit_iir, w_iir[mask_bp])

# Plots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Q8 – Resposta de Fase: FIR vs IIR", fontsize=14, fontweight="bold")

axes[0,0].plot(w_fir, np.degrees(fase_fir), color="steelblue", linewidth=1.5)
axes[0,0].plot(w_fir, np.degrees(fase_linear_ideal), color="red", linestyle="--", linewidth=1, alpha=0.7, label="Reta ideal")
axes[0,0].axvline(fc, color="gray", linestyle=":", alpha=0.5)
axes[0,0].set_title(f"Fase do FIR (ordem {ordem_fir}) – LINEAR")
axes[0,0].set_xlabel("Frequência (Hz)"); axes[0,0].set_ylabel("Fase (graus)")
axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3); axes[0,0].set_xlim(0, fs/2)

axes[0,1].plot(w_iir, np.degrees(fase_iir), color="darkorange", linewidth=1.5)
axes[0,1].axvline(fc, color="gray", linestyle=":", alpha=0.5)
axes[0,1].set_title(f"Fase do IIR Butterworth (ordem {ordem_iir}) – NÃO-LINEAR")
axes[0,1].set_xlabel("Frequência (Hz)"); axes[0,1].set_ylabel("Fase (graus)")
axes[0,1].grid(True, alpha=0.3); axes[0,1].set_xlim(0, fs/2)

axes[1,0].plot(w_fir[mask_bp], np.degrees(erro_lin_fir), color="steelblue", linewidth=1.5)
axes[1,0].set_title("Erro de linearidade de fase – FIR")
axes[1,0].set_xlabel("Frequência (Hz)"); axes[1,0].set_ylabel("Erro (graus)")
axes[1,0].grid(True, alpha=0.3)

axes[1,1].plot(w_iir[mask_bp], np.degrees(erro_lin_iir), color="darkorange", linewidth=1.5)
axes[1,1].set_title("Erro de linearidade de fase – IIR")
axes[1,1].set_xlabel("Frequência (Hz)"); axes[1,1].set_ylabel("Erro (graus)")
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q08_resposta_fase.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"Erro máximo de linearidade na banda de passagem:")
print(f"  FIR: {np.max(np.abs(np.degrees(erro_lin_fir))):.6f} graus")
print(f"  IIR: {np.max(np.abs(np.degrees(erro_lin_iir))):.4f} graus")
print("\nO FIR simétrico possui fase perfeitamente linear (erro ~0),")
print("garantindo atraso constante para todas as frequências.")
print("O IIR apresenta distorção de fase significativa, especialmente")
print("próximo à frequência de corte.")
