# habilidades_sistema.py - ARCHIVO COMPLETO ACTUALIZADO
import subprocess
import re
import logging
import shutil
import platform

logger = logging.getLogger(__name__)

# Detectar sistema operativo
SISTEMA_OPERATIVO = platform.system()

# Comandos según el sistema operativo
if SISTEMA_OPERATIVO == "Linux":
    COMANDOS = {
        "navegador": "firefox",
        "firefox": "firefox",
        "chrome": "google-chrome-stable",
        "chromium": "chromium-browser",
        "código": "code",
        "visual studio code": "code",
        "vscode": "code",
        "terminal": "gnome-terminal",
        "konsole": "konsole",
        "archivos": "nautilus",
        "dolphin": "dolphin",
        "calculadora": "gnome-calculator",
        "calendario": "gnome-calendar",
        "música": "rhythmbox",
        "videos": "totem",
        "texto": "gedit",
        "kate": "kate",
    }
elif SISTEMA_OPERATIVO == "Windows":
    COMANDOS = {
        "navegador": "start firefox",
        "firefox": "start firefox",
        "chrome": "start chrome",
        "edge": "start msedge",
        "código": "code",
        "visual studio code": "code",
        "vscode": "code",
        "terminal": "start cmd",
        "powershell": "start powershell",
        "archivos": "start explorer",
        "explorador": "start explorer",
        "calculadora": "calc",
        "notepad": "notepad",
        "bloc de notas": "notepad",
        "paint": "mspaint",
    }
elif SISTEMA_OPERATIVO == "Darwin":  # macOS
    COMANDOS = {
        "navegador": "open -a Firefox",
        "firefox": "open -a Firefox",
        "chrome": "open -a 'Google Chrome'",
        "safari": "open -a Safari",
        "código": "open -a 'Visual Studio Code'",
        "visual studio code": "open -a 'Visual Studio Code'",
        "vscode": "open -a 'Visual Studio Code'",
        "terminal": "open -a Terminal",
        "finder": "open -a Finder",
        "archivos": "open -a Finder",
        "calculadora": "open -a Calculator",
        "calendario": "open -a Calendar",
        "música": "open -a Music",
        "notas": "open -a Notes",
    }
else:
    COMANDOS = {}
    logger.warning(f"Sistema operativo no reconocido: {SISTEMA_OPERATIVO}")


def abrir_programa(comando, hablar=None, escuchar_confirmacion=None):
    """
    Abre un programa del sistema según el comando del usuario
    
    Args:
        comando: Texto del comando (ej: "abre firefox")
        hablar: Función para hablar (TTS) - opcional
        escuchar_confirmacion: Función para confirmar - opcional
    
    Returns:
        str: Mensaje de confirmación o vacío si no se encontró
    """
    try:
        # Extraer el nombre del programa
        app = comando.replace('abre', '').replace('abrir', '').replace('el', '').replace('la', '').strip()
        
        if not app:
            mensaje = "No entendí qué programa quieres abrir."
            if hablar:
                hablar(mensaje)
            return mensaje
        
        # Buscar en el diccionario de comandos
        ejecutable = None
        for nombre, cmd in COMANDOS.items():
            if nombre in app.lower():
                ejecutable = cmd
                nombre_app = nombre
                break
        
        if ejecutable:
            # Ejecutar el programa
            mensaje = f"Abriendo {nombre_app}."
            if hablar:
                hablar(mensaje)
            
            logger.info(f"Ejecutando: {ejecutable}")
            
            if SISTEMA_OPERATIVO == "Windows":
                subprocess.Popen(ejecutable, shell=True)
            else:
                subprocess.Popen(ejecutable.split())
            
            return mensaje
        else:
            # Programa no encontrado
            mensaje = f"Disculpa, no encontré el programa '{app}'."
            if hablar:
                hablar(mensaje)
                
                if escuchar_confirmacion:
                    hablar("¿Quieres que lo busque en Google?")
                    if escuchar_confirmacion():
                        import pywhatkit
                        hablar(f"Ok, buscando '{app}'.")
                        pywhatkit.search(app)
            
            return mensaje
            
    except FileNotFoundError:
        mensaje = f"No pude encontrar el programa. Verifica que esté instalado."
        logger.error(f"Ejecutable no encontrado: {ejecutable}")
        if hablar:
            hablar(mensaje)
        return mensaje
    except PermissionError:
        mensaje = f"No tengo permisos para abrir ese programa."
        logger.error(f"Sin permisos para ejecutar: {ejecutable}")
        if hablar:
            hablar(mensaje)
        return mensaje
    except Exception as e:
        mensaje = f"Ocurrió un error al intentar abrir el programa."
        logger.error(f"Error al abrir programa: {e}")
        if hablar:
            hablar(mensaje)
        return mensaje


def ajustar_volumen(comando, hablar=None):
    """
    Ajusta el volumen del sistema (solo Linux con amixer)
    
    Args:
        comando: Texto del comando (ej: "volumen a 50")
        hablar: Función para hablar (TTS) - opcional
    """
    try:
        match = re.search(r'(\d+)', comando)
        
        if not match:
            mensaje = "No entendí a qué porcentaje ajustar el volumen."
            if hablar:
                hablar(mensaje)
            return
        
        porcentaje = match.group(1)
        mensaje = f"Ajustando volumen al {porcentaje} por ciento."
        
        if hablar:
            hablar(mensaje)
        
        if SISTEMA_OPERATIVO == "Linux":
            subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', f'{porcentaje}%'])
            logger.info(f"Volumen ajustado a {porcentaje}%")
        else:
            if hablar:
                hablar("Esta función solo está disponible en Linux.")
                
    except Exception as e:
        logger.error(f"Error al ajustar volumen: {e}")
        if hablar:
            hablar("No pude ajustar el volumen.")


def vaciar_papelera(hablar=None, escuchar_confirmacion=None):
    """
    Vacía la papelera del sistema (solo Linux)
    
    Args:
        hablar: Función para hablar (TTS) - opcional
        escuchar_confirmacion: Función para confirmar - opcional
    """
    try:
        if hablar:
            hablar("¿Estás totalmente seguro de que quieres vaciar la papelera? Esta acción es irreversible.")
        
        if escuchar_confirmacion and escuchar_confirmacion():
            if hablar:
                hablar("Vaciando la papelera.")
            
            if SISTEMA_OPERATIVO == "Linux":
                subprocess.run(['trash-empty'])
                logger.info("Papelera vaciada")
            else:
                if hablar:
                    hablar("Esta función solo está disponible en Linux.")
        else:
            if hablar:
                hablar("De acuerdo, acción cancelada.")
                
    except Exception as e:
        logger.error(f"Error al vaciar papelera: {e}")
        if hablar:
            hablar("No pude vaciar la papelera.")


def mover_a_papelera(comando, hablar=None, escuchar_confirmacion=None):
    """
    Mueve un archivo a la papelera (solo Linux)
    
    Args:
        comando: Texto del comando (ej: "borra el archivo test.txt")
        hablar: Función para hablar (TTS) - opcional
        escuchar_confirmacion: Función para confirmar - opcional
    """
    try:
        archivo = comando.replace('borra el archivo', '').replace('borrar el archivo', '').strip()
        
        if hablar:
            hablar(f"Esta acción enviará '{archivo}' a la papelera. ¿Estás seguro?")
        
        if escuchar_confirmacion and escuchar_confirmacion():
            if SISTEMA_OPERATIVO == "Linux":
                subprocess.run(['trash-put', archivo], check=True)
                mensaje = f"Hecho. '{archivo}' está en la papelera."
                logger.info(f"Archivo movido a papelera: {archivo}")
            else:
                mensaje = "Esta función solo está disponible en Linux."
            
            if hablar:
                hablar(mensaje)
        else:
            if hablar:
                hablar("Acción cancelada.")
                
    except FileNotFoundError:
        mensaje = f"No pude encontrar el archivo '{archivo}'."
        logger.error(f"Archivo no encontrado: {archivo}")
        if hablar:
            hablar(mensaje)
    except Exception as e:
        logger.error(f"Error al mover archivo: {e}")
        if hablar:
            hablar("No pude mover el archivo a la papelera.")


def buscar_archivo(comando, hablar=None):
    """
    Busca un archivo en el sistema (solo Linux con kfind)
    
    Args:
        comando: Texto del comando (ej: "busca el archivo documento.pdf")
        hablar: Función para hablar (TTS) - opcional
    """
    try:
        archivo = comando.replace('busca el archivo', '').replace('buscar el archivo', '').strip()
        
        if hablar:
            hablar(f"Buscando '{archivo}' en tu sistema. Esto puede tardar un momento.")
        
        if SISTEMA_OPERATIVO == "Linux":
            subprocess.Popen(['kfind', '--search', archivo])
            logger.info(f"Buscando archivo: {archivo}")
        else:
            if hablar:
                hablar("Esta función solo está disponible en Linux con KDE.")
                
    except Exception as e:
        logger.error(f"Error al buscar archivo: {e}")
        if hablar:
            hablar("No pude iniciar la búsqueda.")


def listar_programas_disponibles():
    """
    Lista todos los programas disponibles según el sistema operativo
    
    Returns:
        dict: Diccionario de programas disponibles
    """
    return COMANDOS.copy()


print(f"✅ Habilidades Sistema cargadas correctamente ({SISTEMA_OPERATIVO})")