#Realtionship between input size and number of steps to find failure set
import matplotlib.pyplot as plt

# Data for different failure sets
failure_sets = {
    "[1]": [(10, 8), (20, 10), (30, 10), (40, 12), (50, 12), (60, 12), (70, 14), (80, 14), (90, 14), (100, 14), (110, 14), (120, 14)],
    "[11]": [(20, 9), (30, 7), (40, 11), (50, 9), (60, 9), (70, 12), (80, 13), (90, 11), (100, 11), (110, 12), (120, 11)],
    "[5]": [(10, 5), (20, 7), (30, 9), (40, 9), (50, 10), (60, 11), (70, 13), (80, 11), (90, 12), (100, 12), (110, 12), (120, 13)],
     "[15]": [(20, 6), (30, 6), (40, 8), (50, 10), (60, 8), (70, 11), (80, 10), (90, 12), (100, 12), (110, 13), (120, 10)],
    "[10]": [(10, 4), (20, 6), (30, 8), (40, 8), (50, 10), (60, 10), (70, 13), (80, 10), (90, 12), (100, 12), (110, 12), (120, 12)]
    
}

# Plotting for each failure set
plt.figure(figsize=(12, 8))
for failure_set, data in failure_sets.items():
    n_values, steps = zip(*data)  # Unpacking the data
    plt.plot(n_values, steps, marker='o', linestyle='-', label=f"Failure Set {failure_set}")

plt.title("Number of Steps vs. Number of Input Sequences for Different Failure (Single) Sets")
plt.xlabel("Number of Input Sequences (n)")
plt.ylabel("Number of Steps to Find Minimal Failure Entities")
plt.grid(True)
plt.legend()
plt.show()




import matplotlib.pyplot as plt

# Data for different failure sets
failure_sets1 = {
    "[1,5]": [(10, 8), (20, 10), (30, 20), (40, 12), (50, 24), (60, 22), (70, 25), (80, 14), (90, 23), (100, 26), (110, 26), (120, 24)],
       "[5, 10]": [(10, 18), (20, 20), (30, 19), (40, 22), (50, 21), (60, 21), (70, 27), (80, 24), (90, 20), (100, 23), (110, 20), (120, 23)],
    "[5,11]": [(20, 18), (30, 25), (40, 20), (50, 26), (60, 27), (70, 22), (80, 22), (90, 25), (100, 28), (110, 26), (120, 29)],
     "[1,11]": [(20, 24), (30, 27), (40, 26), (50, 28), (60, 29), (70, 23), (80, 28), (90, 27), (100, 30), (110, 28), (120, 31)],
     "[5,10],[1,11]": [(20, 20), (30, 19), (40, 22), (50, 21), (60, 21), (70, 27), (80, 24), (90, 20), (100, 23), (110, 20), (120, 23)],
     "[1,5,6]": [(10, 24), (20, 26), (30, 18), (40, 28), (50, 22), (60, 20), (70, 23), (80, 30), (90, 21), (100, 24), (110, 24), (120, 22)],
     "[7,8,9]": [(10, 10), (20, 12), (30, 20), (40, 14), (50, 16), (60, 22), (70, 14), (80, 16), (90, 15), (100, 18), (110, 21), (120, 24)],
     "[1,5,6],[7,8,9]": [(10, 10), (20, 12), (30, 18), (40, 14), (50, 16), (60, 20), (70, 14), (80, 16), (90, 15), (100, 18), (110, 24), (120, 22)]
}

# Plotting for each failure set
plt.figure(figsize=(12, 8))
for failure_set, data in failure_sets1.items():
    n_values, steps = zip(*data)  # Unpacking the data
    plt.plot(n_values, steps, marker='o', linestyle='-', label=f"Failure Set {failure_set}")

plt.title("Number of Steps vs. Number of Input Sequences for Different Failure (multiple) Sets")
plt.xlabel("Number of Input Sequences (n)")
plt.ylabel("Number of Steps to Find Minimal Failure Entities")
plt.grid(True)
plt.legend()
plt.show()


#Relationship between different distributions of minimal failure sets with number of steps to identify these failures for a constant input sequence size
import matplotlib.pyplot as plt

# Data
difference = [29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
steps = [26, 25, 25, 24, 25, 24, 24, 25, 24, 24, 23, 24, 23, 23, 24, 17, 16, 16, 15, 12, 11, 7, 16, 15, 15, 14, 11, 10, 6]

# Plot
plt.plot(difference, steps, marker='o', linestyle='-')
plt.xlabel('Difference (b - a)')
plt.ylabel('Number of Steps')
plt.title('Variation of Steps with cumulative difference (constant input sequence size i.e., n=30)')
plt.grid(True)
plt.show()


#Relationship between number of steps, failed set identified, in relation to change in first component of the input sequence alone
import matplotlib.pyplot as plt

# Data
n_values = list(range(1, 121))
steps = [30] * 120  # Number of steps is constant at 30 for all n values

# Plot
plt.plot(n_values, steps, marker='o', linestyle='-')
plt.xlabel('Input Sequence Size (n) (variable a, fixed b)')
plt.ylabel('Number of Steps')
plt.title('\n Regardless of the size of the input sequences, represented by the variable n, \n the number of steps to identify the failure set F remains constant at 30.', fontsize=10)
plt.grid(True)
plt.show()

