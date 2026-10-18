import msgpackrpc
import sys
from Knode import KademliaNode

def get_config(): #read ip, port
    if len(sys.argv) != 3:
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    return ip, port


if __name__ == "__main__":
    MyIP, MyPort = get_config()

    # create RPC server
    node = KademliaNode(MyIP, MyPort)
    server = msgpackrpc.Server(node)
    server.listen(msgpackrpc.Address(MyIP, MyPort))
    print(f"Kademlia node listening on {MyIP}:{MyPort}")
    server.start()

