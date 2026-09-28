"""Louvain Modularity Community Detection Engine.
100% Python Standard Library.
"""

import collections

class LouvainCommunityDetector:
    """Louvain method for greedy modularity maximization community detection."""
    def __init__(self, adj_dict):
        self.adj = adj_dict
        self.nodes = list(adj_dict.keys())
        self.m = sum(sum(nbrs.values()) for nbrs in adj_dict.values()) / 2.0 or 1.0

    def compute_modularity(self, community):
        two_m = 2.0 * self.m
        comm_nodes = collections.defaultdict(list)
        for node, c in community.items():
            comm_nodes[c].append(node)
        q = 0.0
        for c, nodes in comm_nodes.items():
            node_set = set(nodes)
            in_weight = 0.0
            tot_weight = 0.0
            for u in nodes:
                for v, w in self.adj[u].items():
                    tot_weight += w
                    if v in node_set:
                        in_weight += w
            q += (in_weight / two_m) - ((tot_weight / two_m) ** 2)
        return q

    def detect_communities(self, max_iter=15):
        community = {node: i for i, node in enumerate(self.nodes)}
        cur_q = self.compute_modularity(community)

        for _ in range(max_iter):
            improved = False
            for u in self.nodes:
                best_c = community[u]
                best_q = cur_q
                neighbor_comms = {community[v] for v in self.adj[u]}
                for cand_c in neighbor_comms:
                    if cand_c == community[u]:
                        continue
                    community[u] = cand_c
                    cand_q = self.compute_modularity(community)
                    if cand_q > best_q:
                        best_q = cand_q
                        best_c = cand_c
                    community[u] = best_c

                if best_q > cur_q + 1e-9:
                    community[u] = best_c
                    cur_q = best_q
                    improved = True

            if not improved:
                break

        groups = collections.defaultdict(list)
        for node, c in community.items():
            groups[c].append(node)
        return list(groups.values())
