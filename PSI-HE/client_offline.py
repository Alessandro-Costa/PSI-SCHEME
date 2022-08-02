import pickle
from oprf import client_prf_offline, order_of_generator, G
from time import time

# client's PRF secret key (a value from  range(order_of_generator))
oprf_client_key = 12345678910111213141516171819222222222222
t0 = time()

# key * generator of elliptic curve
client_point_precomputed = (oprf_client_key % order_of_generator) * G

client_set = []
inputFileName = input("Inserisci il nome di un file di input (PER ESEMPIO BASE 'pswclient.txt': ")
inputFileName = open(inputFileName, 'r')
print("File aperto", inputFileName, "per lettura.")
ilines = inputFileName.readlines()
for item in ilines:
	client_set.append(int(item[:-1].encode('utf-8').hex(),16))


# OPRF layer: encode the client's set as elliptic curve points.
encoded_client_set = [client_prf_offline(item, client_point_precomputed) for item in client_set]


g = open('client_preprocessed', 'wb')
pickle.dump(encoded_client_set, g)
g.close()   
t1 = time()
print('Client OFFLINE time: {:.2f}s'.format(t1-t0))

# Mi creo il file in locale dell'intersezione delle psswd
h = open('intersection', 'w')
s = open('pswserver.txt','r')

slines = s.readlines()
for i in ilines:
	for j in slines:
		if i == j:
			h.write(i)
			break
inputFileName.close()
s.close()
h.close()
