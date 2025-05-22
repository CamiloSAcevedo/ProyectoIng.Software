#Archivo para generar texto de anuncios de vacantes utilizando la API de Gemini
# -------------------------------------------------- Gemini Api -----------------------------------------

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generar_texto_ads(prompt):
    try:
        response = model.generate_content(f"""
        Genera un texto para publicar esta vacante en redes sociales. Debe ser directo, profesional y llamar la atención.
        Máximo 250 caracteres.

        Descripción: {prompt}
        """)
        texto = response.text.strip()
        return texto[:250]
    except Exception as e:
        return f"Error al generar el texto: {e}"

def generar_message_creative(prompt, vacante_info=""):
    try:
        response = model.generate_content(f"""
        Genera un texto para el mensaje de un creative de Meta Ads. Debe ser directo, profesional y llamar la atención.
        Usa un tono publicitario profesional. Máximo 200 caracteres. No se pondrá un enlace.

        Prompt del usuario: {prompt}

        Información relevante de la vacante:
        {vacante_info}
        """)
        return response.text.strip()[:200]
    except Exception as e:
        return f"Error al generar el message: {e}"

def generar_body_creative(prompt, vacante_info=""):
    try:
        response = model.generate_content(f"""
        Genera un cuerpo de anuncio para un creative de Meta que proporcione contexto adicional y motive a la acción.
        Usa un tono publicitario profesional. Máximo 500 caracteres. No se pondrá un enlace. Quiero que sea detallado, y trata de usar casi el límite de caracteres.

        Prompt del usuario: {prompt}
        
        Información relevante de la vacante:
        {vacante_info}
        """)
        return response.text.strip()[:500]
    except Exception as e:
        return f"Error al generar el body: {e}"
