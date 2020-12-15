import numpy as np
import matplotlib.pyplot as plt
x_list = np.array(range(0,100, 1))
x_list = x_list / 10
e_list = np.exp(x_list)
print (e_list)

plt.plot(x_list,e_list)
plt.show()