# Kademlia Node Implementation

This is the midterm project for **Practices for Distributed Systems and Cloud Application Development** (NTU, 2025 Fall): a Python implementation of a Kademlia distributed hash table (DHT) node. It supports creating a network, joining one, looking up nodes, and background node health checking.

This repository is the version I reorganized and republished after the course, merging the original core code and the AWS file-migration scripts, which used to live in two separate repos.

## Project Structure

```
Knode.py      Core logic (KademliaNode)
kad.py        Node entry point
xor.py        XOR distance and bucket index
scripts/      File-migration scripts (auto_migrate / migrate_upload / file_exist_checker), used with the nodes on AWS EC2
tests/        Manual integration tests (start the nodes first, see "Testing" below)
```

> Because this is a course assignment, the core parameters (k-bucket sizes, search rounds, etc.) and the paths and ports in the scripts are the assignment's settings, so they are intentionally kept as fixed values.
> `show_bucket()` and `count_msg()` exist only for `tests/` and are not part of the Kademlia protocol.

## Testing

Start the nodes locally, then run the matching test:

| Test | Nodes to start first (127.0.0.1) |
| --- | --- |
| `tests/test3.py` | 11111, 22222, 33333 |
| `tests/test8.py` | 20001 ~ 20008 |
| `tests/test.py`  | 20001 ~ 20016 (covers join, lookup, kill and re-join) |

```bash
python kad.py 127.0.0.1 11111 &   # start each node from the table in turn
python tests/test3.py
```

## Features

* **Create a node**: the Node ID is the SHA-1 of `ip:port`.
* **Join a network**: join an existing Kademlia network through a known node.
* **Look up nodes**: find the closest nodes using XOR distance.
* **Health checking**: a background thread pings known nodes and maintains the list of active ones.
* **Replacement strategy**: dead nodes are replaced by candidates from the replacement cache.

---

## Usage

```bash
python kad.py <ip> <port>
```

**Example**:

```bash
python kad.py 127.0.0.1 20001
```

---

## Core Parameters

* `search_node_per_round`: number of nodes queried per lookup round.
* `search_round_max`: maximum number of lookup rounds.
* `send_back_node`: number of nodes returned by each `send_closest` call.
* `total_k`: maximum number of nodes across the whole k-bucket table.
* `k_value`: maximum number of nodes per bucket.
* `remove_limit`: number of failed pings after which a node is replaced.
* `check_interval`: seconds between background health checks.
* `join_buffer`: seconds a node waits after joining before background pinging starts.

---

## Node Methods

| Method                         | Description                                                        |
| ------------------------------ | ------------------------------------------------------------------ |
| `ping()`                       | Return the node's own IP, port and Node ID                         |
| `create()`                     | Create an empty k-bucket table and start a new network             |
| `start_auto_ping()`            | Start the background ping check                                    |
| `check_nodes()`                | Check node health in the background and replace dead nodes         |
| `join(contact)`                | Join a network through the given contact node                      |
| `find_node(key)`               | Find the closest nodes to a key using a staged expansion strategy  |
| `join_find(key)`               | Look up the node's own position while joining (initial lookup)     |
| `send_closest(key)`            | Return the nodes closest to a key to another node                  |
| `kill()`                       | Terminate the node process                                         |
| `add_node(node_info)`          | Add a node to the k-bucket table or the replacement cache          |
| `replace_dead_node(dead_node)` | Replace a dead node, or mark it inactive if there is no candidate  |

---

## How It Works

1. **Candidate pool (`results`)**

   * All known nodes are kept during a lookup, and the number queried per round is limited (`per_round`).
   * Only some candidates are queried each round, but the pool keeps more nodes to raise the success rate.

2. **Staged expansion**

   * Early rounds query slightly more nodes to spread network information quickly.
   * Later rounds converge gradually to limit message complexity.

3. **Replacement strategy**

   * When a k-bucket is full, extra nodes go into `replacement_cache`.
   * Dead nodes are replaced by cached candidates to keep the network stable.

---

## Dependencies

* `msgpackrpc`: RPC between nodes
* Python standard library: `hashlib`, `os`, `threading`, `time`, `random`

Install the RPC package:

```bash
pip install msgpack-rpc-python
```

On Python 3.13 you may also need `pip install backports.ssl_match_hostname`.

---

## Notes

* Each node's port must be available and reachable by the other nodes.
* The background ping check keeps running; if you change `join_buffer` or `check_interval`, keep them reasonable.
* The bucket size (`k_value`) and total size (`total_k`) affect network coverage and message complexity. With `total_k` = 4 and `k_value` = 1, accuracy may be affected by how nodes join.
