import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon, FancyArrowPatch

# Check available styles and use a modern alternative
print("Available matplotlib styles:", plt.style.available)
# Use 'seaborn-v0_8' or 'ggplot' as alternative modern styles
plt.style.use('seaborn-v0_8')  # or 'ggplot', 'seaborn', 'seaborn-whitegrid'

# Set up a more interesting color palette
BACKGROUND_COLOR = '#F5F5F5'
PLOT_COLOR = '#FFFFFF'
GRID_COLOR = '#DDDDDD'
TEXT_COLOR = '#333333'

# Define more interesting functions
def func1(x):
    """Modified sine function with damping."""
    return np.sin(x) * np.exp(-0.05*x)

def func2(x):
    """Modified cosine function with increasing amplitude."""
    return np.cos(x) * (1 + 0.1*x)

def func3(x):
    """Combination of trigonometric functions."""
    return 0.5*np.sin(2*x) + 0.3*np.cos(3*x)

def func4(x):
    """Phase-shifted sine wave."""
    return np.sin(x + np.pi/4)

# Set the range and number of frames
x_min, x_max = 0, 8 * np.pi
frames = 400
animation_interval = 20

# Generate the x values for the full plot
x_full_range = np.linspace(x_min, x_max, 2000)

# Set up the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
fig.patch.set_facecolor(BACKGROUND_COLOR)

for ax in (ax1, ax2):
    ax.set_facecolor(PLOT_COLOR)
    ax.grid(True, linestyle='--', alpha=0.7, color=GRID_COLOR)
    ax.tick_params(axis='both', colors=TEXT_COLOR)

# Colors for the functions
colors = [
    '#FF6B6B',  # Red
    '#4ECDC4',  # Teal
    '#45B7D1',  # Blue
    '#FFA07A'   # Salmon
]

# Initialize the lines
line1, = ax1.plot([], [], label='Damped sine: sin(x)·e⁻⁰·⁰⁵ˣ', 
                 color=colors[0], linewidth=3, marker='o', markersize=6, markevery=[-1])
line2, = ax1.plot([], [], label='Growing cosine: cos(x)·(1+0.1x)', 
                 color=colors[1], linewidth=3, marker='s', markersize=6, markevery=[-1])
line3, = ax1.plot([], [], label='Combination: 0.5sin(2x) + 0.3cos(3x)', 
                 color=colors[2], linewidth=3, marker='^', markersize=6, markevery=[-1])
line4, = ax1.plot([], [], label='Phase-shifted: sin(x + π/4)', 
                 color=colors[3], linewidth=3, marker='D', markersize=6, markevery=[-1])

# Initialize fills
fills = []
for color in colors:
    fill = ax1.fill_between([], [], [], color=color, alpha=0.15)
    fills.append(fill)

# Set plot limits
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(-2.5, 2.5)
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(0, 1)

# Add legend
legend = ax1.legend(loc='upper right', frameon=True, 
                   fancybox=True, shadow=True, 
                   borderpad=1, fontsize=10)
legend.get_frame().set_facecolor(PLOT_COLOR)

# Add titles and labels
fig.suptitle('Advanced Trigonometric Function Animation', 
             fontsize=18, fontweight='bold', color=TEXT_COLOR, y=0.95)
# ax1.set_title('Function Visualization', fontsize=14, color=TEXT_COLOR)
ax2.set_title('Function Energy (Integral of Squares)', fontsize=14, color=TEXT_COLOR)
ax1.set_ylabel("Amplitude", fontsize=12, color=TEXT_COLOR)
ax2.set_ylabel("Energy", fontsize=12, color=TEXT_COLOR)
ax2.set_xlabel("x (radians)", fontsize=12, color=TEXT_COLOR)

# Add phase arrow
phase_arrow = FancyArrowPatch((0, 0), (0, 0), 
                             arrowstyle='->', color=colors[3], 
                             mutation_scale=20, linewidth=2)
ax1.add_patch(phase_arrow)

# Initialize energy bars
bar_width = 0.2
energy_bars = []
for i, color in enumerate(colors):
    bar = ax2.bar(i*bar_width, 0, width=bar_width-0.02, 
                 color=color, alpha=0.7, 
                 label=['Damped', 'Growing', 'Combination', 'Phase'][i])
    energy_bars.append(bar)

# Add energy legend
ax2.legend(loc='upper right', fontsize=9)

# Initialization function
def init():
    for line in [line1, line2, line3, line4]:
        line.set_data([], [])
    
    for fill in fills:
        if hasattr(fill, 'get_paths'):
            fill.set_paths([])
        else:
            # For fill_between objects
            fill.set_data([], [])
    
    phase_arrow.set_positions((0, 0), (0, 0))
    
    for bar in energy_bars:
        for rect in bar:
            rect.set_height(0)
    
    return [line1, line2, line3, line4, phase_arrow] + fills + [bar[0] for bar in energy_bars]

# Animation function
def animate(i):
    current_x_end = x_min + (x_max - x_min) * (i + 1) / frames
    x_data = x_full_range[x_full_range <= current_x_end]
    
    if len(x_data) < 1:
        return init()
    
    # Update main lines
    y1 = func1(x_data)
    y2 = func2(x_data)
    y3 = func3(x_data)
    y4 = func4(x_data)
    
    line1.set_data(x_data, y1)
    line2.set_data(x_data, y2)
    line3.set_data(x_data, y3)
    line4.set_data(x_data, y4)
    
    # Update fills
    fills[0].remove()
    fills[0] = ax1.fill_between(x_data, 0, y1, color=colors[0], alpha=0.15)
    
    fills[1].remove()
    fills[1] = ax1.fill_between(x_data, 0, y2, color=colors[1], alpha=0.15)
    
    fills[2].remove()
    fills[2] = ax1.fill_between(x_data, 0, y3, color=colors[2], alpha=0.15)
    
    fills[3].remove()
    fills[3] = ax1.fill_between(x_data, 0, y4, color=colors[3], alpha=0.15)
    
    # Update phase arrow
    if len(x_data) > 10:
        idx = -10
        phase_arrow.set_positions(
            (x_data[idx], y4[idx]),
            (x_data[-1], y4[-1])
        )
    
    # Update energy bars
    energies = [
        np.trapz(y1**2, x_data),
        np.trapz(y2**2, x_data),
        np.trapz(y3**2, x_data),
        np.trapz(y4**2, x_data)
    ]
    
    for j, (bar, energy) in enumerate(zip(energy_bars, energies)):
        bar[0].set_height(energy / (current_x_end - x_min) * 10)
        bar[0].set_x(j * bar_width)
    
    # Auto-scale energy plot
    max_energy = max(energies) / (current_x_end - x_min) * 10
    ax2.set_ylim(0, max(1, max_energy * 1.1))
    
    return [line1, line2, line3, line4, phase_arrow] + fills + [bar[0] for bar in energy_bars]

# Create the animation
ani = FuncAnimation(fig, animate, frames=frames,
                   init_func=init, blit=False, 
                   interval=animation_interval, repeat=True)

plt.tight_layout()
plt.show()