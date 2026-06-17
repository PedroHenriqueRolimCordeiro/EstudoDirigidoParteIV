# Q6 - Resposta ao impulso: FIR (finita) vs IIR (infinita)

import numpy as np
from scipy.signal import firwin, butter, lfilter
import matplotlib.pyplot as plt
import os

fs = 1000
fc = 100
N_amostras = 200

# Filtros
ordem_fir = 31
b_fir = firwin(ordem_fir, fc, fs=fs)

ordem_iir = 4
b_iir, a_iir = butter(ordem_iir, fc, btype='low', fs=fs)

# Impulso unitário delta[n]
impulso = np.zeros(N_amostras)
impulso[0] = 1.0

# Respostas
h_fir = lfilter(b_fir, 1.0, impulso)
h_iir = lfilter(b_iir, a_iir, impulso)

# Plots
n = np.arange(N_amostras)

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle("Q6 – Resposta ao Impulso: FIR vs IIR", fontsize=14, fontweight="bold")

axes[0].stem(n, h_fir, linefmt="steelblue", markerfmt=".", basefmt="gray")
axes[0].axvline(ordem_fir - 1, color="red", linestyle="--", alpha=0.7,
                label=f"Ordem do filtro (n={ordem_fir - 1})")
axes[0].set_title(f"Resposta ao impulso – FIR (ordem {ordem_fir}): duração FINITA")
axes[0].set_xlabel("Amostra (n)")
axes[0].set_ylabel("h[n]")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].stem(n, h_iir, linefmt="darkorange", markerfmt=".", basefmt="gray")
axes[1].set_title(f"Resposta ao impulso – IIR Butterworth (ordem {ordem_iir}): duração INFINITA")
axes[1].set_xlabel("Amostra (n)")
axes[1].set_ylabel("h[n]")
axes[1].grid(True, alpha=0.3)

# Anotação mostrando que a cauda do IIR não zera
ultimo_nz = np.max(np.where(np.abs(h_iir) > 1e-6))
axes[1].annotate(f"Ainda ≠ 0 em n={ultimo_nz}",
                 xy=(ultimo_nz, h_iir[ultimo_nz]),
                 xytext=(ultimo_nz - 40, max(h_iir) * 0.6),
                 arrowprops=dict(arrowstyle="->", color="crimson"),
                 fontsize=10, color="crimson")

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q06_resposta_impulso.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print(f"FIR (ordem {ordem_fir}):")
print(f"  h[n] = 0 para n >= {ordem_fir} (resposta FINITA)")
print(f"  Número de coeficientes não-nulos: {np.sum(np.abs(h_fir) > 1e-10)}")
print()
print(f"IIR Butterworth (ordem {ordem_iir}):")
print(f"  h[n] decai exponencialmente mas nunca atinge exatamente zero")
print(f"  |h[{N_amostras-1}]| = {np.abs(h_iir[-1]):.2e} (resposta INFINITA)")
print()
print("A diferença fundamental é que o FIR tem um número finito de coeficientes,")
print("resultando em h[n] = 0 após a ordem do filtro. O IIR, pela realimentação,")
print("produz uma resposta que decai exponencialmente mas nunca se anula completamente.")
