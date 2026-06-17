# PBL - Monitoramento Agrícola (Filtros para temperatura, umidade e pH)

import numpy as np
from scipy.signal import firwin, butter, lfilter, freqz
import matplotlib.pyplot as plt
import os

np.random.seed(42)
os.makedirs("resultados", exist_ok=True)

# 1. Simulando os sinais
fs = 10            # amostras por minuto
T_horas = 24       # tempo total em horas
N = int(fs * 60 * T_horas)
t_min = np.arange(N) / fs
t_horas = t_min / 60

# --- Temperatura (°C) ---
# Variação do dia + nuvens/irrigação
temp_base = 22 + 8 * np.sin(2 * np.pi * t_horas / 24 - np.pi/2)
temp_nuvens = 0.5 * np.sin(2 * np.pi * t_min / 120)
temp_real = temp_base + temp_nuvens

# Ruído: gaussiano + interferência da rede elétrica
ruido_temp = 0.8 * np.random.randn(N)
ruido_temp += 0.3 * np.sin(2 * np.pi * 2.5 * t_min / 60)
temp_ruidosa = temp_real + ruido_temp

# --- Umidade (%) ---
umid_base = 60 * np.ones(N)

# Picos de irrigação às 6h e 18h
for t_irrig in [6, 18]:
    idx_irrig = int(t_irrig * 60 * fs)
    mascara = np.arange(N) >= idx_irrig
    umid_base[mascara] += 15 * np.exp(-(t_min[mascara] - t_irrig * 60) / 180)

# Queda por evaporação durante o dia
umid_base -= 5 * np.maximum(0, np.sin(2 * np.pi * t_horas / 24 - np.pi/6))
umid_real = umid_base

# Ruído do sensor capacitivo
ruido_umid = 2.0 * np.random.randn(N)
ruido_umid += 1.0 * np.sin(2 * np.pi * 3.0 * t_min / 60)
umid_ruidosa = umid_real + ruido_umid

# --- pH do solo ---
# Correção lenta de calcário
ph_base = 6.5 + 0.3 * (1 - np.exp(-t_horas / 12))
ph_real = ph_base + 0.1 * np.sin(2 * np.pi * t_horas / 12)

# Ruído normal + spikes do sensor
ruido_ph = 0.15 * np.random.randn(N)
spikes = np.zeros(N)
idx_spikes = np.random.choice(N, size=30, replace=False)
spikes[idx_spikes] = np.random.choice([-1, 1], size=30) * np.random.uniform(0.5, 1.5, size=30)
ruido_ph += spikes
ph_ruidoso = ph_real + ruido_ph


# 2. Filtros

# Temperatura: FIR passa-baixa (precisa de fase linear pra não perder o tempo exato dos picos)
fc_temp = 0.01
ordem_temp = 201
b_temp = firwin(ordem_temp, fc_temp, fs=fs/60)
temp_filtrada = lfilter(b_temp, 1.0, temp_ruidosa)

# Umidade: IIR Butterworth (mudanças lentas, foca no valor final, gasta menos processamento)
fc_umid = 0.008
ordem_umid = 3
b_umid, a_umid = butter(ordem_umid, fc_umid, btype='low', fs=fs/60)
umid_filtrada = lfilter(b_umid, a_umid, umid_ruidosa)

# pH: Mediana + FIR (mediana tira os spikes, FIR limpa o resto)
from scipy.ndimage import median_filter
ph_sem_spikes = median_filter(ph_ruidoso, size=21)

fc_ph = 0.005
ordem_ph = 151
b_ph = firwin(ordem_ph, fc_ph, fs=fs/60)
ph_filtrado = lfilter(b_ph, 1.0, ph_sem_spikes)


# 3. Calculando métricas

def calcular_snr(limpo, ruidoso):
    erro = ruidoso - limpo
    return 10 * np.log10(np.var(limpo) / (np.var(erro) + 1e-12))

def calcular_rmse(limpo, filtrado):
    return np.sqrt(np.mean((filtrado - limpo) ** 2))

# Corta o início pra não pegar o transiente do filtro
corte = 500

metricas = {
    "Temperatura": {
        "SNR antes": calcular_snr(temp_real[corte:], temp_ruidosa[corte:]),
        "SNR depois": calcular_snr(temp_real[corte:], temp_filtrada[corte:]),
        "RMSE antes": calcular_rmse(temp_real[corte:], temp_ruidosa[corte:]),
        "RMSE depois": calcular_rmse(temp_real[corte:], temp_filtrada[corte:]),
    },
    "Umidade": {
        "SNR antes": calcular_snr(umid_real[corte:], umid_ruidosa[corte:]),
        "SNR depois": calcular_snr(umid_real[corte:], umid_filtrada[corte:]),
        "RMSE antes": calcular_rmse(umid_real[corte:], umid_ruidosa[corte:]),
        "RMSE depois": calcular_rmse(umid_real[corte:], umid_filtrada[corte:]),
    },
    "pH": {
        "SNR antes": calcular_snr(ph_real[corte:], ph_ruidoso[corte:]),
        "SNR depois": calcular_snr(ph_real[corte:], ph_filtrado[corte:]),
        "RMSE antes": calcular_rmse(ph_real[corte:], ph_ruidoso[corte:]),
        "RMSE depois": calcular_rmse(ph_real[corte:], ph_filtrado[corte:]),
    },
}


# 4. Plots

# Sinais no tempo
fig, axes = plt.subplots(3, 2, figsize=(16, 12))
fig.suptitle("Sistema de Monitoramento Agrícola – Filtragem de Sinais de Sensores",
             fontsize=15, fontweight="bold")

# Temp
axes[0, 0].plot(t_horas, temp_ruidosa, color="lightcoral", linewidth=0.3, alpha=0.6, label="Ruidoso")
axes[0, 0].plot(t_horas, temp_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[0, 0].set_title("Temperatura – Sinal ruidoso")
axes[0, 0].set_ylabel("°C"); axes[0, 0].legend(); axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(t_horas, temp_filtrada, color="crimson", linewidth=1.5, label="Filtrado (FIR)")
axes[0, 1].plot(t_horas, temp_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[0, 1].set_title(f"Temperatura – Após FIR (ordem {ordem_temp}, fc={fc_temp} Hz)")
axes[0, 1].set_ylabel("°C"); axes[0, 1].legend(); axes[0, 1].grid(True, alpha=0.3)

# Umid
axes[1, 0].plot(t_horas, umid_ruidosa, color="lightblue", linewidth=0.3, alpha=0.6, label="Ruidoso")
axes[1, 0].plot(t_horas, umid_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[1, 0].set_title("Umidade do solo – Sinal ruidoso")
axes[1, 0].set_ylabel("%"); axes[1, 0].legend(); axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(t_horas, umid_filtrada, color="steelblue", linewidth=1.5, label="Filtrado (IIR Butterworth)")
axes[1, 1].plot(t_horas, umid_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[1, 1].set_title(f"Umidade – Após IIR Butterworth (ordem {ordem_umid}, fc={fc_umid} Hz)")
axes[1, 1].set_ylabel("%"); axes[1, 1].legend(); axes[1, 1].grid(True, alpha=0.3)

# pH
axes[2, 0].plot(t_horas, ph_ruidoso, color="lightgreen", linewidth=0.3, alpha=0.6, label="Ruidoso")
axes[2, 0].plot(t_horas, ph_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[2, 0].set_title("pH do solo – Sinal ruidoso (com spikes)")
axes[2, 0].set_xlabel("Tempo (horas)"); axes[2, 0].set_ylabel("pH")
axes[2, 0].legend(); axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].plot(t_horas, ph_filtrado, color="forestgreen", linewidth=1.5, label="Filtrado (Mediana + FIR)")
axes[2, 1].plot(t_horas, ph_real, color="gray", linewidth=1.5, linestyle="--", label="Real")
axes[2, 1].set_title(f"pH – Após Mediana + FIR (ordem {ordem_ph}, fc={fc_ph} Hz)")
axes[2, 1].set_xlabel("Tempo (horas)"); axes[2, 1].set_ylabel("pH")
axes[2, 1].legend(); axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/pbl_sinais_temporais.png", dpi=150, bbox_inches="tight")
plt.show()

# Respostas em frequência
fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5))
fig2.suptitle("Respostas em Frequência dos Filtros Projetados", fontsize=14, fontweight="bold")

# Temp (FIR)
w_t, H_t = freqz(b_temp, worN=2048, fs=fs/60)
axes2[0].plot(w_t * 1000, 20 * np.log10(np.abs(H_t) + 1e-12), color="crimson", linewidth=1.5)
axes2[0].axvline(fc_temp * 1000, color="gray", linestyle="--", label=f"fc = {fc_temp*1000:.0f} mHz")
axes2[0].axhline(-3, color="gray", linestyle=":", alpha=0.5)
axes2[0].set_title("Temperatura (FIR)"); axes2[0].set_xlabel("Frequência (mHz)")
axes2[0].set_ylabel("Magnitude (dB)"); axes2[0].legend(); axes2[0].grid(True, alpha=0.3)

# Umid (IIR)
w_u, H_u = freqz(b_umid, a_umid, worN=2048, fs=fs/60)
axes2[1].plot(w_u * 1000, 20 * np.log10(np.abs(H_u) + 1e-12), color="steelblue", linewidth=1.5)
axes2[1].axvline(fc_umid * 1000, color="gray", linestyle="--", label=f"fc = {fc_umid*1000:.0f} mHz")
axes2[1].axhline(-3, color="gray", linestyle=":", alpha=0.5)
axes2[1].set_title("Umidade (IIR Butterworth)"); axes2[1].set_xlabel("Frequência (mHz)")
axes2[1].set_ylabel("Magnitude (dB)"); axes2[1].legend(); axes2[1].grid(True, alpha=0.3)

# pH (FIR)
w_p, H_p = freqz(b_ph, worN=2048, fs=fs/60)
axes2[2].plot(w_p * 1000, 20 * np.log10(np.abs(H_p) + 1e-12), color="forestgreen", linewidth=1.5)
axes2[2].axvline(fc_ph * 1000, color="gray", linestyle="--", label=f"fc = {fc_ph*1000:.0f} mHz")
axes2[2].axhline(-3, color="gray", linestyle=":", alpha=0.5)
axes2[2].set_title("pH (FIR)"); axes2[2].set_xlabel("Frequência (mHz)")
axes2[2].set_ylabel("Magnitude (dB)"); axes2[2].legend(); axes2[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/pbl_respostas_frequencia.png", dpi=150, bbox_inches="tight")
plt.show()
