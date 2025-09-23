def chunk_code(code: str, max_lines: int = 100):
    """Split code into manageable chunks by lines."""
    lines = code.splitlines()
    for i in range(0, len(lines), max_lines):
        yield "\n".join(lines[i:i+max_lines])