import streamlit as st
import pandas as pd
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from application.configs.mqtt_broker_configs import mqtt_broker_configs
from application.main.mqtt_connection.mqtt_client_connection import MqttClientConnection
from application.main.mqtt_connection.callbacks import received_data
import time

st.set_page_config(page_title="Monitoramento Sensor", layout="centered")

st.title("Monitoramento do sensor")

if "mqtt_connected" not in st.session_state:
    client = MqttClientConnection(
        mqtt_broker_configs["HOST"],
        mqtt_broker_configs["PORT"],
        mqtt_broker_configs["CLIENT_NAME"],
        mqtt_broker_configs["KEEPALIVE"]
    )
    client.start_connection()
    st.session_state["mqtt_connected"] = True

placeholder = st.empty()

while True:
    with placeholder.container():
        if received_data:
            last_data = received_data[-1]
            temp = last_data.get('temperatura', 0)
            umid = last_data.get('umidade_solo', 0)

            col2, col3 = st.columns(2)

            with col2:
                st.metric(label="Temperatura", value=f'{temp}°C')
            
            with col2:
                st.metric(label="Umidade do solo:", value=f'{umid}%')

        else:
            st.info('Aguardando leitura do sensor...')
            
    time.sleep(0.5)

