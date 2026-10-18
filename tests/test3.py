import msgpackrpc, time
import hashlib

def node_id_of(port, ip="127.0.0.1"): #same rule as KademliaNode: sha1("ip:port")
    return hashlib.sha1(f"{ip}:{port}".encode()).hexdigest()


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))

# 建立節點
client_1 = new_client("127.0.0.1", 11111)
client_2 = new_client("127.0.0.1", 22222)
client_3 = new_client("127.0.0.1", 33333)



# 讓 20001 建立網路
client_1.call("create")
print("Network created on 11111")

# 讓其他節點加入
client_2.call("join", client_1.call("ping"))
print("Node 22222 joined")

client_3.call("join", client_2.call("ping"))
print("Node 33333 joined")



# 測試 find_node
time.sleep(5)
print(f"\nSearching for 33333 from node 11111...")
result1 = client_1.call("find_node", node_id_of(33333))
print("Find node result:", result1)
time.sleep(2)
print(f"\nSearching for 11111 from node 33333...")
result2 = client_3.call("find_node", node_id_of(11111))
print("Find node result:", result2)

# 顯示每個節點的 kbucket 狀況
print("\n--- K-BUCKET STATE ---")
print("11111:", client_1.call("show_bucket"))
print("22222:", client_2.call("show_bucket"))
print("33333:", client_3.call("show_bucket"))
