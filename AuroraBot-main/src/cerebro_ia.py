"""
Cerebro de IA - Integración con OpenRouter
ARCHIVO ACTUALIZADO: Ahora usa OpenRouter en lugar de Gemini
"""
import os
import logging
from pathlib import Path

# Configurar logging
logger = logging.getLogger(__name__)

# Intentar importar las configuraciones
try:
    from config.openrouter_client import is_api_configured, get_client
    from config.settings import ASSISTANT_PROMPT
    OPENROUTER_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error importando configuración de OpenRouter: {e}")
    OPENROUTER_DISPONIBLE = False


def generar_respuesta(pregunta: str) -> str:
    """
    Genera una respuesta usando OpenRouter (DeepSeek)
    
    Args:
        pregunta: Pregunta o comando del usuario
        
    Returns:
        str: Respuesta generada por la IA
    """
    if not OPENROUTER_DISPONIBLE:
        return (
            "Error de configuración: No se pudo cargar OpenRouter. "
            "Verifica que el archivo config/openrouter_client.py existe."
        )
    
    if not is_api_configured():
        logger.warning("API de OpenRouter no configurada")
        return (
            "Lo siento, no puedo conectarme a OpenRouter en este momento. "
            "Verifica que hayas configurado OPENROUTER_API_KEY en el archivo .env\n\n"
            "Para obtener tu API key GRATIS:\n"
            "1. Ve a https://openrouter.ai/\n"
            "2. Haz login con GitHub\n"
            "3. Ve a 'Keys' y crea una nueva\n"
            "4. Cópiala en el archivo .env"
        )
    
    try:
        logger.info(f"Generando respuesta para: {pregunta[:50]}...")
        
        # Obtener cliente y generar respuesta
        client = get_client()
        respuesta = client.simple_chat(
            prompt=pregunta,
            system_prompt=ASSISTANT_PROMPT
        )
        
        if not respuesta:
            logger.warning("Respuesta vacía recibida")
            return "Lo siento, no pude generar una respuesta. ¿Podrías reformular tu pregunta?"
        
        logger.info("Respuesta generada exitosamente")
        
        # Limpiar asteriscos del markdown
        respuesta = respuesta.replace('*', '')
        
        return respuesta
        
    except Exception as e:
        logger.error(f"Error al generar respuesta: {e}")
        error_msg = str(e)
        
        # Mensajes de error más amigables
        if "API key" in error_msg or "401" in error_msg:
            return (
                "Error de autenticación con OpenRouter. "
                "Verifica que tu OPENROUTER_API_KEY en .env sea correcta."
            )
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            return (
                "Error de conexión. Verifica tu conexión a internet y que "
                "https://openrouter.ai esté accesible."
            )
        else:
            return f"Lo siento, ocurrió un error al procesar tu solicitud: {error_msg}"


def verificar_conexion() -> bool:
    """
    Verifica que la conexión con OpenRouter esté funcionando
    
    Returns:
        bool: True si la conexión es exitosa
    """
    if not OPENROUTER_DISPONIBLE:
        return False
    
    try:
        logger.info("Verificando conexión con OpenRouter...")
        respuesta = generar_respuesta("Di 'OK' si me escuchas")
        resultado = "ok" in respuesta.lower()
        
        if resultado:
            logger.info("✅ Conexión verificada correctamente")
        else:
            logger.warning("⚠️  Respuesta inesperada en verificación")
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en verificación de conexión: {e}")
        return False


def obtener_info_api() -> dict:
    """
    Obtiene información sobre la configuración de la API
    
    Returns:
        dict: Información de la API
    """
    if not OPENROUTER_DISPONIBLE:
        return {
            "provider": "OpenRouter",
            "disponible": False,
            "configurado": False,
            "conectado": False,
            "error": "Módulo OpenRouter no disponible"
        }
    
    try:
        if is_api_configured():
            client = get_client()
            info = client.get_model_info()
            info["conectado"] = True
            return info
        else:
            return {
                "provider": "OpenRouter",
                "disponible": True,
                "configurado": False,
                "conectado": False
            }
    except Exception as e:
        logger.error(f"Error al obtener info de API: {e}")
        return {
            "provider": "OpenRouter",
            "disponible": True,
            "configurado": False,
            "conectado": False,
            "error": str(e)
        }


# ============== COMPATIBILIDAD CON CÓDIGO VIEJO ==============
# Estas variables ya NO se usan, pero las dejamos por compatibilidad
API_KEY = None
model = None

print("✅ Cerebro de OpenRouter cargado correctamente (versión actualizada)")


# ============== TEST ==============
if __name__ == "__main__":
    # Configurar logging para el test
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print(" TEST DEL CEREBRO DE IA - OPENROUTER")
    print("=" * 60)
    
    # Test 1: Verificar configuración
    print("\n1️⃣  Verificando configuración...")
    info = obtener_info_api()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # Test 2: Verificar conexión
    print("\n2️⃣  Verificando conexión...")
    if verificar_conexion():
        print("   ✅ Conexión OK")
    else:
        print("   ❌ Conexión fallida")
        print("   💡 Verifica tu OPENROUTER_API_KEY en .env")
    
    # Test 3: Generar respuesta
    print("\n3️⃣  Generando respuesta de prueba...")
    pregunta = "Hola, ¿cómo estás?"
    print(f"   Pregunta: {pregunta}")
    respuesta = generar_respuesta(pregunta)
    print(f"   Respuesta: {respuesta[:100]}...")
    
    print("\n" + "=" * 60)
    print(" Tests completados")
    print("=" * 60)