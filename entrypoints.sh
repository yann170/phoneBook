
#!/bin/sh

echo "🚀 Initialisation de la base..."
python3 -m apps.config.init_db

echo "✔️ Base initialisée. Lancement de FastAPI."
exec fastapi run apps/main.py --port 81
