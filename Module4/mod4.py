# Module 4: Sorting Patient Records (Merge Sort & Quick Sort)

import time
import random

# Linked List Infrastructure
class DSALinkedList:
    class _Node:
        def __init__(self, value):
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_last(self, value):
        node = DSALinkedList._Node(value)
        if self.is_empty():
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size = self.size + 1

    def get_node_at(self, index):
        cur = self.head
        pos = 0
        while cur is not None and pos < index:
            cur = cur.next
            pos = pos + 1
        if cur is None:
            raise IndexError("Index out of range")
        return cur

    def __len__(self):
        return self.size

    def clone_values(self, copier):
        # return a new list with copier(value) for each node
        out = DSALinkedList()
        cur = self.head
        while cur is not None:
            out.insert_last(copier(cur.value))
            cur = cur.next
        return out

    def write_to_file(self, path, formatter):
        f = open(path, "w", encoding="utf-8")
        try:
            cur = self.head
            while cur is not None:
                f.write(formatter(cur.value) + "\n")
                cur = cur.next
        finally:
            f.close()


# Patient record (sort by duration minutes)
class PatientRecord:
    def __init__(self, pid, duration):
        self.PatientID = pid
        self.TreatmentMinutes = duration


# Operation counters
class OpCounter:
    def __init__(self):
        self.compares = 0
        self.moves = 0

    def reset(self):
        self.compares = 0
        self.moves = 0


# Merge Sort (Top-down, stable) on linked list
def _ms_split(head):
    # split linked list in half using slow/fast pointers
    if head is None:
        return None, None
    slow = head
    fast = head.next
    while fast is not None:
        fast = fast.next
        if fast is not None:
            slow = slow.next
            fast = fast.next
    mid = slow.next
    slow.next = None
    if mid is not None:
        mid.prev = None
    return head, mid

def _ms_merge(a, b, keyf, ops):
    # merge two sorted lists; stable
    dummy = DSALinkedList._Node(None)
    tail = dummy
    while (a is not None) and (b is not None):
        ops.compares = ops.compares + 1
        av = keyf(a.value)
        bv = keyf(b.value)
        if av <= bv:
            nxt = a.next
            a.prev = tail
            tail.next = a
            tail = a
            a = nxt
            ops.moves = ops.moves + 1
        else:
            nxt = b.next
            b.prev = tail
            tail.next = b
            tail = b
            b = nxt
            ops.moves = ops.moves + 1
    while a is not None:
        nxt = a.next
        a.prev = tail
        tail.next = a
        tail = a
        a = nxt
        ops.moves = ops.moves + 1
    while b is not None:
        nxt = b.next
        b.prev = tail
        tail.next = b
        tail = b
        b = nxt
        ops.moves = ops.moves + 1
    head = dummy.next
    if head is not None:
        head.prev = None
    return head

def _merge_sort_head(head, keyf, ops):
    if head is None:
        return None
    if head.next is None:
        return head
    left, right = _ms_split(head)
    left_sorted = _merge_sort_head(left, keyf, ops)
    right_sorted = _merge_sort_head(right, keyf, ops)
    return _ms_merge(left_sorted, right_sorted, keyf, ops)

def merge_sort_linked(lst, keyf, ops):
    # sorts in-place (by rewiring nodes) and returns the same DSALinkedList
    if lst.head is None or lst.head.next is None:
        return lst
    new_head = _merge_sort_head(lst.head, keyf, ops)
    # fix tail and size
    lst.head = new_head
    cur = lst.head
    prev = None
    n = 0
    while cur is not None:
        prev = cur
        cur = cur.next
        n = n + 1
    lst.tail = prev
    lst.size = n
    return lst


# Quick Sort (Median-of-three pivot) on linked list
def _ll_concat(a_head, a_tail, b_head, b_tail):
    if a_head is None:
        return b_head, b_tail
    if b_head is None:
        return a_head, a_tail
    a_tail.next = b_head
    b_head.prev = a_tail
    return a_head, b_tail


def _median_of_three(head, tail, keyf, ops):
    # pick head, mid, tail; return pivot value (not node)
    # find mid
    slow = head
    fast = head
    while fast is not None:
        fast = fast.next
        if fast is not None:
            slow = slow.next
            fast = fast.next
    a = keyf(head.value)
    b = keyf(slow.value)
    c = keyf(tail.value)
    # order to find median; avoid break/continue
    # we just compute comparisons logically
    ops.compares = ops.compares + 1
    if a > b:
        t1 = a; a = b; b = t1
    ops.compares = ops.compares + 1
    if b > c:
        t2 = b; b = c; c = t2
    ops.compares = ops.compares + 1
    if a > b:
        t3 = a; a = b; b = t3
    # median now in b
    return b

def _qs_partition(head, tail, keyf, ops):
    if head is None:
        return None, None, None, None, None, None
    pivot = _median_of_three(head, tail, keyf, ops)
    # three lists: less, equal, greater
    lh = None; lt = None
    eh = None; et = None
    gh = None; gt = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.prev = None
        cur.next = None
        kv = keyf(cur.value)
        ops.compares = ops.compares + 1
        if kv < pivot:
            if lh is None:
                lh = cur; lt = cur
            else:
                lt.next = cur
                cur.prev = lt
                lt = cur
            ops.moves = ops.moves + 1
        else:
            ops.compares = ops.compares + 1
            if kv == pivot:
                if eh is None:
                    eh = cur; et = cur
                else:
                    et.next = cur
                    cur.prev = et
                    et = cur
                ops.moves = ops.moves + 1
            else:
                if gh is None:
                    gh = cur; gt = cur
                else:
                    gt.next = cur
                    cur.prev = gt
                    gt = cur
                ops.moves = ops.moves + 1
        cur = nxt
    return lh, lt, eh, et, gh, gt

def _qs_sort_range(head, tail, keyf, ops):
    if head is None:
        return None, None
    if head == tail:
        return head, tail
    lh, lt, eh, et, gh, gt = _qs_partition(head, tail, keyf, ops)
    # sort less and greater
    if lh is not None:
        nlt_head, nlt_tail = _get_tail(lh)
        lh, lt = _qs_sort_range(lh, nlt_tail, keyf, ops)
    if gh is not None:
        ngr_head, ngr_tail = _get_tail(gh)
        gh, gt = _qs_sort_range(gh, ngr_tail, keyf, ops)
    # concatenate less + equal + greater
    head1, tail1 = _ll_concat(lh, lt, eh, et) if lh is not None else (eh, et)
    if head1 is None:
        head1 = eh; tail1 = et
    head2, tail2 = _ll_concat(head1, tail1, gh, gt) if gh is not None else (head1, tail1)
    return head2, tail2

def _get_tail(h):
    if h is None:
        return None, None
    cur = h
    last = None
    while cur is not None:
        last = cur
        cur = cur.next
    return h, last

def quick_sort_linked(lst, keyf, ops):
    if lst.head is None or lst.head.next is None:
        return lst
    h, t = _get_tail(lst.head)
    nh, nt = _qs_sort_range(h, t, keyf, ops)
    lst.head = nh
    lst.tail = nt
    # recompute size
    n = 0
    cur = lst.head
    while cur is not None:
        n = n + 1
        cur = cur.next
    lst.size = n
    return lst


# Dataset generation
def build_random_dataset(n, seed):
    random.seed(seed)
    lst = DSALinkedList()
    i = 1
    while i <= n:
        # durations between 1 and 300
        d = int(1 + random.random() * 300.0)
        lst.insert_last(PatientRecord(i, d))
        i = i + 1
    return lst

def build_reversed_dataset(n):
    lst = DSALinkedList()
    i = n
    while i >= 1:
        lst.insert_last(PatientRecord((n - i + 1), i))  # duration i (descending)
        i = i - 1
    return lst

def build_nearly_sorted_dataset(n, seed):
    # start perfectly sorted (duration = 1..n), then swap <=10% positions
    random.seed(seed)
    lst = DSALinkedList()
    i = 1
    while i <= n:
        lst.insert_last(PatientRecord(i, i))
        i = i + 1
    swaps = int(n * 0.05)  # swap this many pairs => at most 10% positions displaced
    s = 0
    while s < swaps:
        x = int(random.random() * n)
        y = int(random.random() * n)
        # swap node values at x and y
        nx = lst.get_node_at(x)
        ny = lst.get_node_at(y)
        tmp = nx.value.TreatmentMinutes
        nx.value.TreatmentMinutes = ny.value.TreatmentMinutes
        ny.value.TreatmentMinutes = tmp
        s = s + 1
    return lst


# Benchmarking & I/O
def key_by_duration(rec):
    return rec.TreatmentMinutes

def fmt_record(rec):
    return str(rec.PatientID) + "," + str(rec.TreatmentMinutes)

def copier(rec):
    # deep-copy minimal fields we need for sorting
    return PatientRecord(rec.PatientID, rec.TreatmentMinutes)

def time_sort(algoname, ds, sorter, keyf):
    # clone dataset (so we can reuse original for other alg)
    work = ds.clone_values(copier)
    ops = OpCounter()
    t0 = time.perf_counter()
    sorter(work, keyf, ops)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    return work, elapsed, ops

class Experiment:
    def __init__(self, n, cond, seed):
        self.n = n
        self.cond = cond  # "random" | "near" | "rev"
        self.seed = seed

def make_dataset(exp):
    if exp.cond == "random":
        return build_random_dataset(exp.n, exp.seed)
    if exp.cond == "near":
        return build_nearly_sorted_dataset(exp.n, exp.seed)
    if exp.cond == "rev":
        return build_reversed_dataset(exp.n)
    raise ValueError("Unknown condition: " + str(exp.cond))

def out_sorted_filename(algo, exp):
    return "sorted_" + algo + "_" + str(exp.n) + "_" + exp.cond + ".txt"

def run_experiment(exp, timing_log, count_log):
    # build dataset
    data = make_dataset(exp)
    # Merge Sort
    m_sorted, m_time, m_ops = time_sort("merge", data, merge_sort_linked, key_by_duration)
    m_sorted.write_to_file(out_sorted_filename("merge", exp), fmt_record)
    # Quick Sort
    q_sorted, q_time, q_ops = time_sort("quick", data, quick_sort_linked, key_by_duration)
    q_sorted.write_to_file(out_sorted_filename("quick", exp), fmt_record)

    # record timing (CSV-like rows)
    timing_log.insert_last("merge," + str(exp.n) + "," + exp.cond + "," + str(m_time))
    timing_log.insert_last("quick," + str(exp.n) + "," + exp.cond + "," + str(q_time))

    # record op counts
    count_log.insert_last("merge," + str(exp.n) + "," + exp.cond + ",compares=" + str(m_ops.compares) + ",moves=" + str(m_ops.moves))
    count_log.insert_last("quick," + str(exp.n) + "," + exp.cond + ",compares=" + str(q_ops.compares) + ",moves=" + str(q_ops.moves))

def write_list(path, ll):
    f = open(path, "w", encoding="utf-8")
    try:
        if ll.is_empty():
            f.write("(no entries)\n")
        else:
            cur = ll.head
            while cur is not None:
                f.write(str(cur.value) + "\n")
                cur = cur.next
    finally:
        f.close()


# Experiments file
def parse_experiments_file(path, used_ll):
    exps = DSALinkedList()
    f = open(path, "r", encoding="utf-8")
    try:
        for raw in f:
            line = raw.strip()
            if len(line) == 0:
                pass
            else:
                if line[0:1] == "#":
                    pass
                else:
                    # tokenize manually (no split)
                    toks = DSALinkedList()
                    cur = ""
                    i = 0
                    n = len(line)
                    while i < n:
                        ch = line[i]
                        if ch.isspace():
                            if len(cur) > 0:
                                toks.insert_last(cur)
                                cur = ""
                        else:
                            cur = cur + ch
                        i = i + 1
                    if len(cur) > 0:
                        toks.insert_last(cur)
                    if len(toks) >= 4:
                        # EXPECT "EXP size cond seed"
                        t0 = toks.get_node_at(0).value
                        t1 = toks.get_node_at(1).value
                        t2 = toks.get_node_at(2).value
                        t3 = toks.get_node_at(3).value
                        if t0 == "EXP":
                            size = int(t1)
                            cond = t2
                            sd = int(t3)
                            exps.insert_last(Experiment(size, cond, sd))
                            used_ll.insert_last("EXP " + str(size) + " " + cond + " " + str(sd))
    finally:
        f.close()
    return exps

def write_default_experiments(path, used_ll):
    seeds = [
        ("random", 12345),
        ("near",   23456),
        ("rev",    0)  # seed ignored for rev
    ]
    sizes = [100, 500, 1000]
    f = open(path, "w", encoding="utf-8")
    try:
        f.write("# Default Module 4 experiments\n")
        i = 0
        while i < 3:  # sizes count
            n = sizes[i]
            j = 0
            while j < 3:
                cond = seeds[j][0]
                sd = seeds[j][1] + n  # make seed depend on size for variety (rev ignores it)
                f.write("EXP " + str(n) + " " + cond + " " + str(sd) + "\n")
                used_ll.insert_last("EXP " + str(n) + " " + cond + " " + str(sd))
                j = j + 1
            i = i + 1
    finally:
        f.close()


# Main menu
def main():
    print("=== Module 4: Sorting Patient Records (Merge vs Quick) ===")
    expfile = input("Enter experiments file (or press Enter for default): ").strip()

    used = DSALinkedList()
    if len(expfile) == 0:
        expfile = "m4_experiments.txt"
        write_default_experiments(expfile, used)
        print("Wrote default experiments to " + expfile)
    else:
        # still record what we actually read
        pass

    # parse experiments
    if used.is_empty():
        used = DSALinkedList()
        exps = parse_experiments_file(expfile, used)
    else:
        exps = parse_experiments_file(expfile, DSALinkedList())  # already filled 'used' above

    # run
    timing = DSALinkedList()
    counts = DSALinkedList()

    # header rows
    timing.insert_last("ALGO,SIZE,COND,SECONDS")
    counts.insert_last("ALGO,SIZE,COND,COUNTS")

    cur = exps.head
    while cur is not None:
        exp = cur.value
        run_experiment(exp, timing, counts)
        cur = cur.next

    # outputs
    write_list("m4_timing_summary.txt", timing)
    write_list("m4_opcounts.txt", counts)
    write_list("m4_experiments_used.txt", used)

    print("Done. Wrote:")
    print("  - m4_timing_summary.txt")
    print("  - m4_opcounts.txt")
    print("  - m4_experiments_used.txt")
    print("  - plus one sorted_*.txt per algorithm × size × condition")

if __name__ == "__main__":
    main()
