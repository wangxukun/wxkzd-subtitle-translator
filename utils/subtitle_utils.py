def load_srt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_srt(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
