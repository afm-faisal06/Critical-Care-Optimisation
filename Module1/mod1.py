# Module 1: Graph-Based Hospital Navigation (Interactive input filename)


import sys

# Linked List Structures
class DSALinkedList:
    class _Node:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_first(self, value):
        new_node = DSALinkedList._Node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size = self.size + 1

    def insert_last(self, value):
        new_node = DSALinkedList._Node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size = self.size + 1

    def remove_first(self):
        if self.is_empty():
            raise IndexError("List is empty")
        val = self.head.value
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size = self.size - 1
        return val

    def peek_first(self):
        if self.is_empty():
            raise IndexError("List is empty")
        return self.head.value

    def remove_node(self, value):
        current = self.head
        found = False
        while (current is not None) and (not found):
            if current.value == value:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size = self.size - 1
                found = True
            else:
                current = current.next
        return found

    def contains(self, value):
        current = self.head
        present = False
        while (current is not None) and (not present):
            if current.value == value:
                present = True
            else:
                current = current.next
        return present

    def __len__(self):
        return self.size


class DSAStack:
    def __init__(self):
        self._list = DSALinkedList()

    def is_empty(self):
        return self._list.is_empty()

    def push(self, value):
        self._list.insert_first(value)

    def pop(self):
        return self._list.remove_first()

    def top(self):
        return self._list.peek_first()


class DSAQueue:
    def __init__(self):
        self._list = DSALinkedList()

    def is_empty(self):
        return self._list.is_empty()

    def enqueue(self, value):
        self._list.insert_last(value)

    def dequeue(self):
        return self._list.remove_first()


# Min Priority Queue (ordered linked list)
class _PQItem:
    def __init__(self, key, priority):
        self.key = key
        self.priority = priority

class DSAMinPriorityQueue:
    def __init__(self):
        self._list = DSALinkedList()

    def is_empty(self):
        return self._list.is_empty()

    def insert(self, key, priority):
        item = _PQItem(key, priority)
        if self._list.is_empty():
            self._list.insert_last(item)
        else:
            cur = self._list.head
            inserted = False
            while (cur is not None) and (not inserted):
                if priority < cur.value.priority:
                    new_node = DSALinkedList._Node(item)
                    new_node.next = cur
                    new_node.prev = cur.prev
                    if cur.prev is not None:
                        cur.prev.next = new_node
                    else:
                        self._list.head = new_node
                    cur.prev = new_node
                    self._list.size = self._list.size + 1
                    inserted = True
                else:
                    cur = cur.next
            if not inserted:
                self._list.insert_last(item)

    def pop_min(self):
        return self._list.remove_first().key



# Graph (Weighted Undirected)
class _Edge:
    def __init__(self, to_vertex, weight):
        self.to = to_vertex
        self.weight = weight

class DSAGraphVertex:
    def __init__(self, label, x=None, y=None):
        self.label = label
        self.x = x
        self.y = y
        self.visited = False
        self.parent = None
        self.adjacent = DSALinkedList()
        self.g = 0.0
        self.h = 0.0
        self.f = 0.0

    def add_edge(self, vertex, weight):
        if not self._has_edge_to(vertex):
            self.adjacent.insert_last(_Edge(vertex, weight))

    def _has_edge_to(self, vertex):
        cur = self.adjacent.head
        found = False
        while (cur is not None) and (not found):
            if cur.value.to == vertex:
                found = True
            else:
                cur = cur.next
        return found

class DSAGraphWeighted:
    def __init__(self):
        self.vertices = DSALinkedList()

    def find_vertex(self, label):
        cur = self.vertices.head
        found = None
        while (cur is not None) and (found is None):
            if cur.value.label == label:
                found = cur.value
            else:
                cur = cur.next
        return found

    def add_vertex(self, label, x=None, y=None):
        if self.find_vertex(label) is not None:
            raise ValueError("Vertex already exists: " + label)
        self.vertices.insert_last(DSAGraphVertex(label, x, y))

    def add_edge(self, a, b, w):
        if a == b:
            raise ValueError("Self edge not allowed")
        va = self.find_vertex(a)
        vb = self.find_vertex(b)
        if (va is None) or (vb is None):
            raise ValueError("Vertex missing for edge " + a + "-" + b)
        if va._has_edge_to(vb):
            raise ValueError("Edge already exists between " + a + " and " + b)
        va.add_edge(vb, w)
        vb.add_edge(va, w)

    # sorting helpers (alphabetical by label)
    def _sorted_vertices(self):
        out = DSALinkedList()
        cur = self.vertices.head
        while cur is not None:
            v = cur.value
            if out.is_empty():
                out.insert_first(v)
            else:
                s = out.head
                inserted = False
                while (s is not None) and (not inserted):
                    if v.label < s.value.label:
                        node = DSALinkedList._Node(v)
                        node.next = s
                        node.prev = s.prev
                        if s.prev is not None:
                            s.prev.next = node
                        else:
                            out.head = node
                        s.prev = node
                        out.size = out.size + 1
                        inserted = True
                    else:
                        s = s.next
                if not inserted:
                    out.insert_last(v)
            cur = cur.next
        return out

    def _sorted_edges(self, vertex):
        out = DSALinkedList()
        cur = vertex.adjacent.head
        while cur is not None:
            e = cur.value
            if out.is_empty():
                out.insert_first(e)
            else:
                s = out.head
                inserted = False
                while (s is not None) and (not inserted):
                    if e.to.label < s.value.to.label:
                        node = DSALinkedList._Node(e)
                        node.next = s
                        node.prev = s.prev
                        if s.prev is not None:
                            s.prev.next = node
                        else:
                            out.head = node
                        s.prev = node
                        out.size = out.size + 1
                        inserted = True
                    else:
                        s = s.next
                if not inserted:
                    out.insert_last(e)
            cur = cur.next
        return out

    # outputs
    def write_adjacency_list(self, filepath):
        f = open(filepath, "w", encoding="utf-8")
        f.write("Adjacency List (weighted, undirected)\n")
        vcur = self._sorted_vertices().head
        while vcur is not None:
            v = vcur.value
            line = v.label + ": "
            ecur = self._sorted_edges(v).head
            first = True
            while ecur is not None:
                e = ecur.value
                if first:
                    line = line + e.to.label + "(" + str(e.weight) + ")"
                    first = False
                else:
                    line = line + " " + e.to.label + "(" + str(e.weight) + ")"
                ecur = ecur.next
            f.write(line + "\n")
            vcur = vcur.next
        f.close()

    # BFS with levels
    class _BFSItem:
        def __init__(self, vertex, level):
            self.vertex = vertex
            self.level = level

    def bfs_levels_to_file(self, start_label, filepath):
        s = self.find_vertex(start_label)
        if s is None:
            raise ValueError("BFS start not found: " + start_label)
        cur = self.vertices.head
        while cur is not None:
            cur.value.visited = False
            cur = cur.next
        q = DSAQueue()
        s.visited = True
        q.enqueue(DSAGraphWeighted._BFSItem(s, 0))
        f = open(filepath, "w", encoding="utf-8")
        f.write("BFS from " + start_label + " (grouped by levels)\n")
        lvl_now = -1
        first_in_level = True
        while not q.is_empty():
            it = q.dequeue()
            v = it.vertex
            lvl = it.level
            if lvl != lvl_now:
                if lvl_now != -1:
                    f.write("\n")
                f.write("Level " + str(lvl) + ": ")
                lvl_now = lvl
                first_in_level = True
            if not first_in_level:
                f.write(", ")
            f.write(v.label)
            first_in_level = False
            ecur = self._sorted_edges(v).head
            while ecur is not None:
                e = ecur.value
                if not e.to.visited:
                    e.to.visited = True
                    q.enqueue(DSAGraphWeighted._BFSItem(e.to, lvl + 1))
                ecur = ecur.next
        f.write("\n")
        f.close()

    # DFS cycle detection with members 
    class _DFSFrame:
        def __init__(self, vertex, parent, next_edge_node):
            self.vertex = vertex
            self.parent = parent
            self.next_edge_node = next_edge_node

    def _reset_search_fields(self):
        cur = self.vertices.head
        while cur is not None:
            v = cur.value
            v.visited = False
            v.parent = None
            v.g = 0.0
            v.h = 0.0
            v.f = 0.0
            cur = cur.next

    def _reconstruct_cycle(self, u, v):
        # collect ancestors of u
        anc = DSALinkedList()
        a = u
        while a is not None:
            anc.insert_last(a)
            a = a.parent
        # find LCA by scanning v upwards
        lca = None
        pv = v
        found = False
        while (pv is not None) and (not found):
            cur = anc.head
            match = None
            inside = False
            while (cur is not None) and (not inside):
                if cur.value == pv:
                    inside = True
                    match = pv
                else:
                    cur = cur.next
            if inside:
                lca = match
                found = True
            else:
                pv = pv.parent
        # build cycle list: u..lca, then reversed(v..lca)
        cyc = DSALinkedList()
        a2 = u
        while (a2 is not None) and (a2 != lca):
            cyc.insert_last(a2)
            a2 = a2.parent
        if lca is not None:
            cyc.insert_last(lca)
        st = DSAStack()
        b2 = v
        while (b2 is not None) and (b2 != lca):
            st.push(b2)
            b2 = b2.parent
        while not st.is_empty():
            cyc.insert_last(st.pop())
        return cyc

    def dfs_cycle_to_file(self, start_label, filepath):
        s = self.find_vertex(start_label)
        if s is None:
            raise ValueError("DFS start not found: " + start_label)
        self._reset_search_fields()
        st = DSAStack()
        s.visited = True
        st.push(DSAGraphWeighted._DFSFrame(s, None, self._sorted_edges(s).head))
        found = False
        cyc_list = None
        while (not st.is_empty()) and (not found):
            fr = st.top()
            node = fr.next_edge_node
            if node is None:
                st.pop()
            else:
                fr.next_edge_node = node.next
                e = node.value
                w = e.to
                if not w.visited:
                    w.visited = True
                    w.parent = fr.vertex
                    st.push(DSAGraphWeighted._DFSFrame(w, fr.vertex, self._sorted_edges(w).head))
                else:
                    if w != fr.parent:
                        found = True
                        cyc_list = self._reconstruct_cycle(fr.vertex, w)
        f = open(filepath, "w", encoding="utf-8")
        f.write("DFS Cycle Detection (undirected)\nStart: " + start_label + "\n")
        if found and (cyc_list is not None) and (not cyc_list.is_empty()):
            f.write("Cycle detected: YES\nMembers: ")
            c = cyc_list.head
            first = True
            while c is not None:
                if first:
                    f.write(c.value.label)
                    first = False
                else:
                    f.write(" -> " + c.value.label)
                c = c.next
            f.write("\n")
        else:
            f.write("Cycle detected: NO\n")
        f.close()

    # ----- A* -----
    def _manhattan(self, a, b):
        if (a is None) or (b is None):
            return 0.0
        if (a.x is None) or (a.y is None) or (b.x is None) or (b.y is None):
            return 0.0
        dx = a.x - b.x
        if dx < 0:
            dx = -dx
        dy = a.y - b.y
        if dy < 0:
            dy = -dy
        return float(dx + dy)

    def astar_to_file(self, start_label, goal_label, filepath):
        s = self.find_vertex(start_label)
        g = self.find_vertex(goal_label)
        if (s is None) or (g is None):
            raise ValueError("A* requires valid start and goal")
        self._reset_search_fields()
        open_set = DSAMinPriorityQueue()
        closed = DSALinkedList()
        s.g = 0.0
        s.h = self._manhattan(s, g)
        s.f = s.g + s.h
        s.parent = None
        open_set.insert(s, s.f)
        found = False
        while (not open_set.is_empty()) and (not found):
            cur = open_set.pop_min()
            if cur == g:
                found = True
            else:
                if not closed.contains(cur):
                    closed.insert_last(cur)
                ecur = self._sorted_edges(cur).head
                while ecur is not None:
                    e = ecur.value
                    nb = e.to
                    in_closed = closed.contains(nb)
                    if not in_closed:
                        tg = cur.g + float(e.weight)
                        better = False
                        if (nb.parent is None) and (nb != s):
                            better = True
                        else:
                            if tg < nb.g:
                                better = True
                        if better:
                            nb.parent = cur
                            nb.g = tg
                            nb.h = self._manhattan(nb, g)
                            nb.f = nb.g + nb.h
                            open_set.insert(nb, nb.f)
                    ecur = ecur.next
        f = open(filepath, "w", encoding="utf-8")
        f.write("A* Shortest Path\nFrom: " + start_label + " To: " + goal_label + "\n")
        if not found:
            f.write("No path found.\n")
        else:
            # reconstruct
            st = DSAStack()
            v = g
            while v is not None:
                st.push(v)
                v = v.parent
            f.write("Path: ")
            first = True
            while not st.is_empty():
                node = st.pop()
                if first:
                    f.write(node.label)
                    first = False
                else:
                    f.write(" -> " + node.label)
            # integer if whole number, else keep float
            total = g.g
            total_int = int(total)
            txt_cost = str(total_int) if (float(total_int) == float(total)) else str(total)
            f.write("\nTotal walking time: " + txt_cost + " minutes\n")
        f.close()



# Tokenizer (no split())
def tokenize(line):
    toks = DSALinkedList()
    piece = ""
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch.isspace():
            if len(piece) > 0:
                toks.insert_last(piece)
                piece = ""
        else:
            piece = piece + ch
        i = i + 1
    if len(piece) > 0:
        toks.insert_last(piece)
    return toks

def tokens_len(tokens):
    return len(tokens)

def token_at(tokens, idx):
    cur = tokens.head
    pos = 0
    while (cur is not None) and (pos < idx):
        cur = cur.next
        pos = pos + 1
    if cur is None:
        return None
    return cur.value



# I/O Driver
def process_input_file(infile):
    g = DSAGraphWeighted()
    bfs_src = None
    dfs_src = None
    a_src = None
    a_dst = None
    f = open(infile, "r", encoding="utf-8")
    try:
        for raw in f:
            line = raw.strip()
            if len(line) > 0:
                is_comment = False
                if len(line) >= 1:
                    if line[0:1] == "#":
                        is_comment = True
                if not is_comment:
                    toks = tokenize(line)
                    if tokens_len(toks) > 0:
                        cmd = token_at(toks, 0)
                        if cmd == "DEPT":
                            name = token_at(toks, 1)
                            x = None
                            y = None
                            if tokens_len(toks) >= 4:
                                xv = token_at(toks, 2)
                                yv = token_at(toks, 3)
                                ok = True
                                try:
                                    x = int(xv)
                                except:
                                    ok = False
                                if ok:
                                    try:
                                        y = int(yv)
                                    except:
                                        x = None
                                        y = None
                                else:
                                    x = None
                                    y = None
                            g.add_vertex(name, x, y)
                        elif cmd == "EDGE":
                            a = token_at(toks, 1)
                            b = token_at(toks, 2)
                            w = int(token_at(toks, 3))
                            g.add_edge(a, b, w)
                        elif cmd == "BFS":
                            bfs_src = token_at(toks, 1)
                        elif cmd == "DFS":
                            dfs_src = token_at(toks, 1)
                        elif cmd == "ASTAR":
                            a_src = token_at(toks, 1)
                            a_dst = token_at(toks, 2)
                        else:
                            # unknown line: ignore safely
                            pass
    finally:
        f.close()

    # Always create all four outputs, even if the corresponding query is missing.
    g.write_adjacency_list("output_graph.txt")

    if bfs_src is not None:
        g.bfs_levels_to_file(bfs_src, "output_bfs.txt")
    else:
        fb = open("output_bfs.txt", "w", encoding="utf-8")
        fb.write("BFS: no source provided in input.\n")
        fb.close()

    if dfs_src is not None:
        g.dfs_cycle_to_file(dfs_src, "output_dfs.txt")
    else:
        fd = open("output_dfs.txt", "w", encoding="utf-8")
        fd.write("DFS: no source provided in input.\n")
        fd.close()

    if (a_src is not None) and (a_dst is not None):
        g.astar_to_file(a_src, a_dst, "output_astar.txt")
    else:
        fa = open("output_astar.txt", "w", encoding="utf-8")
        fa.write("A*: source/destination not fully provided in input.\n")
        fa.close()

    print("Done. Wrote output_graph.txt, output_bfs.txt, output_dfs.txt, output_astar.txt")



# Demo generator
def write_demo_input(path):
    out = open(path, "w", encoding="utf-8")
    try:
        out.write("# Demo Hospital Map\n")
        out.write("DEPT Emergency 0 0\n")
        out.write("DEPT ICU 0 3\n")
        out.write("DEPT Pharmacy 2 1\n")
        out.write("DEPT Radiology 3 2\n")
        out.write("DEPT Labs 1 4\n")
        out.write("DEPT Theatres 4 1\n")
        out.write("DEPT Wards 2 4\n")
        out.write("DEPT Outpatient 5 3\n")
        out.write("DEPT Isolation 10 10\n")
        out.write("EDGE Emergency ICU 4\n")
        out.write("EDGE Emergency Pharmacy 3\n")
        out.write("EDGE Pharmacy Radiology 2\n")
        out.write("EDGE ICU Labs 2\n")
        out.write("EDGE Radiology Theatres 3\n")
        out.write("EDGE Labs Wards 2\n")
        out.write("EDGE Pharmacy Wards 5\n")
        out.write("EDGE Wards Radiology 3\n")
        out.write("EDGE Theatres Outpatient 4\n")
        out.write("EDGE ICU Pharmacy 3\n")
        out.write("EDGE Labs Radiology 4\n")
        out.write("EDGE Emergency Labs 7\n")
        out.write("BFS Emergency\n")
        out.write("DFS Emergency\n")
        out.write("ASTAR Emergency Outpatient\n")
    finally:
        out.close()


# Main (interactive prompt)
def main():
    fname = input("Enter input file name (or press Enter for demo): ").strip()
    if len(fname) == 0:
        demo = "hospital_demo_input.txt"
        write_demo_input(demo)
        process_input_file(demo)
    else:
        try:
            process_input_file(fname)
        except FileNotFoundError:
            print("Error: file '" + fname + "' not found.")
        except Exception as e:
            print("Error: " + str(e))

if __name__ == "__main__":
    main()
