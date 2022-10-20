import argparse
import subprocess

parser = argparse.ArgumentParser(description="simple client-server program to exchange encrypted messages")
parser.add_argument('--listen', default=False,help='if True: run the script in server mode if False: run the script in client mode default: False',action=argparse.BooleanOptionalAction)
parser.add_argument('--key', help='Specify the secret key for the encryption/decryption default: empty string',default='')
parser.add_argument('--algorithm', default='pbkdf2',help='Specify the encryption/decryption algorithm default: -pbkdf2')
parser.add_argument('--hostname', default='127.0.0.1',help='In client mode, specify the ip address of the server default: localhost')
parser.add_argument('port',help='Specify the port number of the server')
args = parser.parse_args()
print(args.listen)
if args.listen:
    #1. start the server on the given port
    proc = subprocess.Popen(['nc','-l',args.port],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    #2. incapsulate the Received message from the client
    message = proc.stdout.readline()
    #3. show the message
    print("NUOVO MESSAGGIO:"+str(message))
    #4 decrypt the message
    proc2 = subprocess.run(['openssl',args.algorithm,'-d','-k',args.key,'-base64'],stdout=subprocess.PIPE,input=message.encode("utf-8"))
    decMessage = proc2.stdout
    print("messaggio decriptato: "+str(decMessage))
else:
    #1. write the message on the console
    message = input("inserisci il messaggio:")
    #print("messaggio criptato:")
    #2 encrypt the message
    proc2 = subprocess.run(['openssl',args.algorithm,'-k',args.key,'-base64'],stdout=subprocess.PIPE,input=message.encode("utf-8"))
    encMessage = proc2.stdout
    print("messaggio criptato: "+str(encMessage))
    #3. Connect to the specified ip address of the server
    proc = subprocess.Popen(['nc',args.hostname,args.port],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)

    #4 send the encrypted message to the server
    proc.stdin.write(encMessage)
    
#encrypt command
#echo "ciao" | openssl aes-256-cbc -k miapass -base64

#decrypt command
#echo "U2FsdGVkX18l2hjks6Uw6h28olSRVa0AY/cQ3Ayxzi0=" | openssl aes-256-cbc -d -k miapass -base64