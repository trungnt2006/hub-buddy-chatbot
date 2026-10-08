from dataclasses import dataclass

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OPENAI_TEMPERATURE = 0.3
DEFAULT_OPENAI_TIMEOUT = 30
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 2610
DEFAULT_MEMORY_FILE = "memory.json"
DEFAULT_MAX_MESSAGES = 5
DEFAULT_SYSTEM_PROMPT_FILE = "system-prompt.txt"


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = ""
    openai_model: str = DEFAULT_OPENAI_MODEL
    openai_temperature: float = DEFAULT_OPENAI_TEMPERATURE
    openai_timeout: int = DEFAULT_OPENAI_TIMEOUT
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    memory_file: str = DEFAULT_MEMORY_FILE
    max_messages: int = DEFAULT_MAX_MESSAGES
    system_prompt_file: str = DEFAULT_SYSTEM_PROMPT_FILE
