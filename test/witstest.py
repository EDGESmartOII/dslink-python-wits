import dslink
import pdb
import socket
import time
from icecream import ic

class EdgesmartWitsClient:

    def __init__(self, tcp_ip, tcp_port, buffer_size=2048):
        print("You initialized me!!!")
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.file_name = file_name

    # Function to connect to the wits server
    def wits_connect(self):
        print("[*] Connecting...........")
        self.session.connect_ex((self.tcp_ip, self.tcp_port))
        print("Connected")


    def wits_get_data(self):
        print("Got to the get data function")
        message = self.session.recv(self.buffer_size)
        received_data = message.decode("utf-8")
        ic(received_data)

    # Function to disconnect from the server and close the session
    def wits_disconnect(self):
        self.session.close()

class EDGEsmartDSLink(dslink.DSLink):
    def start(self):
        self.responder.profile_manager.create_profile("connect")
        self.responder.profile_manager.register_callback("connect", self.connect)

        self.responder.profile_manager.create_profile("testfunc")
        self.responder.profile_manager.register_callback("testfunc", self.connect)


    def get_default_nodes(self, super_root):
        conn = dslink.Node("Connect", super_root)
        conn.set_display_name("TestName")
        #conn.set_writable("config")
        conn.set_profile("connect")
        conn.set_invokable("write")
        conn.set_parameters([
            {
                "name": "IP Address",
                "type": "string",
                "default": "192.168.100.165"
            },
            {
                "name": "Port Number",
                "type": "int",
                "default": 6341
            },
            {
                "name": "Buffer",
                "type": "int",
                "default": 1024
            },
            {
                "name": "Toggle",
                "type": "bool",
                "default": False
            }
        ])

        func = dslink.Node("TestFunc", super_root)
        func.set_display_name("TestFunction")
        func.set_profile("testfunc")
        func.set_invokable("write")
        func.set_parameters([
            {
                "name": "IP Address",
                "type": "string",
                "default": "192.168.100.165"
            },
            {
                "name": "Port Number",
                "type": "int",
                "default": 6341
            },
            {
                "name": "Buffer",
                "type": "int",
                "default": 1024
            },
            {
                "name": "Toggle",
                "type": "bool",
                "default": False
            }
        ])

        super_root.add_child(conn)
        super_root.add_child(func)

    def connect(self, parameters):
        #Get the connection parameters from the user
        ip = parameters[1]["IP Address"] # Parse number
        port = int(parameters[1]["Port Number"]) # Parse number
        buff = int(parameters[1]["Buffer"]) #Parse Number

        pdb.set_trace()

        #Initialzie the WITS client and connect
        wits_client = EdgesmartWitsClient(ip, port, buff)
        wits_client.wits_connect()

        #Gets super root of the link node. This is used for
        #publishing the connection params after we connect
        sr = self.responder.get_super_root()

        #Check if the nodes exist. If not, create them
        if not sr.has_child("ip_add"):
            sr.create_child("ip_add")
            sr.get("/ip_add").set_type("string")

        if not sr.has_child("port"):
            sr.create_child("port")
            sr.get("/port").set_type("int")

        if not sr.has_child("buffer"):
            sr.create_child("buffer")
            sr.get("/buffer").set_type("int")

        #Setting the connection parameters
        sr.get("/ip_add").set_value(ip)
        sr.get("/port").set_value(port)
        sr.get("/buffer").set_value(buff)

        print("Populated connection data")

    def testfunc(self, parameters):
        print("In TESTFUNC")

if __name__ == '__main__':
    try:
        EDGEsmartDSLink(dslink.Configuration("EDGEsmartWITS", requester=True, responder=True))
    except KeyboardInterrupt:
        print("Got outta here")
