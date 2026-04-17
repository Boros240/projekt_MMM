import matplotlib.pyplot as plt
from parametry import u_harmoniczny,u_trojkatny,t

u_input = u_harmoniczny
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

axs[0].plot(t, u_input, color='blue')
axs[0].set_title('Sygnał harmoniczny')
axs[0].grid(True)

axs[1].plot(t, u_trojkatny, color='orange')
axs[1].set_title('Sygnał trójkątny')
axs[1].grid(True)