import sys
import csv
from collections import defaultdict

fname = sys.argv[1]
with open(fname, "r") as fh:
    table = [row for row in csv.reader(fh)]
print("Reservation Table: ")
print(*("  ".join(row) for row in table), sep='\n')

def get_forbidden_latencies(stage):
    return set(j-i for i in range(len(stage)-1)
                    for j in range(i+1, len(stage)) if stage[i] == stage[j] == 'x')

forbid_lats = set(lats for stage in table for lats in get_forbidden_latencies(stage))
print("Forbidden Latencies: %r"%forbid_lats)

max_forb = 0
coll_vec = 0
for lat in forbid_lats:
    coll_vec |= 1 << (lat-1)
    max_forb = max(max_forb, lat)
print("Collision Vector:    {0:b} (={0})".format(coll_vec))

# build graph
graph = defaultdict(list)
done = set()
nodes = {coll_vec}
while True:
    for u in nodes:
        if u not in done:
            curr = u
            break
    else:
        break
    for i in range(max_forb+1):
        if not (curr >> i) & 1:
            state = (curr >> (i+1)) | coll_vec
            graph[curr].append((state, i+1))
            nodes.add(state)
    done.add(curr)
print("States:\n", *("{0:b}".format(i) for i in nodes))
print("\nState Transition Graph: ")
for u in graph:
    for v, w in graph[u]:
        print("{0:b} -> {1:b} : {2}".format(u, v, w))

def find_cycles(G, u, cycle):
    Cycles = []
    for v, w in G[u]:
        if v == cycle[0][0]:
            Cycles.append(cycle + [(v, w)])
        elif not any(v == c[0] for c in cycle):
            Cycles.extend(c for c in find_cycles(G, v, cycle + [(v, w)]))
    return Cycles

def is_rotated(c1, c2):
    c = c1 + c1
    for i in range(len(c)-len(c2)+1):
        if c[i:i+len(c2)] == c2: return True
    return False

greedy_cycle = None
MAL = float('inf')
Cycles = {}
greedyCycles = {}
print("\nSimple Cycles\tAvg. Latency")

for u in nodes:
    greedy_cycle = None
    MAL = float('inf')
    for cyc in find_cycles(graph, u, [(u, 0)]):
        wts = tuple(i[1] for i in cyc[1:])
        avg = sum(wts)/len(wts)
        if any((is_rotated(wts, c) and Cycles[c]==avg) for c in Cycles): continue
        Cycles[wts] = avg
        wts = '('+", ".join(map(str, wts))+')'
        if avg < MAL:
            MAL = avg
            greedy_cycle = wts
        print("{0:^13s}\t{1:^12.2f}".format(wts, avg))
    if greedy_cycle is not None: greedyCycles[greedy_cycle] = MAL

MAL = float('inf')
print("\nGreedy Cycles\tAvg. Latency")
greedy_cyc = None
for cyc in greedyCycles:
    if greedyCycles[cyc] < MAL:
        MAL = greedyCycles[cyc]
        greedy_cyc = cyc
    print("{0:^13s}\t{1:^12.2f}".format(cyc, greedyCycles[cyc]))

print(f"\nGreedy Cycle:      {greedy_cyc}\n"
      f"MAL:               {MAL:.2f}\n"
      f"Throughput:        {1/MAL:.2f}")
