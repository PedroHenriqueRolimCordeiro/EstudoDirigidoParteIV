# Q5 - Polos e zeros de filtro IIR + análise de estabilidade

import numpy as np
from scipy.signal import butter, tf2zpk
import matplotlib.pyplot as plt
import os

fs = 1000
fc = 150

# Filtro estável: Butterworth ordem 4
b_est, a_est = butter(4, fc, btype='low', fs=fs)
z_est, p_est, k_est = tf2zpk(b_est, a_est)

# Filtro instável (artificial): polo em z = 1.2, fora do circulo unitário
b_inst = [1.0]
a_inst = [1.0, -1.2]
z_inst, p_inst, k_inst = tf2zpk(b_inst, a_inst)

# Plots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Q5 – Diagrama de Polos e Zeros: Estabilidade de Filtros IIR",
             fontsize=14, fontweight="bold")

for ax, zeros, polos, titulo, cor in [
    (axes[0], z_est, p_est, f"Butterworth ordem 4 (fc={fc} Hz)\n✓ ESTÁVEL", "forestgreen"),
    (axes[1], z_inst, p_inst, "Filtro com polo em z=1.2\n✗ INSTÁVEL", "crimson")
]:
    # Circulo unitario
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=1.0, alpha=0.4)

    ax.scatter(np.real(zeros), np.imag(zeros), marker='o', s=100,
               facecolors='none', edgecolors='steelblue', linewidths=2, label='Zeros', zorder=5)
    ax.scatter(np.real(polos), np.imag(polos), marker='x', s=100,
               color=cor, linewidths=2, label='Polos', zorder=5)

    ax.set_title(titulo, fontsize=11)
    ax.set_xlabel("Re(z)")
    ax.set_ylabel("Im(z)")
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.4, 1.4)

plt.tight_layout()
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/q05_polos_zeros.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n--- Discussão ---")
print("Filtro Butterworth (estável):")
print(f"  Polos: {p_est}")
print(f"  |polos| = {np.abs(p_est)}")
print(f"  Todos dentro do círculo unitário: {all(np.abs(p_est) < 1)}")
print()
print("Filtro artificial (instável):")
print(f"  Polos: {p_inst}")
print(f"  |polos| = {np.abs(p_inst)}")
print(f"  Todos dentro do círculo unitário: {all(np.abs(p_inst) < 1)}")
print()
print("Um filtro IIR é BIBO-estável se e somente se todos os polos")
print("estiverem estritamente dentro do círculo unitário (|p| < 1).")
print("O diagrama de polos e zeros permite verificar visualmente essa condição.")
