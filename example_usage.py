from client import LouvainCommunityDetector

graph = {
    1: {2: 1.0, 3: 1.0},
    2: {1: 1.0, 3: 1.0},
    3: {1: 1.0, 2: 1.0, 4: 0.1},
    4: {3: 0.1, 5: 1.0, 6: 1.0},
    5: {4: 1.0, 6: 1.0},
    6: {4: 1.0, 5: 1.0}
}
detector = LouvainCommunityDetector(graph)
communities = detector.detect_communities()

print("Louvain Communities Detected:", communities)
