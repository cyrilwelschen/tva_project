from matplotlib import pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111)
p = ax.plot(np.random.rand(10))
lin = ax.axvline(0.5)
lin.set_xdata(3)


def onclick(event):
    print(event.name)
    print("x-Axis value: ", event.xdata)


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes != self.line.axes:
            return
        self.line.set_xdata(event.xdata)
        self.line.figure.canvas.draw()


lb = LineBuilder(lin)
plt.show()
