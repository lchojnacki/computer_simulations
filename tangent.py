from sympy import symbols, exp, cos, pi, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x_0 = 0
x = np.linspace(0, 2*np.pi, 200)

t = symbols('t')
w = 2*exp(-t) * cos(2*pi*t)
f = lambdify(t, w, 'numpy')

dw = w.diff(t)

f_prime = lambdify(t, dw, 'numpy')
f_prime(x_0) * (x-x_0) + f(x_0)

y = f(x)
ys = f_prime(x_0) * (x-x_0) + f(x_0)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25) # dodajemy miejsce na dole rysunku na drugą oś
ax.set_ylim(-3, 3)
ax.plot(x, y)
line_secant, = ax.plot(x, ys)
line_points, = ax.plot([x_0], [f(x_0)], 'or')
ax2 = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_h = Slider(ax2, 'h', 0, 6.2, valinit=x_0)

def update(val):
    x_0 = val
    ys = f_prime(x_0) * (x-x_0) + f(x_0)
    line_secant.set_ydata(ys)
    line_points.set_xdata([x_0])
    line_points.set_ydata([f(x_0)])

slider_h.on_changed(update)

ax.grid(True)
plt.show()