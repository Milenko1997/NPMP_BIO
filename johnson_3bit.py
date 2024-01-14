from models import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
    

"""
    TESTING
"""

# simulation parameters
t_end = 200
N = 1000


# model parameters
alpha1 = 34.73 # protein_production
alpha2 = 49.36 # protein_production
alpha3 = 32.73 # protein_production
alpha4 = 49.54 # protein_production
delta1 = 1.93 # protein_degradation
delta2 = 0.69 # protein_degradation
Kd = 10.44 # Kd
n = 4.35 # hill

params_ff = (alpha1, alpha2, alpha3, alpha4, delta1, delta2, Kd, n)


# three-bit counter with external clock
# a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3
Y0 = np.array([0]*12) # initial state
T = np.linspace(0, t_end, N) # vector of timesteps

# numerical interation
Y = odeint(three_bit_model, Y0, T, args=(params_ff,))

Y_reshaped = np.split(Y, Y.shape[1], 1)

# plotting the results
Q1 = Y_reshaped[2]
not_Q1 = Y_reshaped[3]
Q2 = Y_reshaped[6]
not_Q2 = Y_reshaped[7]
Q3 = Y_reshaped[10]
not_Q3 = Y_reshaped[11]


plt.plot(T, Q1, label='q1')
plt.plot(T, Q2, label='q2')
plt.plot(T, Q3, label='q3')
#plt.plot(T, not_Q1, label='not q1')
#plt.plot(T, not_Q2, label='not q2')

plt.plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)

plt.legend()
plt.show()
# Set up a column of plots
fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # 4 rows, 1 column
colors = ['blue', 'orange', 'green', 'red']
# Plotting the results in subplots
axs[0].plot(T, Q1, label=f'Q1', color = colors[1])  # Plotting the q output of each flip-flop
axs[1].plot(T, Q2, label=f'Q2', color = colors[2])  # Plotting the q output of each flip-flop
axs[2].plot(T, Q3, label=f'Q3', color = colors[3])  # Plotting the q output of each flip-flop
axs[1].plot(T, get_clock(T),  '--', linewidth=2, label="CLK", color='black', alpha=0.25)
axs[1].set_title(f'State Q{1} Over Time')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('State')
axs[1].legend()


# Main title
fig.suptitle('SIPO Register State Over Time', fontsize=16)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])