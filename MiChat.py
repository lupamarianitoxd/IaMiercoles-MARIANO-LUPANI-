# IMPORTAMOS Streamlit
# pip install python | python -m install streamlit


# pip install python | python -m install streamlit

import streamlit as st
from groq import Groq

st.set_page_config(page_title="Inteligencia Artificial Mariano Lupani", page_icon="clase6/img/logo.jpg")
st.title("Mi primer chat con MarIAno")

nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    if nombre == "":
        st.write("Hola, ingrese su nombre")
    else:
        st.write(f"Hola {nombre}! Yo soy MarIAno, como puedo ayudarte?")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.title("Mi Chat con MarIAno")
    st.sidebar.title("Configuracion de MarIAno")

    elegiModelo = st.sidebar.selectbox(
        "Elegí un modelo",
        options = MODELOS,
        index = 0
    )

    return elegiModelo


def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

# python -m streamlit run index.py (aca deben ingresar el nombre del archivo)
# como hago para que me mande al navegador???

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main ():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat()  # Nuevo
    mensaje = st.chat_input("Escribí tu mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, "😁")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant", avatar="🤖"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()


if __name__ == "__main__":
    main()



#chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
#actualizar_historial("assistant", chat_completo, "🤖")
#st.rerun()


#Para activar el entorno virtual
#python -m venv venv
#.\venv\Scripts\activate
#python -m pip install streamlit
#pip install groq
#streamlit run MiChat.py
