<div align="center">

# imgx

**Batch Image Processor — Resize, compress, convert in bulk**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-purple)](https://github.com/K2st0r/imgx)
[![Donate](https://img.shields.io/badge/Donate-USDT-red)](#donate)

</div>

### 🎯 One-liner

```bash
imgx photos/ -r 800x600 -o resized/
# → 142 images → 142 done. Saved 67.3% space.
```

### ✨ Features

| Feature | Description |
|---------|-------------|
| **Batch resize** | Process entire directories with one command |
| **Aspect ratio** | Specify width OR height, other dimension auto-calculates |
| **Quality control** | JPEG/WebP quality 1-100 |
| **Format convert** | PNG → JPG, BMP → WebP, anything → anything |
| **Compress only** | Keep dimensions, just optimize file size |
| **Progress bar** | Per-file progress with size reduction stats |
| **Remove originals** | `--rm` flag replaces source files inline |

### 🚀 Usage

```bash
# Batch resize entire folder
imgx photos/ -r 800x600 -o resized/

# Compress all JPGs to quality 60
imgx *.jpg -q 60 -o compressed/

# Convert PNG to WebP
imgx *.png -f webp -o webp/

# Resize by width (height auto)
imgx banner.jpg -w 1200 -o banners/

# Resize by height
imgx headshot.jpg --height 800 -o square/

# Replace originals with compressed versions
imgx photos/ -r 1920x1080 -q 80 --rm

# Process multiple folders
imgx folder1/ folder2/file1.png folder3/*.jpg -r 400x300 -o thumbs/
```

### 📊 Sample Output

```
imgx — Batch Image Processor
──────────────────────────────────────────────────
Found: 142 image(s)
Resize: 800x600
──────────────────────────────────────────────────

[1/142] + photo001.jpg         2048K ->  342K (-83.3%)  45ms
[2/142] + photo002.jpg         3156K ->  489K (-84.5%)  52ms
...
[142/142] + photo142.png       1024K ->  156K (-84.8%)  38ms

──────────────────────────────────────────────────
142 ok, 0 failed
Total: 198,456K -> 62,340K (saved 68.6%)
──────────────────────────────────────────────────
```

### 🎯 Use Cases

- **Photo cleanup** — Batch resize vacation photos before sharing
- **Web optimization** — Compress images before uploading to website
- **Format migration** — Convert legacy BMP/TIFF to modern WebP
- **Thumbnail generation** — Create thumbnails for gallery sites
- **E-commerce** — Standardize product image sizes

## 💎 Donate

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

---

*MIT License · Made with ❤️ by [K2st0r](https://github.com/K2st0r)*
