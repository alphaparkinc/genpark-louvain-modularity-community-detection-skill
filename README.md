# genpark-louvain-modularity-community-detection-skill

Agent Skill implementing the **Louvain Method for Community Detection** through local modularity optimization and partition extraction.

## Architectural Overview
```mermaid
flowchart TD
    Adj["Graph Adjacency List"] --> Init["Assign Each Node to Singleton Community"]
    Init --> Eval["Evaluate Modularity Q = sum_c (in_c/(2m) - (tot_c/(2m))^2)"]
    Eval --> Test["Greedy Neighbor Swap: If Delta Q > 0, Move Node"]
    Test --> Converged{"No Further Gain ?"}
    Converged -- No --> Test
    Converged -- Yes --> Groups["Extract Community Membership Clusters"]
```
