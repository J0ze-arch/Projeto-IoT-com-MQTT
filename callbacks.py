from application.configs.mqtt_broker_configs import mqtt_broker_configs
import json
import streamlit as st

received_data = []

def on_connect(client, userdata, flags, rc, message):
    if rc == 0:
        print(f'Conectado: {client}')
        client.subscribe(mqtt_broker_configs['TOPIC'])
    else:
        print(f'Erro ao me conectar! Codigo ={rc}')

def on_subscribe(client, userdata, mid, granted_qos, message):
    print(f'Cliente inscrito no {mqtt_broker_configs["TOPIC"]}')

def on_message(client, userdata, message):
    payload_str = message.payload.decode("utf-8")
    print(f'Recebido: {payload_str}')
    try:
        dados = json.loads(payload_str)
        print(f'Dados processados: {dados}')
        received_data.append(dados)

    except json.JSONDecodeError:
        print('A mensagem nao e um json valido')