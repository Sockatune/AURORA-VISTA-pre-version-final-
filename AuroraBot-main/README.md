# 🌌 Aurora - Asistente de IA

Aurora es un asistente de voz y escritorio con una interfaz futurista (PySide6) y un cerebro impulsado por modelos de lenguaje grande (LLMs) a través de la API de [OpenRouter](https://openrouter.ai/).  
Está diseñado para ofrecer una experiencia fluida, visualmente moderna y con integración completa entre voz, interfaz y web.

---

## 🚀 Características Principales

- 🎙️ **Modo Voz Continuo:** Activación por comando de voz con escucha automática.  
- 💫 **Widget Flotante (Burbuja):** Ícono persistente en pantalla para activación rápida (hilo independiente con QThread).  
- 🌐 **Habilidades Web:** Puede buscar directamente en Google, YouTube o Wikipedia sin usar la API de IA cuando sea innecesario.  
- 🔊 **TTS No Bloqueante:** Usa gTTS en un hilo separado, permitiendo que Aurora hable sin congelar la interfaz.  
- ⚙️ **Configuración Externa:** Usa `.env` para claves API, idioma, voz y otros ajustes.  

---

## ⚙️ Requisitos y Dependencias

### 🐍 Requisitos de Python

- Python 3.9 o superior

Instala todas las dependencias principales:

```bash
pip install PySide6 SpeechRecognition gTTS pywhatkit wikipedia python-dotenv
```

---

### 🎤 Dependencias del Sistema (para Voz)

**SpeechRecognition** depende de **PyAudio** para capturar audio.  
Antes de instalarlo, asegúrate de tener los paquetes del sistema:

| Sistema Operativo | Comando de Pre-requisito |
|------------------|--------------------------|
| 🐧 Linux (Debian/Ubuntu) | `sudo apt-get install portaudio19-dev python3-dev` |
| 🍎 macOS (Homebrew) | `brew install portaudio` |
| 🪟 Windows | Generalmente no requiere pasos adicionales |

Luego instala PyAudio:

```bash
pip install PyAudio
```

---

## 🧠 Configuración Obligatoria

Para que Aurora use su “cerebro” (OpenRouter/Gemini), debes configurar la clave API.

### 1️⃣ Obtener tu Clave API

Crea una en [OpenRouter Keys](https://openrouter.ai/keys) y cópiala.

### 2️⃣ Configurar el Archivo `.env`

Copia el archivo `example.env` (o `config/.env.example`) y renómbralo a `.env`.  
Luego edítalo y agrega tu clave:

```env
# Clave de API OBLIGATORIA
OPENROUTER_API_KEY="PEGA_TU_CLAVE_DE_OPENROUTER_AQUI"

# Configuraciones opcionales
VOICE_LANG="es-ES"
LOG_LEVEL="INFO"
```

⚠️ **Advertencia:**  
Si la clave está ausente o expirada, Aurora mostrará el error `400 API key expired` en los logs y no podrá responder mediante IA.

---

## ▶️ Ejecución

### 💻 Interfaz Gráfica (Recomendada)

```bash
python3 interfaz.py
```

### 💬 Modos Alternativos

```bash
# Modo terminal (sin interfaz)
python3 main.py --terminal

# Test de micrófono, voz y procesamiento
python3 main.py --test
```

---

## 🧩 Estructura del Proyecto

| Archivo / Módulo | Función |
|------------------|----------|
| `main.py` | Motor principal. Contiene `procesar_comando` y la lógica del TTS no bloqueante. |
| `interfaz.py` | Interfaz principal (PySide6). Define `AuroraWindow` y el hilo de voz (`VoiceWorker`). |
| `floating_assistant.py` | Burbuja flotante. Maneja activación rápida y escucha continua (`ListenWorker`). |
| `cerebro_ia.py` | Módulo de IA. Se conecta con OpenRouter/Gemini y procesa respuestas. |
| `habilidades_web.py` | Incluye funciones como `buscar_en_google_directo`, `buscar_en_youtube`, `resumir_wikipedia`. |
| `.env` | Configuración de claves y variables del asistente. |

---

## ⚡ Integraciones Adicionales

### Instalar dependencias extra para automatización web:

```bash
pip install selenium webdriver-manager
```

### Agregar programas personalizados

Edita `config/settings.py` en la sección:
```python
PROGRAMAS_CONFIG = {
    "navegador": "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "spotify": "C:\Users\TuUsuario\AppData\Roaming\Spotify\Spotify.exe",
}
```

### Agregar atajos web personalizados

Edita `config/settings.py` en la sección:
```python
WEB_SHORTCUTS = {
    "youtube": "https://youtube.com",
    "github": "https://github.com",
}
```

---

## 🐛 Solución de Problemas

### 🔈 PyAudio no se instala

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

---

### 🎧 Error “No se encontró reproductor de audio” (Linux)

```bash
sudo apt-get install mpg123 ffmpeg vlc
```

---

### 🎤 Error con el micrófono

1. Verifica que el micrófono esté conectado.  
2. Comprueba los permisos de audio.  
3. En Linux, ejecuta:  
   ```bash
   sudo usermod -a -G audio $USER
   ```

---

### 🤖 La IA no responde

1. Revisa tu `OPENROUTER_API_KEY` en `.env`.  
2. Comprueba tu conexión a Internet.  
3. Mira los logs en `logs/aura.log`.

---

## 🔧 Desarrollo

### Ejecutar tests

```bash
python run.py --test
```

### Ver logs

```bash
tail -f logs/aura.log
```

### Activar modo debug

```bash
# En .env
LOG_LEVEL=DEBUG
```

---

## 📝 Licencia

Este proyecto está bajo la **Licencia MIT**.  
Puedes usarlo, modificarlo y distribuirlo libremente dando el crédito correspondiente.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! 💡

1. Haz un **fork** del repositorio.  
2. Crea una rama para tu feature:  
   ```bash
   git checkout -b feature/MiFeature
   ```
3. Realiza tus commits:  
   ```bash
   git commit -m "Agrega nueva función"
   ```
4. Envía tus cambios:  
   ```bash
   git push origin feature/MiFeature
   ```
5. Abre un **Pull Request** 🚀

---

## 📧 Contacto

Si tienes dudas, sugerencias o ideas:  
Abre un **Issue** en GitHub o contacta al desarrollador.

---

## 🙏 Agradecimientos

- [OpenRouter](https://openrouter.ai/) — API universal para modelos de IA  
- [DeepSeek](https://www.deepseek.com/) — Modelo de IA eficiente y económico  
- [PySide6](https://www.qt.io/qt-for-python) — Framework de interfaz gráfica  
- [gTTS](https://github.com/pndurette/gTTS) — Síntesis de voz natural  
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) — Reconocimiento de voz humano  

---

⭐ **Si te gusta Aurora, dale una estrella en GitHub y apoya el proyecto.**
