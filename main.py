#!/usr/bin/env python3
"""Build the meme for make.fun's 'Post the Meme, Win the Feed' bounty.

Reads base.png (the robot-at-3AM scene), draws the classic top/bottom meme
captions in bold white text with a black outline, and writes meme.png.
Deterministic: same base + same text = same bytes (verified by SHA-256).
Run: python3 main.py  (writes meme.png next to this file)
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_TEXT = "ME: JUST ENTER THE $2 MEME BOUNTY"
BOTTOM_TEXT = "MY AGENT AT 3 AM: SHIPPED IT, TESTED IT, SUBMITTED IT"


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_caption(draw, lines, font, img_w, y_top, stroke):
    """Draw centered lines starting at y_top; returns the y after the block."""
    y = y_top
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((img_w - w) / 2, y), line, font=font, fill="white",
                  stroke_width=stroke, stroke_fill="black")
        y += font.size + int(font.size * 0.18)
    return y


def main():
    img = Image.open(os.path.join(HERE, "base.png")).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    font_size = max(28, w // 22)
    font = ImageFont.truetype(FONT_PATH, font_size)
    stroke = max(2, font_size // 12)
    max_w = int(w * 0.92)
    margin = int(h * 0.035)

    top_lines = wrap_text(draw, TOP_TEXT, font, max_w)
    draw_caption(draw, top_lines, font, w, margin, stroke)

    bottom_lines = wrap_text(draw, BOTTOM_TEXT, font, max_w)
    line_h = font_size + int(font.size * 0.18)
    block_h = len(bottom_lines) * line_h - int(font.size * 0.18)
    draw_caption(draw, bottom_lines, font, w, h - margin - block_h, stroke)

    out = os.path.join(HERE, "meme.png")
    img.save(out, format="PNG")
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"meme.png: {w}x{h}, SHA-256 {sha}")


if __name__ == "__main__":
    main()
