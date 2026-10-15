import socket
import os

def getURL(ans):
    """
    return the URL from the client request
    :param ans:
    :return: 
    """
    line1 = ans.split('\r\n')[0]
    return line1.split(' ')[1][1:]

def check_get_packet(ans):      # Targil3
    """
    check_packet from the client request
    :param ans:
    :return:
    """
    valid = False
    line1 = ans.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == 'HTTP/1.1':
        valid = True
    return valid


server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 80)) #80\8080
server_soc.listen(3)

while True:
    client_soc, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_soc.recv(1024).decode()
    except Exception as e:
        print(f"error in receive {str(e)}")
        client_soc.close()
        continue

    if not check_get_packet(data):  # Targil3
        client_soc.close()

    else:
        url = getURL(data) # call the function
        print(url)
        if os.path.exists(url):
            ans = f"HTTP/1.1 200 OK\r\nConstant-Length: {str(len(data))}\r\n\r\n{url}"
            try:
                client_soc.send(ans.encode())
            except Exception as e:
                print(f"error in send {str(e)}")

        else:
            error = "404 / File Not Found"
            try:
                client_soc.send(error.encode())
            except Exception as e:
                print(f"error in send {str(e)}")


        client_soc.close() # Targil1