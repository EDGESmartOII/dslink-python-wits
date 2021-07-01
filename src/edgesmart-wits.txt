import dslink
import socket

class EdgesmartWitsClient:
    # Create a TCP/IP socket
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, tcp_ip, tcp_port, buffer_size=2048):
        print("You initialized me!!!")
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        #self.file_name = file_name

    # Function to connect to the wits server
    def wits_connect(self):

        while True:

            try:

                # Check if a network port is open
                server_location = self.session.connect_ex((self.tcp_ip, self.tcp_port))
                print("[*] Connecting...........")
                if server_location == 0:

                    while True:

                        # Assign the recived data to message variable
                        message = self.session.recv(self.buffer_size)

                        # Decode the received data with variable-width character
                        received_data = message.decode("utf-8")

                        # Check if no data is received
                        if len(received_data) == 0:
                            break
                        else:
                            print(received_data)
                else:
                    print("Port is not open")

            # Raise exception when the server is disconnected
            except socket.error as e:
                print("[*] The WITS client cannot connect to the server")
                print("[*] Reason: {} ".format(e))
                print("[*] Trying to connect.......")

    # Function to disconnect from the server and close the session
    def wits_disconnect(self):
        self.session.close()

class EDGEsmartDSLink(dslink.DSLink):
    def start(self):
        self.responder.profile_manager.create_profile("connect")
        self.responder.profile_manager.register_callback("connect", self.connect)


    def get_default_nodes(self, super_root):
        conn = dslink.Node("Connect", super_root)
        conn.set_display_name("Connect")
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
            }
        ])

        super_root.add_child(conn)

    def connect(self, parameters):
        ip = str(parameters[1]["IP Address"]) # Parse number
        port = int(parameters[1]["Port Number"]) # Parse number
        wits_client = EdgesmartWitsClient(ip, port)
        print("Connecting. . . ")
        wits_client.wits_connect()

def main():
    #TCP_IP = '192.168.1.143'
    #TCP_PORT = 6341
    #BUFFER_SIZE_INITIAL = 1024
    #FILE_NAME = 'WITSUserDefineRecordItems.csv'

    EDGEsmartDSLink(dslink.Configuration("EDGEsmartWITS", requester=True, responder=True))
    #try:
    #    print("Starting client")
    #    wits_client.wits_connect()

    #except KeyboardInterrupt:
    #    print('Interrupted')
    #    wits_client.wits_disconnect()

if __name__ == '__main__':
    #main()
    EDGEsmartDSLink(dslink.Configuration("EDGEsmartWITS", requester=True, responder=True))
