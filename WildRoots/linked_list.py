"""
linked_list.py - Singly Linked List used as the ONLY storage for species.

Node  ->  Node  ->  Node  -> ... -> None
Each node holds one species (a dictionary) and a pointer to the next node.
"""


class Node:
    def __init__(self, species_data):
        self.species_data = species_data   # one species (dictionary)
        self.next = None                   # pointer to the next node


class LinkedList:
    def __init__(self):
        self.head = None                   # first node (None = empty list)

    # ---------- append: add a species at the END of the list ----------
    def append(self, species_data):
        new_node = Node(species_data)
        if self.head is None:              # empty list: new node is the head
            self.head = new_node
            return
        current = self.head
        while current.next is not None:    # walk to the last node
            current = current.next
        current.next = new_node

    # ---------- display: visit every node and collect the species ----------
    def display(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.species_data)
            current = current.next
        return result

    # ---------- count: number of nodes ----------
    def count(self):
        total = 0
        current = self.head
        while current is not None:
            total += 1
            current = current.next
        return total

    # ---------- search: find species whose name contains the text ----------
    def search(self, name):
        name = name.strip().lower()
        found, current = [], self.head
        while current is not None:
            s = current.species_data
            if name in s["name"].lower() or name in s["scientific_name"].lower():
                found.append(s)
            current = current.next
        return found

    # ---------- delete: remove the first species with this exact name ----------
    def delete(self, name):
        current, previous = self.head, None
        while current is not None:
            if current.species_data["name"].lower() == name.strip().lower():
                if previous is None:       # deleting the head
                    self.head = current.next
                else:                      # skip over the node
                    previous.next = current.next
                return True
            previous, current = current, current.next
        return False

    # ---------- filter: by type / habitat / text, node by node ----------
    def filter(self, species_type="", habitat="", query=""):
        found, current = [], self.head
        while current is not None:
            s = current.species_data
            ok = (species_type in ("", "Both", s["type"])
                  and habitat in ("", s["habitat"])
                  and query.strip().lower() in s["name"].lower())
            if ok:
                found.append(s)
            current = current.next
        return found

    # ---------- classify: score every node against the environment ----------
    def classify(self, env):
        """
        env = {type, habitat, temperature, pollution, water, climate}
        Score = (matching features / 5) * 100.  Returns (matches, nodes_visited).
        """
        features = ["habitat", "temperature", "pollution", "water", "climate"]
        matches, nodes_visited = [], 0
        current = self.head
        while current is not None:
            nodes_visited += 1             # count every node we touch
            s = current.species_data
            if env["type"] in ("Both", s["type"]):
                matched = [f for f in features if env[f] == s[f]]
                score = round(len(matched) / len(features) * 100)
                if score >= 40:            # minimum compatibility
                    item = dict(s)
                    item["compatibility"] = score
                    item["matched_features"] = matched
                    matches.append(item)
            current = current.next
        matches.sort(key=lambda m: m["compatibility"], reverse=True)
        return matches, nodes_visited
