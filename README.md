Assignment 1 Exercise 1 - Create a Server that listen data from client and print that. Start a connection listen the client using s.listen
Accept the connection using s.accept
check if the connection with client is made using with
print the connection details of the client if messaged is received from the client decode that and print that message And at last close the connection

Exercise 2 - Create a client and Server listen data from client and print that and send a confirmation and same data back to client that he received this info and close the connection. Server side:
listen the client using s.listen
Accept the connection using s.accept
check if the connection with client is made using with
print the connection details of the client
Send the same data back to client with a confirmation
And at last close the connection

Client Side: connect to the server using connect. Send data to server using sendall. Receive data and confirmation from server that he got the data. Print the received data from the server.

Exercise 3 - 3 threads will start. Give each of them a id then they should sleep for some time and then wake up and say we are awake. And remember all this is happening parallely.

So the flow should be:
1) Create thread
2) Then make a function that will assign some time to thread and make then sleep for that random time.
3) Finally start the thead with thread.start(), Each thread will call the function.
