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



Assignment 2 Exercise 1 - Spawn a thread in the server to work as the server operator. This way it will be possible interact with the server while
it is running. The operator should display the number of users connected via the command “num users”.
To test the operator, start the server and check “num users” when different amounts of clients are connected.

 = There will be server and clients. The server should handel many clients using threads and should show number of clients connected/talking currently to the server using cmd query num users. Whenever a client end the connection and server check num users again it should show the real time no of connected users.

 Exercise 2 - The interaction between clients and servers involved only sending text messages so far, it is time to create a message
format to enable the sending of structured data. We are going to use Google’s protobuf to design our format. Install
protobuf both for Java (or the language of your choice) and for your operating system, and then compile the format
file provided using the command “protoc --java out=. msgFormat.proto”. In our format a normal message will have
the following fields:
1. int32 fr, specifying who’s sending the message;
2. int32 to, specifying to whom the message is addressed;
3. string msg, specifying the message content.
Integrate protobuf to your project and test the client-server interaction. The server should echo the message back to
the client, as done in the previous assignments.
Java tip: if you want to run your code from the CLI, compile all files using your IDE and run a command similar
to “java -cp protobuf-java-3.21.7.jar:./ exercise1.Server” in the parent folder of where the .class files are located;
“cp” stands for classpath and includes the jar and the current folder, separated by a colon. If you are using Windows,
run a command similar to “java -cp “protobuf-java-3.21.7.jar;./” exercise1.Server” instead. Remember to have the
protobuf jar in the folder!

= Here we have to use proctocol buffer of Google which is used to send specific, structured data to the client.
1 string value and 2 interger value

Assume it as client is a courier man that delivers package(in this case message) to destination address ie.. server

Exercise 3 - To introduce a hand shake protocol between server and client.

Its like having a handshake before starting the communication like we humans do.
Just to let server and client know that they are connected.
