FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    fontconfig \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cairosvg Pillow fonttools pangocffi pangocairocffi

# Install variable fonts directly — Pango handles weight selection from the variable font
RUN mkdir -p /usr/local/share/fonts/chalkboard && \
    curl -fL -o /usr/local/share/fonts/chalkboard/JosefinSans.ttf \
        "https://github.com/google/fonts/raw/main/ofl/josefinsans/JosefinSans%5Bwght%5D.ttf" && \
    curl -fL -o /usr/local/share/fonts/chalkboard/Lora.ttf \
        "https://github.com/google/fonts/raw/main/ofl/lora/Lora%5Bwght%5D.ttf" && \
    fc-cache -f /usr/local/share/fonts/chalkboard

WORKDIR /work
ENTRYPOINT ["python", "render.py"]
