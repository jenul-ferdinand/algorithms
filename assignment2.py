from typing import List
from collections import deque

ClassNumber = int
Allocation = List[ClassNumber]

class Dinic:
    def __init__(self, node_count: int):
        self.node_count = node_count
        self.graph = [[] for _ in range(node_count)]
        
    def add_edge(self, src: int, dst: int, capacity: int) -> None:
        # forward edge
        self.graph[src].append([dst, capacity, len(self.graph[dst])])
        # backward (residual) edge
        self.graph[dst].append([src, 0, len(self.graph[src]) - 1])
        
    def bfs(self, source: int, sink: int) -> bool:
        level_list = [-1] * self.node_count
        queue = deque([source])
        level_list[source] = 0
        while queue:
            u_node = queue.popleft()
            for v_node, cap, _ in self.graph[u_node]:
                if cap > 0 and level_list[v_node] < 0:
                    level_list[v_node] = level_list[u_node] + 1
                    queue.append(v_node)
        self.level_list = level_list
        return level_list[sink] >= 0
    
    def dfs(self, current: int, target: int, flow: int) -> int:
        if current == target:
            return flow
        for i in range(self.iter_ptr[current], len(self.graph[current])):
            v_node, cap, rev = self.graph[current][i]
            if cap > 0 and self.level_list[v_node] == self.level_list[current] + 1:
                pushed = self.dfs(v_node, target, min(flow, cap))
                if pushed > 0:
                    # decrease forward cap, increase backward cap
                    self.graph[current][i][1] -= pushed
                    self.graph[v_node][rev][1] += pushed
                    return pushed
            self.iter_ptr[current] += 1
        return 0
    
    def max_flow(self, source: int, sink: int) -> int:
        total_flow = 0
        INF = 10**18
        # Repeatedly build level graph and send blocking flow
        while self.bfs(source, sink):
            self.iter_ptr = [0] * self.node_count
            pushed = self.dfs(source, sink, INF)
            while pushed > 0:
                total_flow += pushed
                pushed = self.dfs(source, sink, INF)
        return total_flow
  
def crowdedCampus(
    num_students: int,
    num_classes: int,
    time_preferences: List[List[int]],
    proposed_classes: List[List[int]],
    min_satisfaction: int
) -> Allocation:
    # Phase 1: try to satisfy as many “top-5” allocations as possible
    phase1_node_count = num_students + num_classes + 2
    phase1_source      = num_students + num_classes
    phase1_sink        = num_students + num_classes + 1
    dinic_phase1       = Dinic(phase1_node_count)

    #  1. source -> each student (must send exactly 1 unit)
    for student in range(num_students):
        dinic_phase1.add_edge(phase1_source, student, 1)

    #  2. student -> class edges *only* if class time in student’s top-5
    for student in range(num_students):
        for cls in range(num_classes):
            class_time = proposed_classes[cls][0]
            # check top-5
            for rank in range(5):
                if time_preferences[student][rank] == class_time:
                    dinic_phase1.add_edge(student, num_students + cls, 1)
                    break

    #  3. class -> sink with capacity = max_j
    class_minimums = [pc[1] for pc in proposed_classes]
    class_maximums = [pc[2] for pc in proposed_classes]
    for cls in range(num_classes):
        dinic_phase1.add_edge(num_students + cls, phase1_sink, class_maximums[cls])

    # run flow
    flow_phase1 = dinic_phase1.max_flow(phase1_source, phase1_sink)
    if flow_phase1 < min_satisfaction:
        return None

    # Record which students got “top-5” slots and how many each class filled
    allocation     = [-1] * num_students
    class_filled   = [0]  * num_classes
    for student in range(num_students):
        for v_node, cap, _ in dinic_phase1.graph[student]:
            if num_students <= v_node < num_students + num_classes and cap == 0:
                cls = v_node - num_students
                allocation[student] = cls
                class_filled[cls]  += 1
                break

    # Who’s still unassigned?
    remaining_students = [s for s in range(num_students) if allocation[s] < 0]
    # Adjust each class’s lower/upper bounds
    remaining_class_minimums = [
        max(class_minimums[cls] - class_filled[cls], 0)
        for cls in range(num_classes)
    ]
    remaining_class_maximums = [
        class_maximums[cls] - class_filled[cls]
        for cls in range(num_classes)
    ]

    # Phase 2: handle remaining students + enforce [new_min, new_max] per class
    num_remain   = len(remaining_students)
    phase2_source = 0
    student_offset = 1
    class_offset   = student_offset + num_remain
    phase2_sink    = class_offset   + num_classes
    super_source   = phase2_sink    + 1
    super_sink     = super_source   + 1

    dinic_phase2 = Dinic(super_sink + 1)
    node_demands = [0] * (super_sink + 1)
    student_class_edges = []  # to reconstruct assignments

    # 1. phase2_source -> each remaining student with lower=upper=1
    for rem_idx, student in enumerate(remaining_students):
        u = phase2_source
        v = student_offset + rem_idx
        lower = 1; upper = 1
        dinic_phase2.add_edge(u, v, upper - lower)
        node_demands[u] -= lower
        node_demands[v] += lower

    # 2. remaining student -> every class (capacity=1)
    for rem_idx, student in enumerate(remaining_students):
        u = student_offset + rem_idx
        for cls in range(num_classes):
            v = class_offset + cls
            dinic_phase2.add_edge(u, v, 1)
            student_class_edges.append((student, cls, u, len(dinic_phase2.graph[u]) - 1))

    # 3. class -> phase2_sink with [new_min, new_max]
    for cls in range(num_classes):
        u = class_offset + cls
        v = phase2_sink
        lower = remaining_class_minimums[cls]
        upper = remaining_class_maximums[cls]
        dinic_phase2.add_edge(u, v, upper - lower)
        node_demands[u] -= lower
        node_demands[v] += lower

    # 4. super-source / super-sink to satisfy demands
    total_demand = 0
    for node in range(super_sink + 1):
        demand = node_demands[node]
        if demand > 0:
            dinic_phase2.add_edge(super_source, node, demand)
            total_demand += demand
        elif demand < 0:
            dinic_phase2.add_edge(node, super_sink, -demand)

    if dinic_phase2.max_flow(super_source, super_sink) != total_demand:
        return None

    # Extract final assignments for the remaining students
    for orig_student, cls, u, edge_idx in student_class_edges:
        # if that edge is fully used, we assigned orig_student → cls
        if dinic_phase2.graph[u][edge_idx][1] == 0:
            allocation[orig_student] = cls

    return allocation


if __name__ == '__main__':
    # Simple single student/class
    n = 1
    prefs = [[0] + list(range(1, 20))]
    classes = [[0, 1, 1]]  # time=0, min=1, max=1
    assert crowdedCampus(n, len(classes), prefs, classes, 1) == [0]

    # Two students, one class, both satisfied (min_satisfaction=1)
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
    assert result == [0, 0, 1]

    # Infeasible due to min occupancy > students
    n = 1
    prefs = [[5,0,1,2,3] + list(range(6,20))]
    classes = [[5, 2, 2]]
    assert crowdedCampus(n, len(classes), prefs, classes, 0) is None

    print("All tests passed!")
