# Timeline lišta

Nástroj pro showcase videa: nahraješ video projektu, nastavíš segmenty a kapitoly a stáhneš hotové video s animovanou timeline lištou v Liquid Glass stylu. Nebo vyexportuješ jen samotnou lištu (green screen / průhledné WebM) do střihu.

## Spuštění

```
python serve.py
```

a otevři http://127.0.0.1:8765/index.html. Server podporuje HTTP Range, což prohlížeč potřebuje pro přehrávání a scrubování videa (`python -m http.server` to neumí).

## Demo

`demo.mp4` je 9s smyčka z Big Buck Bunny (Blender Foundation, CC BY 3.0), přehrává se na pozadí, dokud nenahraješ vlastní video.
