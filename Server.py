
   
#Kütüphaneler import ediliyor
import socket
from threading import Thread

#Server Fonksiyonlari
def broadcast(msg,prefix=""): # msg:message to broadcast, prefix: sender ideftification  
	# broadcast message to the all clients
	for client_socket in clients:
		client_socket.send(prefix.encode("utf-8")+ msg)







# Baglantilari Kabul Etme Fonksiyonlari

def accept_connections():  # Gelen Clientlerin Baglanti Taleplerini Kabul Etme	
	while True:  # Baglanti Bekleme
		client_conn,client_address = server.accept()  # Client soketi ve client adresi(ip,port) donduruyor
		print("{0}:{1} has connected.".format(client_address[0],client_address[1]))

		client_conn.send("Please type your name and enter:".encode("utf-8"))  # Baglanan cliente ismi soruluyor
		adresses[client_conn] = client_address # add connected client adress to the adresses dict
		Thread(target = handle_client,args = (client_conn,)).start()  # starting thread ps: init thread for every connection


# HANDLE CLİENT

def handle_client(client):

	name = client.recv(BUFFER_SIZE).decode("utf-8") # get client name
	clients[client] = name # add client name to the clients dict.

	hello_msg = "Hi {0}. If you ever want to quit, type kapanbaba".format(name) + "+"
	tmp = " "
	tmp = tmp.join(list(clients.values()))

	hello_msg = hello_msg + tmp

	client.send(hello_msg.encode("utf-8")) #send hello message to the user

	join_msg = "{0} joined to the chat room".format(name) + "+"
	tmp = " "
	tmp = tmp.join(list(clients.values()))
	join_msg = join_msg + tmp
	broadcast(join_msg.encode("utf-8"))  # broad cast the message to the all users.
	
	
	while True:
		client_msg = client.recv(BUFFER_SIZE) #receive client's message
		decoded_msg = client_msg.decode("utf-8")
		 

		if(decoded_msg == "kapanbaba"):
			client.send(bytes("{quit}", "utf-8"))
			client.close()  #close connection

			del clients[client] # delete client from dict
			broadcast(bytes("{0} has left the chat".format(name),"utf-8"))
			break
			
		

		elif(decoded_msg.find("$")!=-1 and decoded_msg.find("+")!=-1):
			decoded_msg = decoded_msg.split("$")[1].split("+")[0]
			encoded_msg = decoded_msg.encode("utf-8")
			broadcast(encoded_msg,name+": ")




		else:  # send message
			if name in messages.keys(): 
				messages[name] = messages[name] + "," + decoded_msg 
			else:
				messages[name] = decoded_msg

			broadcast(client_msg,name+": ")


clients = {} # dict for clients that connected to the server
adresses= {} # dict Connected client's adresses

messages={}




TCP_IP = "127.0.0.1"
TCP_PORT = 5005  #server port number
BUFFER_SIZE = 1024 # server input buffer size

server = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM, proto = 0) # create socket for server
server.bind((TCP_IP,TCP_PORT))  # bind socket adress to server



if __name__ == "__main__":
	server.listen(5) # max 5 connection
	print("Waiting for connection...")
	thread = Thread(target=accept_connections)
	thread.start()
	thread.join()
	server.close()
