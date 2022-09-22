import time
import paho.mqtt.client as mqtt
from hal import temperatura, umidade, aquecedor
from definitions import user, password, client_id, server, port


def mensagem(client, userdata, msg):
    vetor = msg.payload.decode().split(',')
    aquecedor('on' if vetor[1] == '1' else'off')
    client.publish(f'v1/{user}/things/{client_id}/response' , f'ok,{vetor[0]}')
    print(vetor)

# conexão inicial
client = mqtt.Client(client_id)
client.username_pw_set(user, password)
client.connect(server, port)

# realizei um mecanismo para o subscribe, assinatura de um topico é um metodo que será invocado, qnd receber uma
# mensagem do servidor
client.on_message = mensagem
client.subscribe(f'v1/{user}/things/{client_id}/cmd/2')
client.loop_start()


# cmportamento do sistema, criei mecanismo para mandar informação para o broker mqtt, aqui posso madar
# varias informações. A informação estou acessando na camada de hardwer
while True:
    client.publish('v1/'+user+'/things/'+client_id+'/data/0', temperatura())
    client.publish('v1/'+user+'/things/'+client_id+'/data/1', umidade())
    time.sleep(10)

# client.disconnect()
