class FuzzyElement:
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree
        
    def merge(self, name, degree):
        assert self.name == name
        new_degree = self.degree + degree - self.degree * degree
        self.degree = new_degree
    
    def traditional_merge(self, name, degree):
        assert self.name == name
        if degree < self.degree:
            return
        else:
            self.degree = degree
    
    def __str__(self):
        return '{} [{:1.2f}]'.format(self.name, self.degree)
        
class Suade:    
    def filterPredecessor(self, node, relation):
        DG = self.DG
        predecessors = set()
        for edge in DG.in_edges(node):
            SRC = edge[0]
            TGT = edge[1]
            assert TGT == node
            edge_label = DG[SRC][TGT]['label']
            if edge_label == relation:
                predecessors.add(SRC)

        return predecessors

    def filterSuccessor(self, node, relation):
        DG = self.DG
        successors = set()
        for edge in DG.out_edges(node):
            SRC = edge[0]
            TGT = edge[1]
            assert SRC == node
            edge_label = DG[SRC][TGT]['label']
            if edge_label == relation:
                successors.add(TGT)

        return successors

    def getForwardSet(self, node, relation, transpose):
        if not transpose:
            return self.filterPredecessor(node, relation)
        else:
            return self.filterSuccessor(node, relation)

    def getBackwordSet(self, node, relation, transpose):
        if not transpose:
            return self.filterSuccessor(node, relation)
        else:
            return self.filterPredecessor(node, relation)

    def analyzeRelation(self, I, relation, transpose, alpha = 0.25):
        Z = dict()
        for x in I:
    #         print(x)
            # FILTERED by relation
            S_forward = self.getForwardSet(x, relation, transpose)

            for s in S_forward:
                if s not in I:            
    #                 print(s)
                    S_backward = self.getBackwordSet(s, relation, transpose)

                    INTER_1 = S_forward.intersection(I)
                    INTER_2 = S_backward.intersection(I)
                    degree = (((float((1 + len(INTER_1)) * len(INTER_2))) / (len(S_forward) * len(S_backward)))) ** alpha
    #                 print(degree)

                    fuzzy_obj = None
                    if s in Z:
                        fuzzy_obj = Z[s]
                        fuzzy_obj.traditional_merge(s, degree)
                    else:
                        fuzzy_obj = FuzzyElement(s, degree)
                        Z[s] = fuzzy_obj

        return Z

    def union(self, S, T):
        for node in T:
            NEW_fuzzy_obj = T[node]
            fuzzy_obj = None
            if node in S:
                fuzzy_obj = S[node]
                fuzzy_obj.merge(NEW_fuzzy_obj.name, NEW_fuzzy_obj.degree)
            else:
                S[node] = NEW_fuzzy_obj

    def main(self, alpha = 0.25):
        S = dict()

        for relation in self.relations:
            T = self.analyzeRelation(self.I, relation, False)
            self.union(S, T)
            T = self.analyzeRelation(self.I, relation, True)
            self.union(S, T)

        return S
    
    # DG is G1 SG
    def __init__(self, DG, I, relations):
        self.DG = DG
        self.I = I
        self.relations = relations