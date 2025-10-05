def cache_headers(seconds: int = 30):
    return {"Cache-Control": f"public, max-age={seconds}"}
