from typing import List
from collections import deque

ClassNumber = int
Allocation = List[ClassNumber]

class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.g = [[] for _ in range(n)]
        
    def add_edge(self, fr: int, to: int, cap: int) -> None:
        self.g[fr].append([to, cap, len(self.g[to])])
        self.g[to].append([fr, 0, len(self.g[fr]) - 1])
        
    def bfs(self, s: int, t: int) -> bool:
        level = [-1] * self.n
        queue = deque([s])
        level[s] = 0
        while queue:
            u = queue.popleft()
            for v, cap, _ in self.g[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        self.level = level
        return level[t] >= 0
    
    def dfs(self, u: int, t: int, f: int) -> int:
        if u == t:
            return f
        for i in range(self.it[u], len(self.g[u])):
            v, cap, rev = self.g[u][i]
            if cap > 0 and self.level[v] == self.level[u] + 1:
                ret = self.dfs(v, t, min(f, cap))
                if ret > 0:
                    self.g[u][i][1] -= ret
                    self.g[v][rev][1] += ret
                    return ret
            self.it[u] += 1
        return 0
    
    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        INF = 10**18
        while self.bfs(s, t):
            self.it = [0] * self.n
            f = self.dfs(s, t, INF)
            while f > 0:
                flow += f
                f = self.dfs(s, t, INF)
        return flow
  
def crowdedCampus(
    no_students: int,
    no_classes: int,
    time_prefs: List[List[int]],
    proposed_classes: List[List[int]],
    min_satisfaction: int
) -> Allocation:
    """
    
    Args:
        - no_students: Number of students taking FIT2004.
        - no_classes: Number of classes available for FIT2004.
        - time_prefs: List of students' time preferences, time_prefs[i] is a list 
        of times for student i, sorted in preference order, with the first element
        being the most preferred time.
        - proposed_classes: List of lists, where 
    """
    n = no_students
    m = no_classes

    # Phase 1: allocate up to min_satisfaction students to top-5 slots
    N1 = n + m + 2
    s1 = n + m
    t1 = n + m + 1
    dinic1 = Dinic(N1)

    # Source -> each student (1 unit exactly)
    for i in range(n):
        dinic1.add_edge(s1, i, 1)

    # Students -> classes if class time in top-5
    for i in range(n):
        for j in range(m):
            ts = proposed_classes[j][0]
            # check top-5 preferences
            for k in range(5):
                if time_prefs[i][k] == ts:
                    dinic1.add_edge(i, n + j, 1)
                    break

    # Classes -> sink (capacity = max_j)
    max_j_list = [pc[2] for pc in proposed_classes]
    min_j_list = [pc[1] for pc in proposed_classes]
    for j in range(m):
        dinic1.add_edge(n + j, t1, max_j_list[j])

    flow1 = dinic1.max_flow(s1, t1)
    if flow1 < min_satisfaction:
        return None

    # Record partial allocation and remaining capacities
    allocation = [-1] * n
    filled = [0] * m
    for i in range(n):
        for v, cap, _ in dinic1.g[i]:
            if n <= v < n + m and cap == 0:
                j = v - n
                allocation[i] = j
                filled[j] += 1
                break

    remain = [i for i in range(n) if allocation[i] < 0]
    new_min = [max(min_j_list[j] - filled[j], 0) for j in range(m)]
    new_max = [max_j_list[j] - filled[j] for j in range(m)]

    # Phase 2: circulation with lower bounds for remaining students
    n2 = len(remain)
    s2 = 0
    off_u = 1
    off_c = off_u + n2
    t2 = off_c + m
    S = t2 + 1
    T = S + 1
    dinic2 = Dinic(T + 1)
    demand = [0] * (T + 1)
    edges_info = []

    # S2 -> each remaining student (1 unit exactly)
    for idx, i in enumerate(remain):
        u = s2
        v = off_u + idx
        l = 1; ucap = 1
        dinic2.add_edge(u, v, ucap - l)
        demand[u] -= l
        demand[v] += l

    # Students -> classes (0..1)
    for idx, i in enumerate(remain):
        u = off_u + idx
        for j in range(m):
            v = off_c + j
            dinic2.add_edge(u, v, 1)
            edges_info.append((i, j, u, len(dinic2.g[u]) - 1))

    # Classes -> t2 with [new_min, new_max]
    for j in range(m):
        u = off_c + j
        v = t2
        l = new_min[j]; ucap = new_max[j]
        dinic2.add_edge(u, v, ucap - l)
        demand[u] -= l
        demand[v] += l

    # Super-source S and super-sink T for demands
    total_demand = 0
    for v in range(T + 1):
        if demand[v] > 0:
            dinic2.add_edge(S, v, demand[v])
            total_demand += demand[v]
        elif demand[v] < 0:
            dinic2.add_edge(v, T, -demand[v])

    if dinic2.max_flow(S, T) != total_demand:
        return None

    # Extract assignments
    for orig_i, j, u, ei in edges_info:
        if dinic2.g[u][ei][1] == 0:
            allocation[orig_i] = j

    return allocation

if __name__ == '__main__':
    # Simple single student/class
    n = 1
    prefs = [[0] + list(range(1, 20))]
    classes = [[0, 1, 1]]  # time=0, min=1, max=1
    assert crowdedCampus(n, len(classes), prefs, classes, 1) == [0]

    # Two students, one class, enough capacity, both satisfied (min_satisfaction=1)
    n = 2
    prefs = [[0] + list(range(1,20)), [0] + list(range(1,20))]
    classes = [[0, 2, 2]]
    assert crowdedCampus(n, len(classes), prefs, classes, 1) == [0, 0]

    # Satisfaction unattainable (class time not in top-5)
    n = 2
    prefs = [[1,0,2,3,4] + list(range(5,20)), [1,0,2,3,4] + list(range(5,20))]
    classes = [[5, 2, 2]]
    assert crowdedCampus(n, len(classes), prefs, classes, 2) is None

    # Satisfaction attainable with higher threshold (min_satisfaction=2)
    classes = [[0, 2, 2]]  # time=0 is in top-5 for both
    assert crowdedCampus(n, len(classes), prefs, classes, 2) == [0, 0]

    # Two students, two classes, exact matching
    n = 2
    prefs = [[0,1,2,3,4] + list(range(5,20)), [1,0,2,3,4] + list(range(5,20))]
    classes = [[0,1,1], [1,1,1]]
    alloc = crowdedCampus(n, len(classes), prefs, classes, 2)
    assert alloc == [0, 1]

    # Three students, two classes, mixed min/max
    n = 3
    prefs = [
        [0,1,2,3,4] + list(range(5,20)),
        [0,1,2,3,4] + list(range(5,20)),
        [1,0,2,3,4] + list(range(5,20))
    ]
    classes = [[0,2,2], [1,1,2]]
    result = crowdedCampus(n, len(classes), prefs, classes, 2)
    # Two of the three must be in top-5, class capacities force [0,0,1]
    assert result == [0, 0, 1]

    # Infeasible due to min occupancy > students
    n = 1
    prefs = [[5,0,1,2,3] + list(range(6,20))]
    classes = [[5, 2, 2]]
    assert crowdedCampus(n, len(classes), prefs, classes, 0) is None

    print("All tests passed!")
