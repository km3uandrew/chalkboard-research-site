FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libcairo2 \
    fontconfig \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cairosvg Pillow fonttools

# Install variable fonts, plus a static Jost wght-600 instance ("Jost W600") for
# the wordmark — cairo's toy font API can only reach Regular or Bold from a
# variable font, so intermediate weights must be baked at build time.
COPY instance_fonts.py /tmp/instance_fonts.py
RUN mkdir -p /usr/local/share/fonts/chalkboard && \
    curl -fL -o /tmp/Jost.ttf \
        "https://github.com/google/fonts/raw/main/ofl/jost/Jost%5Bwght%5D.ttf" && \
    curl -fL -o /usr/local/share/fonts/chalkboard/Lora.ttf \
        "https://github.com/google/fonts/raw/main/ofl/lora/Lora%5Bwght%5D.ttf" && \
    cp /tmp/Jost.ttf /usr/local/share/fonts/chalkboard/Jost.ttf && \
    python /tmp/instance_fonts.py && \
    fc-cache -f /usr/local/share/fonts/chalkboard

WORKDIR /work
ENTRYPOINT ["python", "render.py"]
