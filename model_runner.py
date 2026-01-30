# model_runner.py
import subprocess

MODEL_NAME = "qwen2.5:3b-instruct"
OLLAMA_PATH = r"C:\Users\HP\AppData\Local\Programs\Ollama\ollama.exe"  # full path to ollama.exe

def ask_model(prompt: str) -> str:
    """
    Sends prompt to local Qwen via Ollama CLI
    Returns plain text answer
    """
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running model: {e.stderr}"
    except FileNotFoundError:
        return f"Error: Ollama executable not found at {OLLAMA_PATH}"
