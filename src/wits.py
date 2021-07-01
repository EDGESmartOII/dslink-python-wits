import socket


class EdgesmartWitsClient:
    # Create a TCP/IP socket
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, tcp_ip, tcp_port, file_name, buffer_size=2048):
        print("You initialized me!!!")
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.buffer_size = buffer_size
        self.file_name = file_name

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


def main():
    TCP_IP = '192.168.1.143'
    TCP_PORT = 6341
    BUFFER_SIZE_INITIAL = 1024
    FILE_NAME = 'WITSUserDefineRecordItems.csv'

    wits_client = EdgesmartWitsClient(TCP_IP, TCP_PORT, FILE_NAME)

    try:
        wits_client.wits_connect()

    except KeyboardInterrupt:
        print('Interrupted')
        wits_client.wits_disconnect()


if __name__ == '__main__':
    main()

