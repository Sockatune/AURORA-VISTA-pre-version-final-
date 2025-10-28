"""
Habilidades Sistema - Control de aplicaciones multiplataforma
VERSIÓN MEJORADA: Detecta automáticamente TODOS los programas instalados
"""
import subprocess
import re
import logging
import shutil
import platform
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Detectar sistema operativo
SISTEMA_OPERATIVO = platform.system()

# Comandos predefinidos (los más comunes)
COMANDOS_BASE = {
    "Linux": {
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
        "spotify": "spotify",
        "discord": "discord",
        "telegram": "telegram-desktop",
        "vlc": "vlc",
        "gimp": "gimp",
        "inkscape": "inkscape",
        "libreoffice": "libreoffice",
        "writer": "libreoffice --writer",
        "calc": "libreoffice --calc",
        "impress": "libreoffice --impress",
    },
    "Windows": {
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
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "outlook": "start outlook",
    },
    "Darwin": {  # macOS
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
}

# Cache de programas detectados
_programas_cache = None


def detectar_programas_instalados():
    """
    Detecta TODOS los programas instalados en el sistema
    
    Returns:
        dict: Diccionario con programas detectados {nombre: comando}
    """
    global _programas_cache
    
    # Si ya se detectaron antes, usar cache
    if _programas_cache is not None:
        return _programas_cache
    
    logger.info(f"🔍 Detectando programas instalados en {SISTEMA_OPERATIVO}...")
    programas = {}
    
    # Empezar con los comandos base
    if SISTEMA_OPERATIVO in COMANDOS_BASE:
        programas.update(COMANDOS_BASE[SISTEMA_OPERATIVO])
    
    # Detectar programas adicionales según el sistema
    if SISTEMA_OPERATIVO == "Linux":
        programas.update(detectar_programas_linux())
    elif SISTEMA_OPERATIVO == "Windows":
        programas.update(detectar_programas_windows())
    elif SISTEMA_OPERATIVO == "Darwin":
        programas.update(detectar_programas_macos())
    
    _programas_cache = programas
    logger.info(f"✅ Detectados {len(programas)} programas")
    
    return programas


def detectar_programas_linux():
    """
    Detecta programas instalados en Linux
    
    Returns:
        dict: Programas detectados
    """
    programas = {}
    
    # 1. Buscar en /usr/share/applications/ (archivos .desktop)
    desktop_dirs = [
        Path("/usr/share/applications"),
        Path.home() / ".local/share/applications",
    ]
    
    for desktop_dir in desktop_dirs:
        if not desktop_dir.exists():
            continue
        
        for desktop_file in desktop_dir.glob("*.desktop"):
            try:
                with open(desktop_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer Name y Exec
                name_match = re.search(r'^Name=(.+)$', content, re.MULTILINE)
                exec_match = re.search(r'^Exec=(.+)$', content, re.MULTILINE)
                
                if name_match and exec_match:
                    name = name_match.group(1).strip().lower()
                    exec_cmd = exec_match.group(1).strip()
                    
                    # Limpiar el comando (quitar %U, %F, etc)
                    exec_cmd = re.sub(r'\s+%[UuFf].*$', '', exec_cmd)
                    
                    # Agregar solo si no está ya
                    if name not in programas:
                        programas[name] = exec_cmd
                        
            except Exception as e:
                logger.debug(f"Error leyendo {desktop_file}: {e}")
    
    # 2. Buscar programas comunes en PATH
    programas_comunes = [
        "gimp", "inkscape", "blender", "audacity", "obs", "obs-studio",
        "steam", "lutris", "discord", "telegram-desktop", "slack",
        "zoom", "skype", "vlc", "mpv", "rhythmbox", "clementine",
        "thunderbird", "evolution", "geary", "darktable", "kdenlive",
        "shotcut", "handbrake", "transmission", "qbittorrent", "deluge",
        "wine", "bottles", "krita", "mypaint", "scribus", "calibre",
    ]
    
    for prog in programas_comunes:
        if shutil.which(prog) and prog not in programas:
            programas[prog] = prog
    
    return programas


def detectar_programas_windows():
    """
    Detecta programas instalados en Windows
    
    Returns:
        dict: Programas detectados
    """
    programas = {}
    
    # Buscar en rutas comunes de instalación
    program_dirs = [
        Path("C:/Program Files"),
        Path("C:/Program Files (x86)"),
        Path.home() / "AppData/Local/Programs",
    ]
    
    for prog_dir in program_dirs:
        if not prog_dir.exists():
            continue
        
        try:
            for app_dir in prog_dir.iterdir():
                if not app_dir.is_dir():
                    continue
                
                # Buscar ejecutables .exe
                exe_files = list(app_dir.glob("*.exe"))
                if exe_files:
                    exe = exe_files[0]
                    name = exe.stem.lower()
                    programas[name] = f'start "" "{exe}"'
                    
        except PermissionError:
            continue
        except Exception as e:
            logger.debug(f"Error buscando en {prog_dir}: {e}")
    
    return programas


def detectar_programas_macos():
    """
    Detecta programas instalados en macOS
    
    Returns:
        dict: Programas detectados
    """
    programas = {}
    
    # Buscar en /Applications
    apps_dir = Path("/Applications")
    
    if apps_dir.exists():
        try:
            for app in apps_dir.glob("*.app"):
                name = app.stem.lower()
                programas[name] = f'open -a "{app.stem}"'
                
        except Exception as e:
            logger.debug(f"Error buscando aplicaciones: {e}")
    
    return programas


def buscar_programa_por_nombre(nombre_busqueda):
    """
    Busca un programa por su nombre (búsqueda flexible)
    
    Args:
        nombre_busqueda: Nombre del programa a buscar
        
    Returns:
        tuple: (nombre_encontrado, comando) o (None, None) si no se encuentra
    """
    programas = detectar_programas_instalados()
    nombre_busqueda = nombre_busqueda.lower().strip()
    
    # 1. Búsqueda exacta
    if nombre_busqueda in programas:
        return nombre_busqueda, programas[nombre_busqueda]
    
    # 2. Búsqueda que contenga el nombre
    for nombre, comando in programas.items():
        if nombre_busqueda in nombre or nombre in nombre_busqueda:
            return nombre, comando
    
    # 3. Búsqueda por palabras clave
    palabras = nombre_busqueda.split()
    for palabra in palabras:
        if len(palabra) < 3:  # Ignorar palabras muy cortas
            continue
        
        for nombre, comando in programas.items():
            if palabra in nombre:
                return nombre, comando
    
    return None, None


def abrir_programa(comando, hablar=None, escuchar_confirmacion=None):
    """
    Abre un programa del sistema según el comando del usuario
    VERSIÓN MEJORADA: Busca dinámicamente en todos los programas
    
    Args:
        comando: Texto del comando (ej: "abre firefox")
        hablar: Función para hablar (TTS) - opcional
        escuchar_confirmacion: Función para confirmar - opcional
    
    Returns:
        str: Mensaje de confirmación o vacío si no se encontró
    """
    try:
        # Extraer el nombre del programa
        nombre_app = comando.replace('abre', '').replace('abrir', '').strip()
        nombre_app = nombre_app.replace('el', '').replace('la', '').replace('los', '').replace('las', '').strip()
        
        if not nombre_app:
            mensaje = "No entendí qué programa quieres abrir."
            if hablar:
                hablar(mensaje)
            return mensaje
        
        logger.info(f"🔍 Buscando programa: '{nombre_app}'")
        
        # Buscar el programa
        nombre_encontrado, ejecutable = buscar_programa_por_nombre(nombre_app)
        
        if ejecutable:
            # Ejecutar el programa
            mensaje = f"Abriendo {nombre_encontrado}."
            if hablar:
                hablar(mensaje)
            
            logger.info(f"▶️  Ejecutando: {ejecutable}")
            
            try:
                if SISTEMA_OPERATIVO == "Windows":
                    subprocess.Popen(ejecutable, shell=True)
                elif SISTEMA_OPERATIVO == "Darwin":
                    subprocess.Popen(ejecutable, shell=True)
                else:  # Linux
                    # Separar el comando y sus argumentos
                    cmd_parts = ejecutable.split()
                    subprocess.Popen(cmd_parts)
                
                return mensaje
                
            except Exception as e:
                logger.error(f"Error al ejecutar {ejecutable}: {e}")
                return f"Error al abrir {nombre_encontrado}."
        else:
            # Programa no encontrado
            mensaje = f"No encontré el programa '{nombre_app}' instalado."
            logger.warning(f"❌ Programa no encontrado: {nombre_app}")
            
            if hablar:
                hablar(mensaje)
                
                # Ofrecer buscar en Google
                if escuchar_confirmacion:
                    if hablar:
                        hablar("¿Quieres que lo busque en Google?")
                    
                    if escuchar_confirmacion():
                        try:
                            import pywhatkit
                            if hablar:
                                hablar(f"Ok, buscando '{nombre_app}'.")
                            pywhatkit.search(nombre_app)
                        except ImportError:
                            import webbrowser
                            webbrowser.open(f"https://www.google.com/search?q={nombre_app}")
            
            return mensaje
            
    except Exception as e:
        mensaje = f"Ocurrió un error al intentar abrir el programa."
        logger.error(f"Error en abrir_programa: {e}")
        if hablar:
            hablar(mensaje)
        return mensaje


def listar_programas_disponibles():
    """
    Lista todos los programas disponibles detectados
    
    Returns:
        dict: Diccionario de programas disponibles
    """
    return detectar_programas_instalados()


def actualizar_cache_programas():
    """
    Fuerza la actualización del cache de programas
    (útil si se instala un programa nuevo)
    """
    global _programas_cache
    _programas_cache = None
    return detectar_programas_instalados()


# ============== FUNCIONES DE SISTEMA ADICIONALES ==============

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


# Detectar programas al cargar el módulo
logger.info("🚀 Iniciando detección de programas...")
try:
    num_programas = len(detectar_programas_instalados())
    print(f"✅ Habilidades Sistema cargadas ({SISTEMA_OPERATIVO}) - {num_programas} programas detectados")
except Exception as e:
    logger.error(f"Error al detectar programas: {e}")
    print(f"⚠️  Habilidades Sistema cargadas ({SISTEMA_OPERATIVO}) - Detección parcial")


# ============== TEST ==============
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🖥️  TEST DE DETECCIÓN DE PROGRAMAS")
    print("=" * 60)
    
    # Test 1: Detectar programas
    print("\n1️⃣  Detectando programas instalados...")
    programas = detectar_programas_instalados()
    print(f"   ✅ Detectados {len(programas)} programas")
    
    # Mostrar algunos ejemplos
    print("\n📋 Ejemplos de programas detectados:")
    for i, (nombre, comando) in enumerate(list(programas.items())[:10]):
        print(f"   {i+1}. {nombre} → {comando}")
    
    if len(programas) > 10:
        print(f"   ... y {len(programas) - 10} más")
    
    # Test 2: Búsqueda de programas
    print("\n2️⃣  Probando búsqueda de programas...")
    pruebas = ["firefox", "chrome", "código", "calculadora", "telegram"]
    
    for prueba in pruebas:
        nombre, cmd = buscar_programa_por_nombre(prueba)
        if nombre:
            print(f"   ✅ '{prueba}' → {nombre} ({cmd})")
        else:
            print(f"   ❌ '{prueba}' → No encontrado")
    
    print("\n" + "=" * 60)
    print("Tests completados")
    print("=" * 60)