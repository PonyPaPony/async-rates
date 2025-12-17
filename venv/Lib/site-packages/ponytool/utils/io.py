def ask_confirm(text: str) -> bool:
    answer = input(f"{text} (y/n): ").strip().lower()
    return answer == 'y'

def ask_input(prompt: str, default: str | None = None) -> str:
    value = input(f"{prompt}: ").strip()
    return value if value else default
