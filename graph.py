from vertice import Vertice

class Graph():

    def __init__(self, showplaces=[], tiles={}) -> None:
        self.vertices = []
        for v in tiles:
            is_sp = False
            pair = 0
            for sp in showplaces:
                if v in sp:
                    is_sp = True
                    pair = sp[sp.index(v)-1]
            edges = tiles[v]
            for i in range(len(edges)):
                edges[i] = [edges[i], 1]
            self.vertices.append(
                Vertice(v, edges, is_sp, pair)
            )
        self.subs = []
        self.showplaces = len(showplaces)
    
    def find_not_connected_points(self):
        X = [self.vertices[0].id]
        short_a = X[0]
        while short_a != 0:
            d = 100
            short_a = 0
            short_b = 0
            for name in X:
                v = self.vertice_value_by_id(name)
                if v is None:
                    continue
                for p, l in v.edges:
                    if p in X:
                        continue
                    if l < d:
                        d = l
                        short_b = p
                        short_a = name
                        X.append(short_b)
        connected = []
        out = []
        for v in self.vertices:
            if v.id in X:
                connected.append(v)
            else:
                out.append(v)
        return connected, out

    def divide_graphs(self):
        graphs = []
        connected, out = self.find_not_connected_points()
        gr = Graph()
        gr.vertices = connected
        rest = Graph()
        rest.vertices = out
        graphs.append(gr)
        while len(out) > 0:
            connected, out = rest.find_not_connected_points()
            gr = Graph()
            gr.vertices = connected
            rest = Graph()
            rest.vertices = out
            graphs.append(gr)
        for gr in graphs:
            gr.showplaces = 0
            p = 0
            u = 0
            for v in gr.vertices:
                if v.is_sp and v.pair == 0:
                    u += 1
                elif v.is_sp:
                    p += 1
            gr.showplaces = u + p//2
        self.vertices = graphs[0].vertices
        self.showplaces = graphs[0].showplaces
        for i in range(1, len(graphs)):
            self.subs.append(graphs[i])

    def vertice_value_by_id(self, v_id) -> Vertice:
        for v in self.vertices:
            if v_id == v.id:
                return v
        for gr in self.subs:
            if gr.vertice_value_by_id(v_id) is not None:
                return gr.vertice_value_by_id(v_id)
    
    def vertice_index_by_id(self, v_id) -> int:
        for v in range(len(self.vertices)):
            if v_id == self.vertices[v].id:
                return v
    
    def has_leafs(self):
        for v in self.vertices:
            if len(v.edges) > 1:
                continue
            if not v.is_sp and v.pair == 0:
                return True
            other = self.vertice_value_by_id(v.pair)
            if other is None:
                continue
            if len(v.edges) < len(self.vertice_value_by_id(v.pair).edges):
                return True
        return False
    
    def remove_node(self, v_id):
        vertice = self.vertice_value_by_id(v_id)
        for id, length in vertice.edges:
            node = self.vertice_value_by_id(id)
            if node is None:
                continue
            node.edges.remove([v_id, length])
        if vertice.is_sp:
            node = self.vertice_value_by_id(vertice.pair)
            node.pair = 0
        del self.vertices[self.vertice_index_by_id(v_id)]
        vertice.clear()
    
    def remove_edge(self, v1, v2):
        v = self.vertice_value_by_id(v1)
        for p, l in v.edges:
            if p == v2:
                v.edges.remove([p, l])
        v = self.vertice_value_by_id(v2)
        for p, l in v.edges:
            if p == v1:
                v.edges.remove([p, l])

    def simplify(self):
        while self.has_leafs():
            for v in self.vertices:
                if len(v.edges) > 1:
                    continue
                elif len(v.edges) == 1:
                    if not v.is_sp:
                        self.remove_node(v.id)
                    else:
                        if v.pair == 0:
                            continue
                        other = self.vertice_value_by_id(v.pair)
                        if other is None:
                            continue
                        if len(other.edges) == 0:
                            self.remove_node(other.id)
                        elif len(other.edges) > len(v.edges):
                            self.remove_node(v.id)
                else:
                    if not v.is_sp or v.pair != 0:
                        self.remove_node(v.id)

    def __str__(self) -> str:
        string = ''
        for v in self.vertices:
            string += str(v)
            string += '\n'
        return string
    
    def find_path(self, v_id: int):
        unvisited_nodes = []
        for v in self.vertices:
            unvisited_nodes.append(v.id)
        shortest_path = {}
        previous_nodes = {v_id: 0}
        for node in unvisited_nodes:
            shortest_path[node] = 1000
        shortest_path[v_id] = 0

        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes:
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
                neighbours = self.vertice_value_by_id(current_min_node).edges
                for p, l in neighbours:
                    tentative = shortest_path[current_min_node] + l
                    if tentative < shortest_path[p]:
                        shortest_path[p] = tentative
                        previous_nodes[p] = current_min_node
            unvisited_nodes.remove(current_min_node)
        return shortest_path, previous_nodes

    def has_pairs(self) -> bool:
        for v in self.vertices:
            if v.pair != 0:
                return True
        return False

    def nearest_showplace(self, v_id, unique=False) -> int:
        lens, _ = self.find_path(v_id)
        dist = 100
        it = self.vertice_value_by_id(v_id)
        for i in lens:
            if i == v_id:
                continue
            node = self.vertice_value_by_id(i)
            if node.is_sp and it.pair != node.id and lens[i] < dist:
                if not unique:
                    dist = lens[i]
                else:
                    if node.pair == 0:
                        dist = lens[i]
        return dist

    def copy(self):
        gr = Graph()
        for v in self.vertices:
            gr.vertices.append(v.copy())
        return gr

    def delete_safely(self, v_id) -> bool:
        gr = self.copy()
        gr.remove_node(v_id)
        _, out = gr.find_not_connected_points()
        return len(out) == 0

    def remove_pairs_by_priority(self, priority):
        for v in self.vertices:
            if not v.is_sp or v.pair == 0:
                continue
            pair = self.vertice_value_by_id(v.pair)
            if pair is None:
                continue
            remove = 0
            match priority:
                case 1:
                    it_nearest = self.nearest_showplace(v.id)
                    other_nearest = self.nearest_showplace(pair.id)
                    if it_nearest < other_nearest:
                        remove = 2
                    elif it_nearest > other_nearest:
                        remove = 1                    
                case 2:
                    connected = False
                    for p, _ in v.edges:
                        if p == pair.id:
                            connected = True
                    safe = True
                    if connected:
                        gr = self.copy()
                        gr.remove_edge(v.id, pair.id)
                        con, out = gr.find_not_connected_points()
                        safe = len(out) == 0
                    if not safe:
                        if v.id in con:
                            grv = len(con)
                            grp = len(out)
                        else:
                            grv = len(out)
                            grp = len(con)
                        if grv > grp:
                            remove = 2
                        elif grv < grp:
                            remove = 1
                case 3:
                    it_nearest = self.nearest_showplace(v.id, True)
                    other_nearest = self.nearest_showplace(pair.id, True)
                    if it_nearest < other_nearest:
                        remove = 2
                    elif it_nearest > other_nearest:
                        remove = 1
            
            match remove:
                case 1:
                    if self.delete_safely(v.id):
                        self.remove_node(v.id)
                    v.is_sp = False
                    v.pair = 0
                    pair.pair = 0
                case 2:
                    if self.delete_safely(pair.id):
                        self.remove_node(pair.id)
                    pair.is_sp = False
                    pair.pair = 0
                    v.pair = 0

    def remove_pairs(self):
        for i in range(1, 4):
            self.remove_pairs_by_priority(i)
            self.simplify()
        for gr in self.subs:
            gr.remove_pairs()
    
    def remove_extra_vertices(self):
        for v in self.vertices:
            for point, length in v.edges:
                node = self.vertice_value_by_id(point)
                if node.is_sp:
                    continue
                if len(node.edges) == 2:
                    ind = node.edges.index([v.id, length])
                    other = self.vertice_value_by_id(node.edges[abs(ind-1)][0])
                    l=0
                    for p, dist in other.edges:
                        if p == node.id:
                            l = dist
                    self.remove_node(point)
                    v.edges.append([other.id, length+l])
                    other.edges.append([v.id, length+l])

    def minimum_spanning_tree(self):
        edges = []
        X = [self.vertices[0]]
        while len(edges) < len(self.vertices)-1:
            cur_min = 100
            for v in self.vertices:
                if v in X:
                    for p, l in v.edges:
                        node = self.vertice_value_by_id(p)
                        if node not in X and l < cur_min:
                            cur_min = l
                            cur_a = v
                            cur_b = node
            X.append(cur_b)
            edges.append((min(cur_a.id, cur_b.id), max(cur_a.id, cur_b.id), cur_min))
        return edges
    
    def has_edge(self, v1, v2):
        vert = self.vertice_value_by_id(v1)
        for p, l in vert.edges:
            if p == v2:
                return True
        return False

    def safe_delete_on_distance(self, edge: tuple) -> bool:
        v1, v2, _ = edge
        removed = self.copy()
        removed.remove_edge(v1, v2)
        return removed.shortest_distance() <= self.shortest_distance()

    def remove_extra_edges(self):
        
        checked_edges = []
        done = False
        while len(self.vertices) > self.count_showplaces() and not done:
            prev_vert = 100
            while self.count_vertices() < prev_vert:
                prev_vert = self.count_vertices()
                self.remove_extra_vertices()

            edges = self.minimum_spanning_tree()
            extra=0
            for v in self.vertices:
                for p, l in v.edges:
                    edge = (min(v.id, p), max(v.id, p), l)
                    if edge not in edges:
                        if edge not in checked_edges:
                            extra += 1
                        if self.safe_delete_on_distance(edge):
                            self.remove_edge(v.id, p)
                        checked_edges.append(edge)
            done = extra==0
            self.simplify()
        for gr in self.subs:
            gr.remove_extra_edges()

    def endpoints_order(self, extra: list) -> list:
        points = []
        for v in self.vertices:
            if len(v.edges) < 2:
                points.append(v.id)
        points += extra
        visited = [points[0]]
        while len(visited) < len(points):
            p = visited[-1]
            dist = 100
            point = 0
            for other in points:
                if other not in visited and p != other:
                    d, _ = self.dist_between_points(p, other)
                    if d < dist:
                        dist = d
                        point = other
            visited.append(point)
        return visited
    
    def shortest_distance(self) -> int:
        all_checked = False
        showplaces = []
        extra = []
        for v in self.vertices:
            if v.is_sp:
                showplaces.append(v.id)
        while not all_checked:
            order = self.endpoints_order(extra)
            distance = 0
            path = str(order[0])
            visited = [order[0]]
            for i in range(len(order)-1):
                d, p = self.dist_between_points(order[i], order[i+1])
                p = p[1:]
                distance += d
                for each in p:
                    visited.append(each)
                    path += f' -> {each}'
            all_checked = True
            for s in showplaces:
                if s not in visited:
                    extra.append(s)
                    all_checked = False
        return distance, path

    
    def dist_between_points(self, v1:int, v2:int) -> int:
        ds, ps = self.find_path(v1)
        cur = v1
        path = []
        prev = ps[v2]
        while prev != v1:
            cur = prev
            path.append(prev)
            prev = ps[cur]
        path.append(v1)
        path.reverse()
        path.append(v2)
        return ds[v2], path
    
    def index_variants(self, dec: int) -> list:
        variants = []
        for i in range(dec):
            binary = str(bin(i))[2:]
            binary = '0'*(self.count_showplaces()-self.showplaces-len(binary))+binary
            variants.append(binary)
        return variants

    def variants(self):
        gr_counter = 2 ** (self.count_showplaces()-self.showplaces)
        if gr_counter == 1:
            return []
        variants = self.index_variants(gr_counter)
        graphs = []
        pairs = self.all_pairs()
        for i in range(gr_counter):
            gr = self.copy()
            for ind in range(len(variants[i])):
                index = gr.vertice_index_by_id(pairs[ind][int(variants[i][ind])])
                gr.vertices[index].is_sp = False
                gr.vertices[index].pair = 0
            gr.simplify()
            gr.remove_extra_edges()
            graphs.append(gr)
        return graphs

    def all_pairs(self) -> list:
        checked = []
        result = []
        for v in self.vertices:
            if v.is_sp and v.pair != 0 and v.id not in checked:
                checked.append(v.id)
                checked.append(v.pair)
                result.append((v.id, v.pair))
        for gr in self.subs:
            for each in gr.all_pairs():
                result.append(each)
        return result

    def count_vertices(self) -> int:
        c = len(self.vertices)
        for gr in self.subs:
            c += gr.count_vertices()
        return c

    def count_showplaces(self) -> int:
        c = 0
        for v in self.vertices:
            if v.is_sp:
                c += 1
        return c
    
    def calculate(self):
        self.simplify()
        self.divide_graphs()
        self.remove_pairs()
        self.remove_extra_edges()
        d, p = self.shortest_distance()
        return d, p