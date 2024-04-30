import matplotlib.pyplot as plt

# Read data from file
filename = "lp_b250_e250_s1800_r30_sa0_sp300.csv"
data = []
with open(filename, 'r') as file:
    for line in file:
        if not line or line == "\n": continue
        x, y = map(int, line.strip().split(','))
        data.append((x, y))

# Separate x and y values
x = [point[0] for point in data]
y = [point[1] for point in data]

# Plot
plt.plot(x, y, marker='o', linestyle='-')
plt.title('Requests per second over time')
plt.xlabel('Time (s)')
plt.ylabel('Requests per second')
plt.grid(True)
plt.show()