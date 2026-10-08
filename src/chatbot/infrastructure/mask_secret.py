def mask_secret(value: str) -> str:
    if len(value) < 12:
        return "****"
    return "****" + value[-4:]
