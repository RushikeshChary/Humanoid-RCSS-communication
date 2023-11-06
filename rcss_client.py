# # import socket

# # port = 6000
# # server = "local host"








# # # Create a socket object
# # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # # Define the server address and port to connect to
# # server_address = ('localhost', 6000)  # Use the same address and port as the server

# # # Connect to the server
# # client_socket.connect(server_address)

# # # Send data to the server
# # message = "Hello, server!"
# # client_socket.send(message.encode())

# # # Receive the server's response
# # response = client_socket.recv(1024)
# # print(f"Received from server: {response.decode()}")

# # # Close the client socket
# # client_socket.close()



# import socket
# import sys
# import select
# import signal
# import os

# class Client:
#     def __init__(self, server, port):
#         self.M_dest = (server, port)
#         self.M_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.M_transport = None
#         self.M_comp_level = -1
#         self.M_clean_cycle = True
#         self.M_gz_buf = None  # Optional, if you have compression

#         self.open()
#         self.bind()

#     def open(self):
#         try:
#             self.M_socket.setblocking(0)  # Make the socket non-blocking
#         except socket.error as e:
#             print(f"Error setting socket non-blocking: {e}")
#             self.M_socket.close()
#             return -1

#         self.M_transport = self.M_socket

#     def bind(self):
#         try:
#             self.M_socket.bind(('127.0.0.1', 0))
#         except socket.error as e:
#             print(f"Error binding socket: {e}")
#             self.M_socket.close()
#             return -1

# # This is for data compression.


#     # def setCompression(self, level):
#     #     if level >= 0:
#     #         if not self.M_gz_buf:
#     #             self.M_gz_buf = None  # You can create the gzstreambuf here if needed
#     #         self.M_gz_buf.setLevel(level)
#     #         self.M_transport = self.M_gz_buf
#     #     else:
#     #         self.M_transport = self.M_socket
#     #     self.M_comp_level = level


#     def processMsg(self, msg):
#         if self.M_comp_level >= 0:
#             # Decompression logic here if needed
#             pass
#         else:
#             self.parseMsg(msg)

#     def parseMsg(self, msg):
#         if msg.startswith("(ok compression"):
#             level = int(msg.split(" ")[-2])
#             self.setCompression(level)
#         elif msg.startswith("(sense_body") or msg.startswith("(see_global") or msg.startswith("(init"):
#             self.M_clean_cycle = True

#         print(msg)

#     def messageLoop(self):
#         while True:
#             readable, _, _ = select.select([self.M_socket], [], [], 0)
#             for sock in readable:
#                 if sock == self.M_socket:
#                     data, _ = sock.recvfrom(6000)
#                     if data:
#                         self.processMsg(data.decode())
#                 else:
#                     # Handle other sockets if needed
#                     pass

# def sig_exit_handle(signal, frame):
#     print("\nKilled. Exiting...")
#     if client:
#         client.close()
#     # sys.exit(EXIT_FAILURE)

# if __name__ == "__main__":
#     server_address = "localhost"
#     server_port = 6000

#     client = Client(server_address, server_port)
#     signal.signal(signal.SIGINT, sig_exit_handle)
#     client.messageLoop()


import socket
import sys
import select
import threading
import errno

def receive_and_print_thread(M_socket):
    size = 8192
    while True:
        try:
            data = M_socket.recvfrom(size)
            if not data[0]:
                sys.stderr.write(f"Error receiving data from server\n")
                break
            print(data[0].decode('utf-8'))
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                sys.stderr.write("Connection refused by the server\n")
                break
            else:
                raise

def input_thread(M_socket, server_address):
    while True:
        input_data = input("")
        M_socket.sendto(input_data.encode('utf-8'), server_address)

def main():
    server_port = 6000
    server_address = ('localhost', server_port)
    M_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    team_name = input("")
    init_message = f"{team_name}"
    M_socket.sendto(init_message.encode('utf-8'), server_address)
    receive_thread = threading.Thread(target=receive_and_print_thread, args=(M_socket,))
    input_thread_worker = threading.Thread(target=input_thread, args=(M_socket, server_address))

    receive_thread.start()
    input_thread_worker.start()

    receive_thread.join()
    input_thread_worker.join()

if __name__ == '__main__':
    main()
