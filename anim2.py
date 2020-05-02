import sys
import numpy as np
from random import randrange
from matplotlib import use as mplbackend
mplbackend('qt5agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('seaborn-ticks')

fig = plt.figure()

color = list()

def animate(num, data, lines):

	for i, line in enumerate(lines):
		line.set_data(data[i][..., :num])

	return lines

	
def newplot(limits, lines, legends, data, num):
	xmin, xmax, ymin, ymax = limits
	plt.xlim(xmin, xmax)
	plt.ylim(ymin, ymax)
	
	plt.grid()
	plt.legend(lines, legends)

	plt.ylabel('Time (seconds)')
	plt.xlabel('Input Dimensions')

	#anime = animation.FuncAnimation(fig, animate, fargs=(data, lines), interval=2000/data.shape[2], blit=True)
	
	plt.show()
	
def foo(n, r):
	return np.power(n, r)

def main():

	lnum = 5
	#lnum = int(input())
	#num = int(input())
	num = 200
	lines = list()
	data = list()

	xmax, xmin = 0, 0
	ymax, ymin = 0, 0

	legends = list()

	for j in range(lnum):
		color.append('#' + ('%006x' % randrange(16**6)).upper())
		legends.append("execution " + str(j+1))
		data_x, data_y = [None]*num, [None]*num
		for i in range(num):
			#data_x[i] = float(input())
			data_x[i] = i * 10
			xmax = max([xmax, data_x[i]])
			xmin = min([xmin, data_x[i]])

		for i in range(num):
			#data_y[i] = float(input())
			data_y[i] = foo(i, j*0.25 + 1)
			ymax = max([ymax, data_y[i]])
			ymin = min([ymin, data_y[i]])

		data.append(np.row_stack((np.array(data_x), np.array(data_y))))
		
	data = np.array(data)
	for i in range(lnum):
		line, = plt.plot([], [], color[i] , lw=2)
		lines.append(line)
	
	newplot((xmin, xmax, ymin, ymax), lines, legends, data, num)


if __name__ == '__main__':
	main()

