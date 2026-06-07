#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
imgx — Batch Image Processor
========================================
Resize, compress, convert images in bulk. One command.

Usage:
  imgx photos/ -r 800x600 -o resized/       # Batch resize
  imgx *.png -q 75 -o compressed/           # Batch compress
  imgx logo.jpg -f png -o converted/ --rm   # Convert format
  imgx images/ -w 1200 -o thumbs/           # Resize by width

Install:
  pip install pillow

License: MIT
Donate:  0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697 (USDT ERC20)
"""
import argparse, os, sys, time, glob
from typing import Optional, Tuple, List

# Fix encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk','cp936','cp1252'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

__version__ = "1.0.0"
__wallet__  = "0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697"

try:
    from PIL import Image
except ImportError:
    sys.exit("imgx requires Pillow. Install: pip install pillow")

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}

def find_images(paths: List[str]) -> List[str]:
    files = []
    for p in paths:
        if os.path.isfile(p):
            if os.path.splitext(p)[1].lower() in SUPPORTED_EXT:
                files.append(p)
        elif os.path.isdir(p):
            for root, _, fnames in os.walk(p):
                for f in fnames:
                    if os.path.splitext(f)[1].lower() in SUPPORTED_EXT:
                        files.append(os.path.join(root, f))
    return sorted(set(files))

def parse_size(s: str) -> Optional[Tuple[int, int]]:
    """Parse '800x600' or '800'."""
    if s.lower() == "none":
        return None
    parts = s.split("x")
    w = int(parts[0]) if parts[0] else None
    h = int(parts[1]) if len(parts) > 1 and parts[1] else None
    if w is None and h is None:
        return None
    return (w, h)

def process_image(src: str, dst: str, size: Optional[Tuple[int, int]],
                  width: Optional[int], height: Optional[int],
                  quality: int, fmt: Optional[str]) -> Tuple[int, int, float]:
    """Process one image. Returns (orig_size, new_size, elapsed)."""
    t0 = time.perf_counter()
    orig_size = os.path.getsize(src)
    
    with Image.open(src) as img:
        # Convert RGBA to RGB for JPEG output
        if fmt in ("jpg", "jpeg") and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Resize
        orig_w, orig_h = img.size
        if size:
            w, h = size
            if w and h:
                img = img.resize((w, h), Image.LANCZOS)
            elif w:
                ratio = w / orig_w
                img = img.resize((w, int(orig_h * ratio)), Image.LANCZOS)
            elif h:
                ratio = h / orig_h
                img = img.resize((int(orig_w * ratio), h), Image.LANCZOS)
        elif width:
            ratio = width / orig_w
            img = img.resize((width, int(orig_h * ratio)), Image.LANCZOS)
        elif height:
            ratio = height / orig_h
            img = img.resize((int(orig_w * ratio), height), Image.LANCZOS)
        
        # Format conversion
        save_fmt = fmt
        if save_fmt is None:
            ext = os.path.splitext(dst)[1].lower().lstrip(".")
            save_fmt = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "gif": "GIF",
                        "bmp": "BMP", "webp": "WEBP", "tiff": "TIFF"}.get(ext, "JPEG")
        else:
            save_fmt = save_fmt.upper()
        
        save_kwargs = {}
        if save_fmt == "JPEG":
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True
            dst = os.path.splitext(dst)[0] + ".jpg"
        elif save_fmt == "PNG":
            save_kwargs["optimize"] = True
            dst = os.path.splitext(dst)[0] + ".png"
        elif save_fmt == "WEBP":
            save_kwargs["quality"] = quality
        
        os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
        img.save(dst, save_fmt, **save_kwargs)
    
    new_size = os.path.getsize(dst)
    elapsed = (time.perf_counter() - t0) * 1000
    return orig_size, new_size, elapsed

def main():
    parser = argparse.ArgumentParser(
        prog="imgx",
        description="Batch image processor — resize, compress, convert",
        epilog="Examples:\n  imgx photos/ -r 800x600 -o resized/\n  imgx *.png -q 75 -o compressed/",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", nargs="+", help="Image files or directories")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current)")
    parser.add_argument("-r", "--resize", help="Target size: WxH or W or xH (e.g. 800x600)")
    parser.add_argument("-w", "--width", type=int, help="Target width (preserve aspect)")
    parser.add_argument("--height", type=int, help="Target height (preserve aspect)")
    parser.add_argument("-q", "--quality", type=int, default=85, help="JPEG/WebP quality 1-100 (default: 85)")
    parser.add_argument("-f", "--format", choices=["jpg","png","webp","gif","bmp"], help="Convert to format")
    parser.add_argument("--rm", "--remove", dest="remove", action="store_true", help="Replace original files")
    parser.add_argument("--version", action="version", version=f"imgx {__version__}")
    
    args = parser.parse_args()
    files = find_images(args.input)
    
    if not files:
        print("No image files found.")
        return
    
    print(f"\n  imgx — Batch Image Processor")
    print(f"  {'─' * 50}")
    print(f"  Found: {len(files)} image(s)")
    if args.resize: print(f"  Resize: {args.resize}")
    if args.width: print(f"  Width: {args.width}")
    if args.format: print(f"  Format: {args.format}")
    print(f"  {'─' * 50}\n")
    
    total_orig = 0
    total_new = 0
    ok = fail = 0
    
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        rel = os.path.splitext(name)[0]
        ext = f".{args.format}" if args.format else os.path.splitext(name)[1]
        dst = os.path.join(args.output, rel + ext) if not args.remove else f
        
        size = parse_size(args.resize) if args.resize else None
        
        try:
            orig, new, elapsed = process_image(
                f, dst, size, args.width, args.height,
                args.quality, args.format
            )
            reduction = (1 - new / orig) * 100 if orig > 0 else 0
            icon = "✓" if reduction >= 0 else "✗"
            print(f"  [{i}/{len(files)}] {icon} {name:<30} {orig/1024:>6.0f}K -> {new/1024:>6.0f}K "
                  f"({reduction:>+5.1f}%) {elapsed:>5.0f}ms")
            total_orig += orig
            total_new += new
            ok += 1
        except Exception as e:
            print(f"  [{i}/{len(files)}] ✗ {name:<30} ERROR: {e}")
            fail += 1
    
    print(f"\n  {'─' * 50}")
    total_red = (1 - total_new / total_orig) * 100 if total_orig > 0 else 0
    print(f"  {ok} ok, {fail} failed")
    print(f"  Total: {total_orig/1024:,.0f}K -> {total_new/1024:,.0f}K (saved {total_red:.1f}%)")
    print(f"  {'─' * 50}")
    print(f"  imgx v{__version__} | Donate: {__wallet__[:10]}...\n")

if __name__ == "__main__":
    main()
