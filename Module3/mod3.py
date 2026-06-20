# Module 3: Heap-Based Emergency Scheduling (Max Heap) with Hash integration


# Linked List (array-like access)
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

    def get_at(self, index):
        cur = self.head
        pos = 0
        while cur is not None:
            if pos == index:
                return cur.value
            cur = cur.next
            pos = pos + 1
        raise IndexError("Index out of range")

    def set_at(self, index, value):
        cur = self.head
        pos = 0
        while cur is not None:
            if pos == index:
                cur.value = value
                return
            cur = cur.next
            pos = pos + 1
        raise IndexError("Index out of range")

    def __len__(self):
        return self.size


# Patients & Hash Table (chaining)
class Patient:
    def __init__(self, pid, name, age, dept, urg, status):
        self.PatientID = pid
        self.Name = name
        self.Age = age
        self.Department = dept
        self.UrgencyLevel = urg
        self.TreatmentStatus = status

    def __eq__(self, other):
        if other is None:
            return False
        return self.PatientID == other.PatientID

    def printable(self):
        return ("PatientID=" + str(self.PatientID) +
                ", Name=" + self.Name.replace("_", " ") +
                ", Age=" + str(self.Age) +
                ", Department=" + self.Department.replace("_", " ") +
                ", UrgencyLevel=" + str(self.UrgencyLevel) +
                ", TreatmentStatus=" + self.TreatmentStatus.replace("_", " "))

class _HashEntry:
    def __init__(self, key, patient):
        self.key = key
        self.patient = patient

class PatientHashTable:
    def __init__(self, size_hint=29):
        self.size = self._nextPrime(size_hint)
        self.count = 0
        self.buckets = DSALinkedList()
        i = 0
        while i < self.size:
            self.buckets.insert_last(DSALinkedList())
            i = i + 1

    def put(self, patient):
        idx = self._hash(patient.PatientID)
        chain = self._bucket(idx)
        cur = chain.head
        updated = False
        while cur is not None and (not updated):
            e = cur.value
            if e.key == patient.PatientID:
                e.patient = patient
                updated = True
            else:
                cur = cur.next
        if not updated:
            chain.insert_last(_HashEntry(patient.PatientID, patient))
            self.count = self.count + 1

    def get(self, pid):
        idx = self._hash(pid)
        chain = self._bucket(idx)
        cur = chain.head
        found = None
        while cur is not None and (found is None):
            e = cur.value
            if e.key == pid:
                found = e.patient
            else:
                cur = cur.next
        return found

    def _bucket(self, idx):
        cur = self.buckets.head
        pos = 0
        while cur is not None and (pos < idx):
            cur = cur.next
            pos = pos + 1
        if cur is None:
            raise IndexError("Bucket index OOR")
        return cur.value

    def _hash(self, key):
        try:
            k = int(key)
            if k < 0:
                k = -k
            return k % self.size
        except:
            total = 0
            s = str(key)
            i = 0
            n = len(s)
            while i < n:
                total = total + ord(s[i])
                i = i + 1
            return (total if total >= 0 else -total) % self.size

    def _nextPrime(self, n):
        def isPrime(x):
            if x < 2:
                return False
            if (x % 2 == 0) and (x != 2):
                return False
            i = 3
            ok = True
            while (i * i) <= x and ok:
                if x % i == 0:
                    ok = False
                else:
                    i = i + 2
            return ok
        m = n
        while not isPrime(m):
            m = m + 1
        return m


# Max Heap (priority queue)
class DSAHeapEntry:
    def __init__(self, priority, value):  # value will be a Request
        self.priority = priority
        self.value = value

    def getPriority(self):
        return self.priority

    def getValue(self):
        return self.value

class Request:
    def __init__(self, pid, U, T, pr):
        self.PatientID = pid
        self.U = U
        self.T = T
        self.priority = pr

    def printable(self):
        return ("(pid=" + str(self.PatientID) +
                ", U=" + str(self.U) +
                ", T=" + str(self.T) +
                ", pr=" + str(self.priority) + ")")

class MaxHeap:
    def __init__(self):
        self.arr = DSALinkedList()
        self.count = 0

    def insert(self, priority, value):
        self.arr.insert_last(DSAHeapEntry(priority, value))
        self.count = self.count + 1
        self._percolate_up(self.count - 1)

    def peek(self):
        if self.count == 0:
            raise Exception("Heap empty")
        return self.arr.get_at(0)

    def extract(self):
        if self.count == 0:
            raise Exception("Heap empty")
        root = self.arr.get_at(0)
        last = self.arr.get_at(self.count - 1)
        self.arr.set_at(0, last)
        self.count = self.count - 1
        if self.count > 0:
            self._percolate_down(0)
        return root

    def _percolate_up(self, idx):
        parent = (idx - 1) // 2
        # no break/continue: loop ends by resetting idx to 0 when done
        while idx > 0:
            cur = self.arr.get_at(idx)
            par = self.arr.get_at(parent)
            if cur.getPriority() > par.getPriority():
                self.arr.set_at(idx, par)
                self.arr.set_at(parent, cur)
                idx = parent
                parent = (parent - 1) // 2
            else:
                idx = 0  # natural exit

    def _percolate_down(self, idx):
        # while idx has at least one child
        while idx < (self.count // 2):
            l = (idx * 2) + 1
            r = l + 1
            big = l
            if r < self.count:
                left = self.arr.get_at(l)
                right = self.arr.get_at(r)
                if right.getPriority() > left.getPriority():
                    big = r
            cur = self.arr.get_at(idx)
            child = self.arr.get_at(big)
            if cur.getPriority() < child.getPriority():
                self.arr.set_at(idx, child)
                self.arr.set_at(big, cur)
                idx = big
            else:
                idx = self.count  # exit naturally

    def state_string(self):
        # array view: [(prio,pid), ...]
        s = "["
        i = 0
        first = True
        while i < self.count:
            e = self.arr.get_at(i)
            pr = e.getPriority()
            val = e.getValue()
            txt = "(" + str(pr) + "," + str(val.PatientID) + ")"
            if first:
                s = s + txt
                first = False
            else:
                s = s + ", " + txt
            i = i + 1
        s = s + "]"
        return s


# Tokenizer (no split())
def tokenize(line):
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
    return toks

def tok_at(tokens, idx):
    node = tokens.head
    pos = 0
    while node is not None and (pos < idx):
        node = node.next
        pos = pos + 1
    if node is None:
        return None
    return node.value

def toks_len(tokens):
    return len(tokens)



# Logging helpers
def write_list_to_file(path, ll):
    f = open(path, "w", encoding="utf-8")
    try:
        if ll is None or ll.is_empty():
            f.write("(no entries)\n")
        else:
            cur = ll.head
            while cur is not None:
                f.write(str(cur.value) + "\n")
                cur = cur.next
    finally:
        f.close()


# Priority metric
def compute_priority(U, T):

    base = 6 - int(U)
    # integer division not allowed; ensure float
    numer = 1000.0
    denom = float(T)
    return float(base) + (numer / denom)

def is_inactive(status_text):
    if status_text is None:
        return True
    st = status_text.lower()
    # treat clearly inactive states as inactive
    has = False
    if "discharged" in st:
        has = True
    else:
        if "completed" in st:
            has = True
        else:
            if "inactive" in st:
                has = True
    return has


# Driver
def load_patients_from_file(ht, patient_file, priolog):
    f = open(patient_file, "r", encoding="utf-8")
    try:
        for raw in f:
            line = raw.strip()
            if len(line) == 0:
                pass
            else:
                if line[0:1] == "#":
                    pass
                else:
                    toks = tokenize(line)
                    if toks_len(toks) > 0:
                        cmd = tok_at(toks, 0)
                        is_patient = (cmd == "PATIENT") or (cmd == "INSERT")
                        if is_patient:
                            pid_s = tok_at(toks, 1)
                            name = tok_at(toks, 2)
                            age_s = tok_at(toks, 3)
                            dept = tok_at(toks, 4)
                            urg_s = tok_at(toks, 5)
                            status = tok_at(toks, 6)

                            ok = True
                            pid = 0
                            age = 0
                            urg = 0

                            try:
                                pid = int(pid_s)
                            except:
                                ok = False
                                priolog.insert_last("PATIENT LOAD ERROR -> invalid PatientID: " + str(pid_s))

                            if ok:
                                try:
                                    age = int(age_s)
                                except:
                                    ok = False
                                    priolog.insert_last("PATIENT LOAD ERROR -> invalid Age for PID=" + str(pid))

                            if ok:
                                try:
                                    urg = int(urg_s)
                                    if urg < 1 or urg > 5:
                                        ok = False
                                        priolog.insert_last("PATIENT LOAD ERROR -> urgency must be 1..5 for PID=" + str(pid))
                                except:
                                    ok = False
                                    priolog.insert_last("PATIENT LOAD ERROR -> invalid Urgency for PID=" + str(pid))

                            if ok:
                                if name is None or len(name.strip()) == 0:
                                    ok = False
                                    priolog.insert_last("PATIENT LOAD ERROR -> empty name for PID=" + str(pid))
                            if ok:
                                if dept is None or len(dept.strip()) == 0:
                                    ok = False
                                    priolog.insert_last("PATIENT LOAD ERROR -> empty department for PID=" + str(pid))
                            if ok:
                                if status is None or len(status.strip()) == 0:
                                    ok = False
                                    priolog.insert_last("PATIENT LOAD ERROR -> empty status for PID=" + str(pid))

                            if ok:
                                p = Patient(pid, name, age, dept, urg, status)
                                ht.put(p)
                        else:
                            priolog.insert_last("PATIENT FILE: ignored line -> " + line)
    finally:
        f.close()

def process_requests(ht, requests_file, heap_trace, priolog, summary):
    heap = MaxHeap()
    # track served order
    served = DSALinkedList()

    f = open(requests_file, "r", encoding="utf-8")
    try:
        for raw in f:
            line = raw.strip()
            if len(line) == 0:
                pass
            else:
                if line[0:1] == "#":
                    pass
                else:
                    toks = tokenize(line)
                    if toks_len(toks) > 0:
                        cmd = tok_at(toks, 0)

                        if cmd == "REQUEST":
                            pid_s = tok_at(toks, 1)
                            t_s = tok_at(toks, 2)
                            can = True
                            pid = 0
                            T = 0
                            try:
                                pid = int(pid_s)
                            except:
                                can = False
                                priolog.insert_last("REQUEST ERROR -> invalid PatientID: " + str(pid_s))
                            if can:
                                try:
                                    T = int(t_s)
                                except:
                                    can = False
                                    priolog.insert_last("REQUEST ERROR -> invalid T for PID=" + str(pid))

                            if can:
                                if T <= 0:
                                    priolog.insert_last("REQUEST SKIPPED -> non-positive T for PID=" + str(pid))
                                else:
                                    pat = ht.get(pid)
                                    if pat is None:
                                        priolog.insert_last("REQUEST SKIPPED -> PatientID not found: " + str(pid))
                                    else:
                                        if is_inactive(pat.TreatmentStatus):
                                            priolog.insert_last("REQUEST SKIPPED -> inactive status for PID=" + str(pid) + " (" + pat.TreatmentStatus.replace("_"," ") + ")")
                                        else:
                                            U = pat.UrgencyLevel
                                            pr = compute_priority(U, T)
                                            r = Request(pid, U, T, pr)
                                            priolog.insert_last("PRIORITY pid=" + str(pid) + " U=" + str(U) + " T=" + str(T) + " -> " + str(pr))
                                            heap.insert(pr, r)
                                            heap_trace.insert_last("INSERT: " + r.printable())
                                            heap_trace.insert_last("HEAP: " + heap.state_string())

                        elif cmd == "EXTRACT":
                            if heap.count == 0:
                                heap_trace.insert_last("EXTRACT: heap empty")
                            else:
                                top = heap.extract()
                                req = top.getValue()
                                heap_trace.insert_last("EXTRACT -> " + req.printable())
                                heap_trace.insert_last("HEAP: " + heap.state_string())
                                served.insert_last("SERVED -> pid=" + str(req.PatientID) + " pr=" + str(req.priority))

                        elif cmd == "PEEK":
                            if heap.count == 0:
                                heap_trace.insert_last("PEEK: heap empty")
                            else:
                                p = heap.peek()
                                req = p.getValue()
                                heap_trace.insert_last("PEEK -> " + req.printable())
                                heap_trace.insert_last("HEAP: " + heap.state_string())

                        elif cmd == "UPDATE":
                            pid_s = tok_at(toks, 1)
                            u_s = tok_at(toks, 2)
                            status = tok_at(toks, 3)
                            can = True
                            pid = 0
                            newU = 0
                            try:
                                pid = int(pid_s)
                            except:
                                can = False
                                priolog.insert_last("UPDATE ERROR -> invalid PatientID: " + str(pid_s))
                            if can:
                                try:
                                    newU = int(u_s)
                                    if newU < 1 or newU > 5:
                                        can = False
                                        priolog.insert_last("UPDATE ERROR -> urgency must be 1..5 for PID=" + str(pid))
                                except:
                                    can = False
                                    priolog.insert_last("UPDATE ERROR -> invalid urgency for PID=" + str(pid))
                            if can:
                                pat = ht.get(pid)
                                if pat is None:
                                    priolog.insert_last("UPDATE SKIPPED -> unknown PID=" + str(pid))
                                else:
                                    pat.UrgencyLevel = newU
                                    pat.TreatmentStatus = status
                                    ht.put(pat)
                                    priolog.insert_last("UPDATED PATIENT -> " + pat.printable())

                        else:
                            priolog.insert_last("REQUEST FILE: ignored line -> " + line)
    finally:
        f.close()

    # summary
    if served.is_empty():
        summary.insert_last("No patients served.")
    else:
        cur = served.head
        order = 1
        while cur is not None:
            summary.insert_last(str(order) + ". " + str(cur.value))
            cur = cur.next
            order = order + 1

def write_demo_patients(path):
    f = open(path, "w", encoding="utf-8")
    try:
        # Mixed statuses; one discharged to test inactive skip; urgency 1..5 spread
        f.write("# Demo patients for Module 3\n")
        f.write("PATIENT 5001 Alice_W 41 Emergency 1 Waiting\n")
        f.write("PATIENT 5002 Bob_K 55 ICU 2 Waiting\n")
        f.write("PATIENT 5003 Chen_L 63 Wards 3 In_Treatment\n")
        f.write("PATIENT 5004 Devi_R 36 Pharmacy 4 Waiting\n")
        f.write("PATIENT 5005 Elias_T 29 Radiology 5 Waiting\n")
        f.write("PATIENT 5006 Farah_M 47 Labs 2 Waiting\n")
        f.write("PATIENT 5007 Gita_P 33 Theatres 1 Waiting\n")
        f.write("PATIENT 5008 Hadi_Q 71 Outpatient 3 Discharged\n")   # inactive
        f.write("PATIENT 5009 Inez_S 58 ICU 4 Waiting\n")
        f.write("PATIENT 5010 Jamal_U 22 Emergency 2 Waiting\n")
        f.write("PATIENT 5011 Kira_V 44 Wards 5 Waiting\n")
    finally:
        f.close()

def write_demo_requests(path):
    f = open(path, "w", encoding="utf-8")
    try:
        f.write("# Demo requests: >=10 inserts, >=5 extracts, with updates\n")
        f.write("REQUEST 5001 40\n")  # U=1, T=40
        f.write("REQUEST 5002 60\n")  # U=2
        f.write("REQUEST 5003 30\n")  # U=3
        f.write("REQUEST 5004 20\n")  # U=4
        f.write("REQUEST 5005 10\n")  # U=5
        f.write("REQUEST 5006 45\n")  # U=2
        f.write("REQUEST 5007 25\n")  # U=1
        f.write("REQUEST 5008 30\n")  # inactive -> skipped
        f.write("REQUEST 9999 30\n")  # unknown -> skipped
        f.write("REQUEST 5010 15\n")  # U=2
        f.write("REQUEST 5011 120\n") # U=5
        # peek once
        f.write("PEEK\n")
        # 5 extractions
        f.write("EXTRACT\n")
        f.write("EXTRACT\n")
        f.write("EXTRACT\n")
        f.write("EXTRACT\n")
        f.write("EXTRACT\n")
        # Update one patient (raise urgency), then request again
        f.write("UPDATE 5004 1 In_Treatment\n")  # 5004 urgency from 4 -> 1
        f.write("REQUEST 5004 30\n")
        f.write("EXTRACT\n")
    finally:
        f.close()

def main():
    print("=== Module 3: Heap-Based Emergency Scheduling ===")
    pfile = input("Enter Patients file (or press Enter for demo): ").strip()
    if len(pfile) == 0:
        pfile = "m3_demo_patients.txt"
        write_demo_patients(pfile)
        print("Demo patients written to " + pfile)

    rfile = input("Enter Requests file (or press Enter for demo): ").strip()
    if len(rfile) == 0:
        rfile = "m3_demo_requests.txt"
        write_demo_requests(rfile)
        print("Demo requests written to " + rfile)

    priolog = DSALinkedList()
    heap_trace = DSALinkedList()
    summary = DSALinkedList()

    # load patients
    ht = PatientHashTable(29)
    load_patients_from_file(ht, pfile, priolog)

    # process requests with heap
    process_requests(ht, rfile, heap_trace, priolog, summary)

    # outputs
    write_list_to_file("m3_heap_trace.txt", heap_trace)
    write_list_to_file("m3_priority_log.txt", priolog)
    write_list_to_file("m3_summary.txt", summary)

    print("Done. Wrote m3_heap_trace.txt, m3_priority_log.txt, m3_summary.txt")

if __name__ == "__main__":
    main()
