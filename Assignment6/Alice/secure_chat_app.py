import socket as sc
import ssl
from sys import argv

#chat headers that will be used in the communication
CHAT_HELLO = 'CHAT_HELLO'
CHAT_REPLY = 'CHAT_REPLY'
CHAT_STARTTLS = 'CHAT_STARTTLS'
CHAT_STARTTLS_ACK = 'CHAT_STARTTLS_ACK'
CHAT_STARTTLS_NOT_SUPPORTED = 'CHAT_STARTTLS_NOT_SUPPORTED'
CHAT_CLOSE = 'CHAT_CLOSE'

# Alice acts as client
class alice_Client:
    def __init__(self,hostname,serverport):
        #creating a send socket
        self.sendsock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)


        try:
            self.host_ip = sc.gethostbyname(hostname)         #using gethostbyname to find the ip adress fom domain name
        except sc.gaierror:
            print("Error resolving the host")
            exit()

        self.S_hostname=hostname
        self.start_connection() # Function call to start the connection
        self.close_connection() # Function call to stop the connection

    #start the connection
    def start_connection(self):
        self.sendsock.connect((self.host_ip,serverport))
        print(f"Connected successfully to {self.host_ip}")


        self.sendsock.sendall(CHAT_HELLO.encode())
        data = self.sendsock.recv(1024)
        print(f"recieved the data --->   {data.decode()}")


        # chat_STARTTLS
        self.sendsock.sendall(CHAT_STARTTLS.encode())
        data = self.sendsock.recv(1024)
        print("recieved data ", data.decode())
        print(f"recieved data --->  {data.decode()} ")


        if data.decode() == CHAT_STARTTLS_ACK:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations('root.crt')                           #load the root certiicate
            context.load_cert_chain('Alice/alice.crt', 'Alice/alice_pvtkey_new.pem')   #load the certificates and private key of Alice
            context.verify_mode = ssl.CERT_REQUIRED #set the mode to certicates required

            self.sendsock = context.wrap_socket(
                self.sendsock, server_hostname=self.S_hostname, do_handshake_on_connect=True)
            print('SSL certificates verified successfully')

        #if there is no TLs--> we ll have to proceed in unsecure methods
        elif (data.decode() == CHAT_STARTTLS_NOT_SUPPORTED):
            print('Continuing in TCP connection')

        #Continuous chatting

        while (True):
            data1 = input('Enter the message to be sent: ')
            self.sendsock.sendall(data1.encode())
            if (data1 == CHAT_CLOSE):
                break
            print('Waiting for message . . .')
            data = self.sendsock.recv(1024)
            print("recieved ", data.decode())
            if (data.decode() == CHAT_CLOSE):
                break

    #close the sendsocket
    def close_connection(self):
        self.sendsock.close()

class bob_Server:
    def __init__(self,serverport):
        self.recvsock=sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        self.recvsock.bind(('',serverport))
        self.recvsock.listen(1)
        print("waiting for client for connection")


        self.sendsock,self.sender_addr=self.recvsock.accept()
        print(f"recieved the connection from client {self.sender_addr}")

        self.hello = False
        self.tls_count= False

        self.start_connection()
        self.close_connection()


    def start_connection(self):
        while (True):
            print("Waiting for the message to be received ..... ")
            data = self.sendsock.recv(1024)
            print(f"Received! {data.decode()}")
            # chat_hello
            if data.decode() == CHAT_HELLO and self.hello == False:
                self.sendsock.sendall(CHAT_REPLY.encode())
                self.hello = True
            # chat_STARTTLS
            elif data.decode() == CHAT_STARTTLS and self.tls_count == False:
                self.sendsock.sendall(CHAT_STARTTLS_ACK.encode())

                # Loading Keys and Certificates
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_verify_locations(
                    'root.crt')
                context.load_cert_chain('Bob/bob.crt', 'Bob/bob_pvtkey_new.pem')
                context.verify_mode = ssl.CERT_REQUIRED
                self.sendsock = context.wrap_socket(
                    self.sendsock, server_side=True, do_handshake_on_connect=True)

                self.tls_count = True
                print('Secure TLS 1.3 pipe Established')

            # chat_close
            elif (data.decode() == CHAT_CLOSE):
                break
            # else
            else:
                send_data = input('Enter message to send: ')
                self.sendsock.sendall(send_data.encode())
                if (send_data == CHAT_CLOSE):
                    break

    def close_connection(self):
        # closing the connections
        self.sendsock.close()
        self.recvsock.close()


if __name__ == "__main__":
    serverport=int(input("Enter the serverport "))
    if(len(argv) == 3 and argv[1] == "-c"):
        alice_Client(argv[2],serverport)
    elif (len(argv) == 2 and argv[1] == "-s"):
        bob_Server(serverport)
    else:
        print("Command Syntax Error")
        print("Correct Syntax -> \n Server: -s \n Client: -c <serverhostname>")
        exit()

