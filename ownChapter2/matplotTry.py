import matplotlib.pyplot as plt
import numpy as np

noten_tobi = [72, 78, 55, 63]
noten_jan = [66, 55, 44, 60]


#plot
#           x,      y
plt.plot([1, 2, 3, 4], noten_tobi, color= "blue")
plt.plot([1, 2, 3, 4], noten_jan, color= "red")
plt.legend(["tobi", "jan"])
plt.xlabel(["Fach"])
plt.ylabel(["Note/%"])
plt.grid()
plt.title("Jan ist schlechter als Tobi")
plt.show()

#scatter
plt.scatter([1, 2, 3, 4], noten_tobi, color= "blue")
plt.scatter([1, 2, 3, 4], noten_jan, color= "red")
plt.legend(["tobi", "jan"])
plt.xlabel(["Fach"])
plt.ylabel(["Note/%"])
plt.grid()
plt.title("Jan ist schlechter als Tobi")
plt.show()