import sys
import json
from client import LouvainCommunityDetector

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-louvain-modularity-community-detection-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "detect_graph_communities",
                        "description": "Partition graph into modularity-maximizing communities via Louvain algorithm",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "adjacency": {
                                    "type": "object",
                                    "description": "Map of node -> {neighbor: weight}"
                                }
                            },
                            "required": ["adjacency"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "detect_graph_communities":
            raw_adj = args.get("adjacency", {})
            adj = {int(k) if k.isdigit() else k: {int(vk) if vk.isdigit() else vk: float(w) for vk, w in v.items()} for k, v in raw_adj.items()}
            detector = LouvainCommunityDetector(adj)
            comms = detector.detect_communities()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"communities": comms, "count": len(comms)})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
