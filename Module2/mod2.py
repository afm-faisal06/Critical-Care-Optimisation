# Module 2: Hash-Based Patient Lookup (Chaining + Linked Lists, NO arrays/lists/dicts, NO break/continue)


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


# Patient Record 
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

    def to_line(self):
        # single-line printable record
        return ("PatientID=" + str(self.PatientID) +
                ", Name=" + self.Name.replace("_", " ") +
                ", Age=" + str(self.Age) +
                ", Department=" + self.Department.replace("_", " ") +
                ", UrgencyLevel=" + str(self.UrgencyLevel) +
                ", TreatmentStatus=" + self.TreatmentStatus.replace("_", " "))


# Hash Entry (chaining node)
class _HashEntry:
    def __init__(self, key, patient):
        self.key = key
        self.patient = patient  # one-to-one by PatientID unique


# Hash Table (Chaining)
class PatientHashTable:
    def __init__(self, tableSize=29):
        # choose prime >= 29 to handle 20+ with LF<0.7
        self.size = self._nextPrime(tableSize)
        self.count = 0
        self.buckets = DSALinkedList()  # list of chains
        self.upper_threshold = 0.7
        self.resizes = 0
        # create empty chains
        i = 0
        while i < self.size:
            self.buckets.insert_last(DSALinkedList())
            i = i + 1
        # simple step counter for complexity snapshots
        self.steps = 0


    def insert(self, patient, log_ll, collision_ll):
        # validation
        self._validate_patient(patient, log_ll)

        # Resize if needed
        if self.getLoadFactor() > self.upper_threshold:
            self._resize(self.size * 2, log_ll)

        idx = self._hash(patient.PatientID)
        chain = self._bucket_at(idx)

        # see if duplicate ID exists -> update instead of reject
        cur = chain.head
        updated = False
        while (cur is not None) and (not updated):
            self.steps = self.steps + 1
            entry = cur.value
            if entry.key == patient.PatientID:
                # update in place
                entry.patient = patient
                updated = True
            else:
                cur = cur.next

        if updated:
            log_ll.insert_last("UPDATE @index " + str(idx) + " -> " + patient.to_line())
        else:
            # detect collision: chain non-empty means collision on this insert
            was_collision = (not chain.is_empty())
            chain.insert_last(_HashEntry(patient.PatientID, patient))
            self.count = self.count + 1
            if was_collision:
                # Log the full chain state to show resolution by chaining
                log_ll.insert_last("INSERT (collision) @index " + str(idx) + " -> " + patient.to_line())
                self._log_chain(idx, chain, collision_ll)
            else:
                log_ll.insert_last("INSERT @index " + str(idx) + " -> " + patient.to_line())

    def search(self, patientID, log_ll):
        idx = self._hash(patientID)
        chain = self._bucket_at(idx)
        cur = chain.head
        found = None
        while (cur is not None) and (found is None):
            self.steps = self.steps + 1
            entry = cur.value
            if entry.key == patientID:
                found = entry.patient
            else:
                cur = cur.next
        if found is None:
            log_ll.insert_last("SEARCH @index " + str(idx) + " -> NOT FOUND (PatientID=" + str(patientID) + ")")
        else:
            log_ll.insert_last("SEARCH @index " + str(idx) + " -> FOUND: " + found.to_line())
        return found

    def delete(self, patientID, log_ll):
        idx = self._hash(patientID)
        chain = self._bucket_at(idx)
        cur = chain.head
        removed = False
        while (cur is not None) and (not removed):
            self.steps = self.steps + 1
            entry = cur.value
            if entry.key == patientID:
                # remove this node from chain
                removed = True
                # We can't use break; do in-place remove using list.remove_node on the actual object value
                chain.remove_node(entry)
            else:
                cur = cur.next
        if removed:
            self.count = self.count + (-1)
            log_ll.insert_last("DELETE @index " + str(idx) + " -> OK (PatientID=" + str(patientID) + ")")
        else:
            log_ll.insert_last("DELETE @index " + str(idx) + " -> NOT FOUND (PatientID=" + str(patientID) + ")")
        return removed

    def getLoadFactor(self):
        if self.size == 0:
            return 0.0
        return float(self.count) / float(self.size)

    # Internal helpers

    def _validate_patient(self, p, log_ll):
        ok = True
        msg = ""
        # PatientID must be int
        try:
            _ = int(p.PatientID)
        except:
            ok = False
            msg = "Invalid PatientID (must be integer)."
        if ok:
            if p.Name is None or len(p.Name.strip()) == 0:
                ok = False
                msg = "Invalid Name."
        if ok:
            try:
                a = int(p.Age)
                if a < 0 or a > 130:
                    ok = False
                    msg = "Invalid Age."
            except:
                ok = False
                msg = "Invalid Age."
        if ok:
            if p.Department is None or len(p.Department.strip()) == 0:
                ok = False
                msg = "Invalid Department."
        if ok:
            try:
                u = int(p.UrgencyLevel)
                if (u < 1) or (u > 5):
                    ok = False
                    msg = "Urgency must be 1..5."
            except:
                ok = False
                msg = "Urgency must be 1..5."
        if ok:
            if p.TreatmentStatus is None or len(p.TreatmentStatus.strip()) == 0:
                ok = False
                msg = "Invalid TreatmentStatus."
        if not ok:
            log_ll.insert_last("VALIDATION ERROR -> " + msg)
            raise ValueError(msg)

    def _hash(self, key):
        self.steps = self.steps + 1
        try:
            k = int(key)
            if k < 0:
                k = -k
            return k % self.size
        except:
            # fallback: sum of ords
            total = 0
            # manual loop to avoid sum() over list
            s = str(key)
            i = 0
            n = len(s)
            while i < n:
                total = total + ord(s[i])
                i = i + 1
            if total < 0:
                total = -total
            return total % self.size

    def _bucket_at(self, idx):
        # traverse buckets linked list to specific index
        node = self.buckets.head
        pos = 0
        while (node is not None) and (pos < idx):
            node = node.next
            pos = pos + 1
        if node is None:
            raise IndexError("Bucket index out of range")
        return node.value

    def _resize(self, newSize, log_ll):
        newSize = self._nextPrime(newSize)
        log_ll.insert_last("RESIZE: " + str(self.size) + " -> " + str(newSize))
        # build new bucket set
        newBuckets = DSALinkedList()
        i = 0
        while i < newSize:
            newBuckets.insert_last(DSALinkedList())
            i = i + 1
        # rehash all entries
        oldBuckets = self.buckets
        oldHead = oldBuckets.head
        self.buckets = newBuckets
        oldSize = self.size
        self.size = newSize
        self.count = 0
        self.resizes = self.resizes + 1

        # iterate old buckets -> chains -> entries
        bnode = oldHead
        while bnode is not None:
            chain = bnode.value
            cnode = chain.head
            while cnode is not None:
                entry = cnode.value
                # re-insert (no logging of collision here to keep output concise)
                idx = self._hash(entry.key)
                dest = self._bucket_at(idx)
                dest.insert_last(_HashEntry(entry.key, entry.patient))
                self.count = self.count + 1
                cnode = cnode.next
            bnode = bnode.next

    def _nextPrime(self, n):
        # simple prime search without lists
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
        p = isPrime(m)
        while not p:
            m = m + 1
            p = isPrime(m)
        return m

    def _log_chain(self, idx, chain, collision_ll):
        # record chain members at index idx
        line = "INDEX " + str(idx) + " CHAIN: "
        cur = chain.head
        first = True
        while cur is not None:
            e = cur.value
            pl = "{" + str(e.key) + ":" + e.patient.Name.replace("_", " ") + "}"
            if first:
                line = line + pl
                first = False
            else:
                line = line + " -> " + pl
            cur = cur.next
        collision_ll.insert_last(line)


# Tokenizer (no split())
def tokenize(line):
    tokens = DSALinkedList()
    current = ""
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch.isspace():
            if len(current) > 0:
                tokens.insert_last(current)
                current = ""
        else:
            current = current + ch
        i = i + 1
    if len(current) > 0:
        tokens.insert_last(current)
    return tokens

def token_at(tokens, idx):
    cur = tokens.head
    pos = 0
    while (cur is not None) and (pos < idx):
        cur = cur.next
        pos = pos + 1
    if cur is None:
        return None
    return cur.value

def tokens_len(tokens):
    return len(tokens)


# Driver: process input file & write outputs
def process_input_file(infile):
    ht = PatientHashTable(29)
    log_ll = DSALinkedList()
    collision_ll = DSALinkedList()

    f = open(infile, "r", encoding="utf-8")
    try:
        for raw in f:
            line = raw.strip()
            if len(line) == 0:
                pass
            else:
                is_comment = False
                if len(line) >= 1:
                    if line[0:1] == "#":
                        is_comment = True
                if not is_comment:
                    toks = tokenize(line)
                    if tokens_len(toks) > 0:
                        cmd = token_at(toks, 0)

                        if cmd == "INSERT":
                            # Read raw fields
                            pid_s = token_at(toks, 1)
                            name = token_at(toks, 2)
                            age_s = token_at(toks, 3)
                            dept = token_at(toks, 4)
                            urg_s = token_at(toks, 5)
                            status = token_at(toks, 6)

                            # Safe numeric conversions (no crash)
                            ok = True
                            # PatientID
                            pid = 0
                            try:
                                pid = int(pid_s)
                            except:
                                ok = False
                                log_ll.insert_last("VALIDATION ERROR -> Invalid PatientID (must be integer).")
                                log_ll.insert_last("INSERT ERROR: Invalid PatientID (must be integer).")
                            # Age
                            if ok:
                                try:
                                    _ = int(age_s)  # just to check; actual validation in insert() too
                                except:
                                    ok = False
                                    log_ll.insert_last("VALIDATION ERROR -> Invalid Age.")
                                    log_ll.insert_last("INSERT ERROR: Invalid Age.")
                            # Urgency
                            if ok:
                                try:
                                    _ = int(urg_s)
                                except:
                                    ok = False
                                    log_ll.insert_last("VALIDATION ERROR -> Urgency must be 1..5.")
                                    log_ll.insert_last("INSERT ERROR: Urgency must be 1..5.")

                            if ok:
                                # Build patient; deeper field validation happens inside ht.insert()
                                age = int(age_s)
                                urg = int(urg_s)
                                p = Patient(pid, name, age, dept, urg, status)
                                try:
                                    ht.insert(p, log_ll, collision_ll)
                                except Exception as e:
                                    log_ll.insert_last("INSERT ERROR: " + str(e))

                        elif cmd == "SEARCH":
                            pid_raw = token_at(toks, 1)
                            can = True
                            pid = 0
                            try:
                                pid = int(pid_raw)
                            except:
                                can = False
                                log_ll.insert_last("SEARCH @index ? -> NOT FOUND (PatientID=" + str(pid_raw) + ")")
                            if can:
                                ht.search(pid, log_ll)

                        elif cmd == "DELETE":
                            pid_raw = token_at(toks, 1)
                            can = True
                            pid = 0
                            try:
                                pid = int(pid_raw)
                            except:
                                can = False
                                log_ll.insert_last("DELETE @index ? -> NOT FOUND (PatientID=" + str(pid_raw) + ")")
                            if can:
                                ht.delete(pid, log_ll)

                        else:
                            # Unknown line -> log and continue
                            log_ll.insert_last("IGNORED LINE: " + line)
    finally:
        f.close()

    # Write outputs even if there were validation errors
    write_list_to_file("m2_log.txt", log_ll)
    write_list_to_file("m2_collisions.txt", collision_ll)

    s = DSALinkedList()
    s.insert_last("SUMMARY")
    s.insert_last("Records: " + str(ht.count))
    s.insert_last("Table size (buckets): " + str(ht.size))
    s.insert_last("Load factor: " + str(ht.getLoadFactor()))
    s.insert_last("Resizes: " + str(ht.resizes))
    s.insert_last("Step counter (approx ops): " + str(ht.steps))
    write_list_to_file("m2_summary.txt", s)

    print("Done. Wrote m2_log.txt, m2_collisions.txt, m2_summary.txt")


def write_list_to_file(path, linked_list):
    out = open(path, "w", encoding="utf-8")
    try:
        if linked_list is None or linked_list.is_empty():
            out.write("(no entries)\n")
        else:
            cur = linked_list.head
            while cur is not None:
                out.write(str(cur.value) + "\n")
                cur = cur.next
    finally:
        out.close()


# Demo Input (20+ records, collisions, hits/misses, deletions)
def write_demo_input(path):
    out = open(path, "w", encoding="utf-8")
    try:
        out.write("# Demo for Module 2: chaining + collisions + hits/misses + deletions\n")
        # 22 patients distributed to guarantee collisions by hashing PatientID % tableSize (29)
        out.write("INSERT 1001 John_Doe 47 Emergency 5 Waiting\n")
        out.write("INSERT 1002 Jane_Smith 34 ICU 4 Waiting\n")
        out.write("INSERT 1003 Mark_Tan 63 Wards 3 In_Treatment\n")
        out.write("INSERT 1004 Priya_K 29 Pharmacy 2 Waiting\n")
        out.write("INSERT 1030 Luca_B 51 Radiology 1 Discharged\n")   # potential collision with 1001
        out.write("INSERT 1060 Aisha_R 40 Labs 5 Waiting\n")         # potential collision chain
        out.write("INSERT 1015 Omar_Q 38 Theatres 3 Waiting\n")
        out.write("INSERT 1022 Chen_L 45 Outpatient 2 Waiting\n")
        out.write("INSERT 1089 Eva_M 56 Emergency 4 In_Treatment\n")
        out.write("INSERT 1120 Noah_P 21 ICU 1 Waiting\n")
        out.write("INSERT 1149 Zara_N 30 Wards 5 Waiting\n")
        out.write("INSERT 1178 Amir_S 72 Pharmacy 4 Waiting\n")
        out.write("INSERT 1207 Hana_J 66 Radiology 2 In_Treatment\n")
        out.write("INSERT 1236 Leo_K 53 Labs 3 Waiting\n")
        out.write("INSERT 1265 Isha_T 19 Theatres 2 Waiting\n")
        out.write("INSERT 1294 Yuki_A 61 Outpatient 5 Waiting\n")
        out.write("INSERT 1323 Musa_D 60 Emergency 4 Waiting\n")
        out.write("INSERT 1352 Sara_U 44 ICU 3 Waiting\n")
        out.write("INSERT 1381 Vik_G 57 Wards 1 Discharged\n")
        out.write("INSERT 1410 Riya_H 26 Pharmacy 2 Waiting\n")
        out.write("INSERT 1439 Tom_R 36 Radiology 5 Waiting\n")
        out.write("INSERT 1468 Ana_V 41 Labs 4 Waiting\n")
        # searches (hit/miss)
        out.write("SEARCH 1001\n")
        out.write("SEARCH 2000\n")
        out.write("SEARCH 1060\n")
        # deletions + post-delete searches
        out.write("DELETE 1030\n")
        out.write("SEARCH 1030\n")
        out.write("DELETE 7777\n")
        # duplicate insert -> update
        out.write("INSERT 1001 John_Doe 48 Emergency 5 In_Treatment\n")
    finally:
        out.close()


# Main (interactive prompt) 
def main():
    fname = input("Enter Module 2 input file name (or press Enter for demo): ").strip()
    if len(fname) == 0:
        demo = "m2_demo_input.txt"
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
