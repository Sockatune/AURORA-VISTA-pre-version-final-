"""
Habilidades Web - Navegación y búsquedas en internet
ARCHIVO COMPLETO CON TODAS LAS FUNCIONES
"""
import webbrowser
import logging
from config.settings import WEB_SHORTCUTS, USE_SELENIUM, FIREFOX_PROFILE_PATH

# Configurar logging
logger = logging.getLogger(__name__)

# Importaciones opcionales
SELENIUM_AVAILABLE = False
if USE_SELENIUM:
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        SELENIUM_AVAILABLE = True
        logger.info("✅ Selenium disponible")
    except ImportError:
        logger.warning("Selenium no disponible")

PYWHATKIT_AVAILABLE = False
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    logger.debug("PyWhatKit no disponible")

WIKIPEDIA_AVAILABLE = False
try:
    import wikipedia
    wikipedia.set_lang("es")
    WIKIPEDIA_AVAILABLE = True
    logger.info("✅ Biblioteca Wikipedia disponible (es)")
except ImportError:
    logger.debug("Biblioteca Wikipedia no disponible")


def abrir_busqueda_web(termino: str, motor: str = "google") -> str:
    """Abre una pestaña en el navegador con la búsqueda del término."""
    if not termino:
        return f"Dime qué quieres buscar en {motor}."
    
    if motor == "google":
        url = f"https://www.google.com/search?q={termino.replace(' ', '+')}"
        mensaje = f"Buscando '{termino}' en Google."
    elif motor == "youtube":
        url = f"https://www.youtube.com/results?search_query={termino.replace(' ', '+')}"
        mensaje = f"Buscando '{termino}' en YouTube."
    else:
        url = f"https://www.google.com/search?q={termino.replace(' ', '+')}"
        mensaje = f"Buscando '{termino}' en Google."

    try:
        webbrowser.open_new_tab(url)
        logger.info(f"Abriendo búsqueda en {motor}: {url}")
        return mensaje
    except Exception as e:
        logger.error(f"Error al abrir el navegador para {motor}: {e}")
        return f"No pude abrir el navegador para buscar en {motor}."


def buscar_en_google_directo(termino: str) -> str:
    """Función wrapper para mantener la consistencia en main.py."""
    return abrir_busqueda_web(termino, motor="google")


def buscar_en_youtube(termino: str, hablar=None) -> str:
    """
    Busca un video en YouTube y reproduce el primero (si pywhatkit está disponible).
    """
    if not termino:
        return "Por favor, dime qué quieres buscar en YouTube."
        
    if PYWHATKIT_AVAILABLE:
        try:
            logger.info(f"Reproduciendo en YouTube: {termino}")
            pywhatkit.playonyt(termino)
            return f"Buscando y reproduciendo '{termino}' en YouTube."
        except Exception as e:
            logger.error(f"Error al reproducir en YouTube con pywhatkit: {e}. Fallback a búsqueda web.")
    
    # Fallback a búsqueda web si pywhatkit no está disponible o falla
    return abrir_busqueda_web(termino, motor="youtube")


def resumir_wikipedia(termino: str) -> str:
    """
    Busca un artículo en Wikipedia, lee el contenido y genera un resumen.
    """
    if not termino:
        return "Por favor, dime qué quieres buscar en Wikipedia."

    if not WIKIPEDIA_AVAILABLE:
        url = f"https://es.wikipedia.org/wiki/Especial:Buscar?search={termino.replace(' ', '+')}"
        webbrowser.open_new_tab(url)
        return (f"La biblioteca de Wikipedia no está instalada. "
                f"Abrí la página de búsqueda para '{termino}' en el navegador. "
                f"(Instala con 'pip install wikipedia')")

    try:
        # 1. Buscar el artículo
        page_title = wikipedia.search(termino)
        if not page_title:
             return f"No encontré ningún artículo en Wikipedia para '{termino}'. Intenta ser más específico."
        
        # 2. Obtener el resumen (5 oraciones)
        resumen = wikipedia.summary(page_title[0], sentences=5)
        page = wikipedia.page(page_title[0], auto_suggest=False)
        
        # Formatear la respuesta
        respuesta = (
            f"Según Wikipedia sobre {page.title}:\n\n"
            f"{resumen}\n\n"
            f"(Fuente: {page.url})"
        )
        logger.info("Resumen de Wikipedia generado exitosamente.")
        return respuesta
        
    except wikipedia.exceptions.PageError:
        return f"Lo siento, no pude encontrar el artículo de Wikipedia para '{termino}'."
    except wikipedia.exceptions.DisambiguationError as e:
        opciones = ", ".join(e.options[:5])
        return f"Hay varias opciones para '{termino}'. ¿Podrías ser más específico? (Opciones: {opciones}...)"
    except Exception as e:
        logger.error(f"Error al resumir Wikipedia: {e}")
        return f"Ocurrió un error inesperado al intentar buscar en Wikipedia."


def iniciar_driver_firefox():
    """
    Inicializa un driver de Selenium para Firefox
    
    Returns:
        WebDriver: Instancia del driver o None si hay error
    """
    if not SELENIUM_AVAILABLE:
        logger.error("Selenium no está disponible")
        return None
    
    try:
        options = webdriver.FirefoxOptions()
        
        if FIREFOX_PROFILE_PATH and FIREFOX_PROFILE_PATH != "":
            options.add_argument("-profile")
            options.add_argument(FIREFOX_PROFILE_PATH)
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        logger.info("✅ Driver de Firefox inicializado")
        return driver
        
    except Exception as e:
        logger.error(f"Error al inicializar Firefox driver: {e}")
        return None


def abrir_pagina_web(comando):
    """
    Abre una página web predefinida según el comando
    
    Args:
        comando (str): Comando del usuario
        
    Returns:
        str: Mensaje de confirmación o vacío si no se encontró
    """
    # Buscar en los atajos predefinidos
    for nombre, url in WEB_SHORTCUTS.items():
        if nombre in comando.lower():
            return abrir_url(url, nombre)
    
    # Intentar detectar URLs en el comando
    if "http://" in comando or "https://" in comando:
        palabras = comando.split()
        for palabra in palabras:
            if palabra.startswith(("http://", "https://")):
                return abrir_url(palabra, "página web")
    
    return ""


def abrir_url(url, nombre="sitio web"):
    """
    Abre una URL usando el método disponible
    
    Args:
        url (str): URL a abrir
        nombre (str): Nombre descriptivo del sitio
        
    Returns:
        str: Mensaje de confirmación
    """
    try:
        # Método 1: Usar Selenium si está habilitado
        if USE_SELENIUM and SELENIUM_AVAILABLE:
            driver = iniciar_driver_firefox()
            if driver:
                driver.get(url)
                logger.info(f"Abriendo {nombre} con Firefox: {url}")
                return f"Abriendo {nombre} con Firefox."
        
        # Método 2: Usar webbrowser (por defecto)
        webbrowser.open(url)
        logger.info(f"Abriendo {nombre}: {url}")
        return f"Abriendo {nombre}."
        
    except Exception as e:
        logger.error(f"Error al abrir {nombre}: {e}")
        return f"No pude abrir {nombre}. Verifica tu navegador."


def buscar_en_google(comando):
    """
    Realiza una búsqueda en Google
    
    Args:
        comando (str): Comando del usuario
        
    Returns:
        str: Mensaje de confirmación o vacío si no es búsqueda
    """
    # Detectar palabras clave de búsqueda
    palabras_clave = ["busca", "buscar", "búsqueda", "googlea", "buscar en google"]
    
    for palabra in palabras_clave:
        if palabra in comando.lower():
            termino = extraer_termino_busqueda(comando, palabra)
            
            if termino:
                return realizar_busqueda(termino)
    
    return ""


def extraer_termino_busqueda(comando, palabra_clave):
    """
    Extrae el término de búsqueda del comando
    
    Args:
        comando (str): Comando completo
        palabra_clave (str): Palabra clave usada
        
    Returns:
        str: Término de búsqueda limpio
    """
    try:
        partes = comando.lower().split(palabra_clave, 1)
        
        if len(partes) > 1:
            termino = partes[1].strip()
            
            # Limpiar palabras comunes
            palabras_remover = ["en google", "por favor", "para mí"]
            for palabra in palabras_remover:
                termino = termino.replace(palabra, "").strip()
            
            return termino if termino else None
        
    except Exception as e:
        logger.error(f"Error al extraer término: {e}")
    
    return None


def realizar_busqueda(termino):
    """
    Ejecuta la búsqueda usando el método disponible
    
    Args:
        termino (str): Término a buscar
        
    Returns:
        str: Mensaje de confirmación
    """
    try:
        # Método 1: Usar pywhatkit si está disponible
        if PYWHATKIT_AVAILABLE:
            pywhatkit.search(termino)
            logger.info(f"Buscando con pywhatkit: {termino}")
            return f"Buscando '{termino}' en Google."
        
        # Método 2: Usar webbrowser
        url_busqueda = f"https://www.google.com/search?q={termino.replace(' ', '+')}"
        webbrowser.open(url_busqueda)
        logger.info(f"Buscando con webbrowser: {termino}")
        return f"Buscando '{termino}' en Google."
        
    except Exception as e:
        logger.error(f"Error al buscar: {e}")
        return f"No pude realizar la búsqueda de '{termino}'."


def listar_atajos_web():
    """
    Lista todos los atajos web disponibles
    
    Returns:
        dict: Diccionario de atajos
    """
    return WEB_SHORTCUTS.copy()


def listar_programas_disponibles():
    """
    Alias para listar_atajos_web (compatibilidad)
    
    Returns:
        dict: Diccionario de atajos
    """
    return listar_atajos_web()


# ============== TEST ==============
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🌐 TEST DE HABILIDADES WEB")
    print("=" * 60)
    
    # Test 1: Listar atajos
    print("\n1️⃣  Atajos web disponibles:")
    atajos = listar_atajos_web()
    for nombre, url in list(atajos.items())[:5]:
        print(f"   • {nombre} → {url}")
    print(f"   ... y {len(atajos) - 5} más")
    
    # Test 2: Probar detección de comandos
    print("\n2️⃣  Probando detección de comandos...")
    comandos_prueba = [
        "abre youtube",
        "abre google",
        "busca python tutorial",
        "buscar recetas de pasta"
    ]
    
    for cmd in comandos_prueba:
        # Probar abrir página
        resultado = abrir_pagina_web(cmd)
        if resultado:
            print(f"   '{cmd}' → {resultado}")
            continue
        
        # Probar búsqueda
        resultado = buscar_en_google(cmd)
        if resultado:
            print(f"   '{cmd}' → {resultado}")
        else:
            print(f"   '{cmd}' → No detectado")
    
    print("\n" + "=" * 60)
    print("Tests completados")
    print("=" * 60)