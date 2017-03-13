import matplotlib as mpl
import matplotlib.pyplot as plt
import math

f_1 = open('time_run_out.csv')
f_2 = open('time_run_window_out.csv')

f_1_data = f_1.readlines()
f_1_data = [item.strip().split(';') for item in f_1_data]
f_1_x = [int(float(item[0])) for item in f_1_data]
f_1_y = [float(item[1]) for item in f_1_data]
f_1.close()

#print(f_1_y)

f_2_data = f_2.readlines()
f_2_data = [item.strip().split(';') for item in f_2_data]
f_2_x = [int(float(item[0])/1000) for item in f_2_data]
f_2_y = [float(item[1]) for item in f_2_data]
del f_2_x[-1]
del f_2_y[-1]
f_2.close()

#print(f_2_x)


plt.plot(f_1_x, f_1_y, 'ro')
#plt.plot(f_2_x, f_2_y, 'bs')
plt.xlabel('Number of alternatives')
#plt.xlabel('Number of alternatives (in thousands)')
plt.ylabel('Excution time (in seconds)')
plt.title('Execution time in the case of "standard" PROMETHEE')
#plt.title('Execution time in the case of "sorting-based" PROMETHEE')
plt.grid(True)
plt.savefig('standard_promethee.pdf')
#plt.savefig('sorting_based_promethee.pdf')
plt.show()
