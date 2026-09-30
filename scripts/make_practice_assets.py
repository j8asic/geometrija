#!/usr/bin/env python3
"""Generate the original teaching body plan and offsets. Python 3 standard library only."""
import csv
import math
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "downloads"
W, H = 1120, 1000
OX, OZ, SCALE = 150, 850, 360
FONT = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    ".": ["00000"] * 5 + ["00100", "00100"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    " ": ["00000"] * 7,
}


def generate():
    with (OUT / "practice-stations.csv").open(newline="", encoding="utf-8") as f:
        stations = list(csv.DictReader(f))
    if len(stations) != 5:
        raise ValueError("The introductory exercise expects five stations.")
    rows = []
    curves = []
    for row in stations:
        x, b, k, d = (float(row[key]) for key in
                      ("x_m", "half_breadth_m", "keel_z_m", "sheer_z_m"))
        if not (0 < b <= 2 and 0 <= k < d <= 2):
            raise ValueError("Practice station is outside the drawing bounds.")
        def point(theta):
            return b * math.sin(theta), k + (d - k) * (1 - math.cos(theta))
        for j in range(7):
            y, z = point(j * math.pi / 12)
            rows.append([row["station"], j, f"{x:.6f}", f"{y:.6f}", f"{z:.6f}"])
        curves.append((row["station"], [point(j * math.pi / 480) for j in range(241)]))
    with (OUT / "practice-offsets.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station", "point", "x_m", "y_m", "z_m"])
        writer.writerows(rows)

    pixels = bytearray([255]) * (W * H)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           '<title id="title">Synthetic half-body plan for the Rhino exercise</title>',
           '<desc id="desc">Five half-sections S0 to S4. Horizontal axis is world Y in metres, vertical axis world Z in metres. All sections are overlaid; longitudinal positions are in practice-stations.csv. This is not a real vessel.</desc>',
           '<rect width="100%" height="100%" fill="white"/>']

    def dot(x, y, shade=0, radius=1):
        for yy in range(round(y)-radius, round(y)+radius+1):
            for xx in range(round(x)-radius, round(x)+radius+1):
                if 0 <= xx < W and 0 <= yy < H:
                    pixels[yy * W + xx] = shade

    def line(x1, y1, x2, y2, shade=0, width=2):
        n = max(1, math.ceil(max(abs(x2-x1), abs(y2-y1))))
        for i in range(n+1):
            t = i/n
            dot(x1 + t*(x2-x1), y1 + t*(y2-y1), shade, (width-1)//2)
        svg.append(f'<path d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f}" fill="none" stroke="rgb({shade},{shade},{shade})" stroke-width="{width}"/>')

    def text(x, y, value, size=3):
        for n, ch in enumerate(value):
            for j, row in enumerate(FONT[ch]):
                for i, bit in enumerate(row):
                    if bit == "1":
                        for yy in range(size):
                            for xx in range(size):
                                dot(x+n*6*size+i*size+xx, y+j*size+yy, 0, 0)
        svg.append(f'<text x="{x}" y="{y+7*size}" font-family="sans-serif" font-size="{8*size}">{value}</text>')

    def screen(y, z):
        return OX + SCALE*y, OZ - SCALE*z

    for i in range(5):
        v = i/2
        px, pz = screen(v, v)
        line(px, OZ, px, OZ-2*SCALE, 210, 1)
        line(OX, pz, OX+2*SCALE, pz, 210, 1)
        text(round(px)-20, OZ+20, f"{v:.1f}")
        text(OX-85, round(pz)-10, f"{v:.1f}")
    line(OX, OZ, OX+2.15*SCALE, OZ, 0, 3)
    line(OX, OZ, OX, OZ-2.15*SCALE, 0, 3)
    text(OX+int(2.2*SCALE), OZ+5, "Y M")
    text(OX-25, OZ-int(2.2*SCALE)-20, "Z M")
    for name, pts in curves:
        for a, b in zip(pts, pts[1:]):
            line(*screen(*a), *screen(*b), 35, 3)
        px, pz = screen(*pts[-1])
        text(round(px)-12, round(pz)-35, name, 2)
    for _, _, _, y, z in rows:
        px, pz = screen(float(y), float(z))
        dot(px, pz, 0, 3)
        svg.append(f'<circle cx="{px:.2f}" cy="{pz:.2f}" r="3"/>')
    svg.append('</svg>')
    (OUT / "practice-body-plan.svg").write_text("\n".join(svg)+"\n", encoding="utf-8")

    def chunk(kind, data):
        return struct.pack("!I", len(data)) + kind + data + struct.pack("!I", zlib.crc32(kind+data) & 0xffffffff)
    scanlines = b"".join(b"\0" + pixels[y*W:(y+1)*W] for y in range(H))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack("!2I5B", W, H, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b"")
    (OUT / "practice-body-plan.png").write_bytes(png)
    print(f"Generated PNG, SVG and {len(rows)} reference points in {OUT}")


if __name__ == "__main__":
    generate()
