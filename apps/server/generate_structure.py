from pathlib import Path

folders = [
    "app",
    "app/api",
    "app/core",
    "app/db",
    "app/models",
    "app/repositories",
    "app/schemas",
    "app/services",
    "app/utils",
    "app/workers",

    "app/modules",
    "app/modules/auth",
    "app/modules/coach",
    "app/modules/client",
    "app/modules/program",
    "app/modules/workout",
    "app/modules/nutrition",
    "app/modules/intelligence",
    "app/modules/ai",
]

for folder in folders:
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)

    init = path / "__init__.py"

    if not init.exists():
        init.touch()

main = Path("app/main.py")

main.write_text(
'''from fastapi import FastAPI

app = FastAPI(
    title="Fitness Intelligence Platform API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Fitness Intelligence Platform API"
    }
'''
)

print("Backend structure created successfully!")