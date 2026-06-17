# Q9 - Atraso de grupo: Butterworth vs Chebyshev vs Elíptico

import numpy as np
from scipy.signal import butter, cheby1, ellip, group_delay, freqz
import matplotlib.pyplot as plt
import os

fs = 1000
fc = 100
ordem = 4

# Três tipos de filtro IIR, mesma ordem e fc
b_but, a_but = butter(ordem, fc, btype='low', fs=fs)
b_cheb, a_cheb = cheby1(ordem, 1.0, fc, btype='low', fs=fs)      # 1 dB ripple
b_elip, a_elip = ellip(ordem, 1.0, 40, fc, btype='low', fs=fs)   # 1 dB ripple, 40 dB rejeição

# Atraso de grupo
w_but, gd_but = group_delay((b_but, a_but), w=2048, fs=fs)
w_cheb, gd_cheb = group_delay((b_cheb, a_cheb), w=2048, fs=fs)
w_elip, gd_elip = group_delay((b_elip, a_elip), w=2048, fs=fs)

# Plots
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle("Q9 – Atraso de Grupo: Butterworth vs Chebyshev vs Elíptico",
             fontsize=14, fontweight="bold")

axes[0].plot(w_but, gd_but, color="steelblue", linewidth=1.5, label="Butterworth")
axes[0].plot(w_cheb, gd_cheb, color="darkorange", linewidth=1.5, label="Chebyshev I (1 dB)")
axes[0].plot(w_elip, gd_elip, color="crimson", linewidth=1.5, label="Elíptico (1 dB, 40 dB)")
axes[0].axvline(fc, color="gray", linestyle="--", alpha=0.5, label=f"fc = {fc} Hz")
axes[0].set_title("Atraso de grupo (amostras)")
axes[0].set_xlabel("Frequência (Hz)")
axes[0].set_ylabel("Atraso de grupo (amostras)")
axes[0].set_xlim(0, 200)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Magnitude pra contexto
w, H_but = freqz(b_but, a_but, worN=2048, fs=fs)
_, H_cheb = freqz(b_cheb, a_cheb, worN=2048, fs=fs)
_, H_elip = freqz(b_elip, a_elip, worN=2048, fs=fs)

axes[1].plot(w, 20*np.log10(np.abs(H_but)+1e-12), color="steelblue", linewidth=1.5, label="Butterworth")
axes[1].plot(w, 20*np.log10(np.abs(H_cheb)+1e-12), color="darkorange", linewidth=1.5, label="Chebyshev I")
axes[1].plot(w, 20*np.log10(np.abs(H_elip)+1e-12), color="crimson", linewidth=1.5, label="Elíptico")
axes[1].axvline(fc, color="gray", linestyle="--", alpha=0.5, label=f"fc = {fc} Hz")
axes[1].axhline(-3, color="gray", linestyle=":", alpha=0.5, label="-3 dB")
axes[1].set_title("Resposta em magnitude (referência)")
axes[1].set_xlabel("Frequência (Hz)")
axes[1].set_ylabel("Magnitude (dB)")
axes[1].set_xlim(0, 300); axes[1].set_ylim(-60, 5)
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q09_atraso_grupo.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"Atraso de grupo máximo próximo a fc:")
mask = (w_but > 0.8*fc) & (w_but < 1.2*fc)
print(f"  Butterworth: {np.max(gd_but[mask]):.2f} amostras")
print(f"  Chebyshev I: {np.max(gd_cheb[mask]):.2f} amostras")
print(f"  Elíptico:    {np.max(gd_elip[mask]):.2f} amostras")
print("\nO filtro elíptico tem transição mais abrupta, mas paga com maior variação")
print("no atraso de grupo. Butterworth tem atraso mais suave. Chebyshev fica entre os dois.")
print("Em aplicações onde atraso constante é crítico, Butterworth é preferível.")
