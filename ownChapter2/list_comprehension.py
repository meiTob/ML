import numpy as np
import matplotlib.pyplot as plt

data = [[1,2,3],
        [2,3,4]]

y = ['red', 'blue', 'green']


plt.scatter(data[0], data[1])
#plt.show()

w = [1, 3, 6, 9, 7, 4]
w_sqare = [val**2 for val in w[1:5]]
print (w_sqare)