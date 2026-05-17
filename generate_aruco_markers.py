#!/usr/bin/env python3
"""Generate ArUco marker PNG images for DICT_5X5_1000.

Usage:
    python generate_aruco_markers.py --out Markers/generated --count 1000
"""

import argparse
import re
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:
    raise SystemExit('OpenCV and numpy are required. Install with: pip install opencv-python numpy')


def parse_app_dict(dict_path):
    text = Path(dict_path).read_text(encoding='utf-8')
    pairs = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', text)
    if not pairs:
        raise SystemExit(f'Failed to parse dict file: {dict_path}')
    return [[int(a), int(b)] for a, b in pairs]


def render_app_marker(marker_bytes, size):
    # The UI preview in the app uses a 6x6 image with a 1-pixel black border
    # and a 4x4 payload inside. Bits are white when set.
    pattern = [((marker_bytes[0] >> i) & 1) for i in range(7, -1, -1)] + [((marker_bytes[1] >> i) & 1) for i in range(7, -1, -1)]
    pattern = pattern[:16]

    img = np.zeros((6, 6), dtype=np.uint8)
    for i in range(4):
        for j in range(4):
            if pattern[i * 4 + j]:
                img[i + 1, j + 1] = 255

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_NEAREST)
    return img


def main():
    parser = argparse.ArgumentParser(description='Generate ArUco marker images for DICT_5X5_1000.')
    parser.add_argument('--out', default='Markers/generated', help='Output directory for generated marker PNGs.')
    parser.add_argument('--count', type=int, default=1000, help='Number of marker IDs to generate (max 1000).')
    parser.add_argument('--size', type=int, default=512, help='Output image size in pixels.')
    parser.add_argument('--format', choices=['png', 'jpg'], default='png', help='Output image format.')
    parser.add_argument('--style', choices=['opencv', 'app'], default='opencv',
                        help='Image style: "opencv" for real ArUco markers, "app" for the internal app preview style.')
    parser.add_argument('--dict-file', default='Interface/MarkerGraphic/dict.ts',
                        help='Path to the app marker dictionary for app-style rendering.')
    args = parser.parse_args()

    if args.count < 1 or args.count > 1000:
        raise SystemExit('Count must be between 1 and 1000 for DICT_5X5_1000.')

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.style == 'opencv':
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)

    if args.style == 'app':
        marker_dict = parse_app_dict(args.dict_file)
        if len(marker_dict) < args.count:
            raise SystemExit(f'The app dictionary contains only {len(marker_dict)} markers.')

    for marker_id in range(args.count):
        if args.style == 'opencv':
            if hasattr(cv2.aruco, 'generateImageMarker'):
                marker = cv2.aruco.generateImageMarker(dictionary, marker_id, args.size)
            else:
                marker = cv2.aruco.drawMarker(dictionary, marker_id, args.size)
        else:
            marker = render_app_marker(marker_dict[marker_id], args.size)

        filename = out_dir / f'marker_{marker_id:04d}.{args.format}'
        cv2.imwrite(str(filename), marker)
        if marker_id % 100 == 0:
            print(f'Generated {marker_id}/{args.count} -> {filename}')

    print(f'Done. Generated {args.count} markers in: {out_dir.resolve()}')


if __name__ == '__main__':
    main()
