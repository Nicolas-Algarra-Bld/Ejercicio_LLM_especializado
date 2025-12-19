import streamlit as st
import boto3
import json
import os

# Configuración
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Cliente Bedrock
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

SYSTEM_PROMPT = """
Eres un asistente experto en AWS Cloud Practitioner,
con amplio conocimiento en conceptos fundamentales de computación en la nube,
servicios principales de AWS, seguridad, facturación y modelos de precios.

Tu audiencia son estudiantes y personas que se preparan
para la certificación AWS Cloud Practitioner,
con conocimientos básicos o iniciales de tecnología.

Tu objetivo es ayudarles a:
- Comprender los conceptos clave de cloud computing
- Identificar y entender los servicios principales de AWS
- Prepararse para preguntas tipo examen de la certificación
- Comprender buenas prácticas básicas de seguridad y costos en AWS

Estilo de respuesta:
- Claro, didáctico y fácil de entender
- Evita jerga técnica innecesaria
- Usa ejemplos simples y cotidianos cuando sea posible
- Utiliza listas o pasos para estructurar la información

Formato recomendado al explicar un concepto:
1. Definición breve
2. Para qué se usa
3. Ejemplo simple en AWS

Reglas:
- No inventes servicios ni características de AWS
- No profundices en configuraciones avanzadas o técnicas de nivel asociado/profesional
- Si la pregunta es ambigua, solicita aclaración
- Si no conoces la respuesta, indícalo claramente
- Mantente siempre dentro del alcance de AWS Cloud Practitioner
"""
# Configuración de Streamlit
st.set_page_config(page_title="Asistente AWS Cloud Practitioner")
st.title("Experto AWS Cloud Practitioner")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]

# Mostrar historial
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para Bedrock
    messages_for_bedrock = []
    for m in st.session_state.messages:
        messages_for_bedrock.append(
            {"role": m["role"], "content": [{"text": m["content"]}]} 
        )

    # Llamada a Bedrock con API 'converse'
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=messages_for_bedrock,
        inferenceConfig={"maxTokens": 500, "temperature": 0.6}
    )

    # Extraer respuesta del asistente
    assistant_reply = response["output"]["message"]["content"][0]["text"]

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)