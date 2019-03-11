from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

path = "../results/gridSearch/eps/cm100k/param/eps{0}_recall_cm100_wmean.txt"
alg = "Epsilon"

values = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1]
fig = plt.figure()
sns.set()
sns.set_context("paper")
ax = fig.add_subplot(111)
colors = sns.hls_palette(len(values)+1, l=.4, s=.8)
ax.set_prop_cycle('color', colors)
for value in values:
    print(path.format(value))
    plot_results_graph(path.format(value), r"$\epsilon$={0}".format(value))

plt.legend()
plt.savefig("../results/memoria/cm100k/Recall"+ alg +".png")
plt.show()

fig = plt.figure()
sns.set()
sns.set_context("paper")
ax = fig.add_subplot(111)
colors = sns.hls_palette(len(values)+1, l=.4, s=.8)
ax.set_prop_cycle('color', colors)
X = []
Y = []
with open("../results/gridSearch/eps/cm100k/param/eps_param.txt") as input_file:
    for line in input_file:
        spl = line.strip("\n").split(",")
        x = float(spl[0])
        y = float(spl[1])
        X.append(x)
        Y.append(y)
        plt.scatter([x], [y], s=50)
plt.plot(X, Y, color="black")
plt.xlabel(r"$\epsilon$")
plt.ylabel("Recall mitad")
plt.savefig("../results/memoria/cm100k/RecallMitad"+ alg +".png")
plt.show()
