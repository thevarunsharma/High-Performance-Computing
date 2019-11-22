import math
import random
import threading
from collections import defaultdict, deque

V = int(input("No. of vertices: "))

def generate_random_edges(V):
    edges = [ (u, v, random.randint(1, 100)) for u in range(1, V)
             for v in range(u+1, V+1)]
    return edges
    
# randomly generated edges
edges = generate_random_edges(V)
print("edges: ", edges)
E = len(edges)

# start and end vertices of path
start = int(input("start vertex: "))
end   = int(input("end   vertex: ")) 
# no. of candidates
C = int(input("No. of candidates: "))
# candidate edge array
cands = [[0]*E for i in range(C)]

def assign_vals(cand, V):
    idx = random.sample(range(len(cand)), V-1)
    for i in idx:
        cand[i] = 1

threads = []
for c in cands:
    th = threading.Thread(target=assign_vals, args=(c, V))
    threads.append(th)
    th.start()
for th in threads:
    th.join()
    
def get_fitness(path, start, end, vis):
    if start == end:
        return 0
    vis.add(start)
    min_fit = float('inf')
    for v, w in path[start]:
        if v in vis:
            continue
        min_fit = min(min_fit, get_fitness(path, v, end, vis) + w)
    return min_fit
    
def check_path(cand, edges, start, end, fits):
    path = defaultdict(list)
    for c in range(len(cand)):
        if cand[c]:
            u, v, w = edges[c]
            path[u].append((v, w))
            path[v].append((u, w))
    if end not in path:
        fits.append(float('inf'))
        return
    fits.append(get_fitness(path, start, end, set()))
    
# calcualting initial fitnesses
print("initial candidate edges and fitnesses:")
fitness = []
for c in cands:
    check_path(c, edges, start, end, fitness)
    print(*c, "\tfitness: %.2f"%fitness[-1], sep="")

def do_crossover(cands, fits):
    """
    first sorts the candidates based on fitness and then crosses-over ith and (N-i)th candidate
    """
    sorted_cands = [i[0] for i in sorted(zip(cands, fits), key = lambda i:i[1])]
    S = len(sorted_cands)
    for i in range(S//2):
        pt = random.randint(1, E-2)
        cands[i] = sorted_cands[i][:pt] + sorted_cands[S-i-1][pt:]
        cands[S-i-1] = sorted_cands[S-i-1][:pt] + sorted_cands[i][pt:]

# Run the main genetic algorithm
min_fitness = float('inf')
best_cand = None
rep_count = 0       # repetition count
for i in range(1000):       # perform 1000 iters
    fits = list()
    threads = list()
    for c in cands:
        th = threading.Thread(target=check_path, args=(c, edges, start, end, fits))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
        
    mincand, min_fit = min(zip(cands, fits), key=lambda i:i[1])
    if math.isclose(min_fit, min_fitness, rel_tol=0.1):
        rep_count += 1
    else:
        rep_count = 0
    if min_fit < min_fitness:
        min_fitness = min_fit
        best_cand = mincand
    if i%10 == 0:
        print("Minimum fitness in iteration %2d: %.2f"%(i, min_fit))
    if rep_count == 20:     # if repeated value for 20 iters than break
        break
    do_crossover(cands, fits)
    
print("Final candidates after GA search")
for i in range(len(cands)):
    print(*cands[i], "\tfitness: %.2f"%fits[i], sep="")
    
print("\nBest candidate edge array:\n",*best_cand, "\tfitness: %.2f"%min_fitness, sep="")
