#!/usr/bin/env python3
"""
Annotate GUIDE-005 Performance Metrics screenshots with instructional overlays.

Requirements from VISUAL_ASSETS_AUDIT.md lines 227-231:
- Label key metrics with plain English definitions
- Highlight threshold lines (10% heat limit)
- Add example calculations as overlays
- Circle important values

Annotation specs:
- Arrows: Red #FF0000, 3px
- Highlights: Yellow #FFFF00, 50% opacity
- Threshold circles: Red, 4px width
- Labels: White on dark background, 14pt
- Example calculations: Light blue background box
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Paths
IMAGES_DIR = "/Users/ianbutler/repos/SuperTrader/SuperClaude/triple-screen/docs/images"
OUTPUT_DIR = os.path.join(IMAGES_DIR, "annotated")

# Colors
RED = "#FF0000"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"
BLACK = "#000000"
LIGHT_BLUE = "#ADD8E6"
DARK_BG = "#333333"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_arrow(draw, start, end, color=RED, width=3):
    """Draw an arrow from start to end."""
    draw.line([start, end], fill=color, width=width)

    # Calculate arrow head
    import math
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6

    left_x = end[0] - arrow_length * math.cos(angle - arrow_angle)
    left_y = end[1] - arrow_length * math.sin(angle - arrow_angle)
    right_x = end[0] - arrow_length * math.cos(angle + arrow_angle)
    right_y = end[1] - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([end, (left_x, left_y), (right_x, right_y)], fill=color)


def draw_label(draw, position, text, font, bg_color=DARK_BG, text_color=WHITE):
    """Draw text label with background."""
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw background rectangle
    padding = 5
    rect = [
        position[0] - padding,
        position[1] - padding,
        position[0] + text_width + padding,
        position[1] + text_height + padding
    ]
    draw.rectangle(rect, fill=bg_color)

    # Draw text
    draw.text(position, text, fill=text_color, font=font)


def draw_highlight_box(draw, rect, color=YELLOW, opacity=128):
    """Draw semi-transparent highlight box."""
    # Create overlay for transparency
    overlay = Image.new('RGBA', (rect[2] - rect[0], rect[3] - rect[1]),
                        color + f"{opacity:02x}")
    return overlay, (rect[0], rect[1])


def annotate_equity_curve(image_path):
    """
    Annotate equity curve screenshot:
    - Label axes: "Time" (x-axis), "Portfolio Value (£)" (y-axis)
    - Arrow to trend line
    - Label: "Upward trend = profitable system"
    """
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    # Try to use default font, fall back to basic if needed
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        font = ImageFont.load_default()
        font_large = font

    width, height = img.size

    # X-axis label
    draw_label(draw, (width // 2 - 20, height - 30), "Time", font_large)

    # Y-axis label (rotated text simulation with regular text)
    draw_label(draw, (10, 50), "Portfolio Value (£)", font_large)

    # Arrow pointing to upward trend (assuming chart is in center-right)
    arrow_start = (width - 200, 100)
    arrow_end = (width - 250, 150)
    draw_arrow(draw, arrow_start, arrow_end, color=RED, width=3)

    # Trend explanation label
    draw_label(draw, (width - 350, 70), "Upward trend = profitable system",
               font, bg_color=DARK_BG, text_color=WHITE)

    return img


def annotate_metrics_summary(image_path):
    """
    Annotate metrics summary screenshot:
    - Label key metrics with plain English:
      - "R-multiple: Average gain per £1 risked"
      - "Expectancy: Expected £ per trade"
      - "Win Rate: % of winning trades"
      - "Profit Factor: Gross profit ÷ gross loss"
    - Add example calculation overlay: "Risk £100, make £300 = 3R"
    """
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except:
        font = ImageFont.load_default()
        font_small = font

    width, height = img.size

    # Metric labels (positioned vertically down the left side)
    y_start = 100
    y_spacing = 80

    metrics = [
        "R-multiple: Average gain per £1 risked",
        "Expectancy: Expected £ per trade",
        "Win Rate: % of winning trades",
        "Profit Factor: Gross profit ÷ gross loss"
    ]

    for i, metric in enumerate(metrics):
        y_pos = y_start + (i * y_spacing)
        draw_label(draw, (20, y_pos), metric, font_small,
                   bg_color=DARK_BG, text_color=WHITE)

    # Example calculation box (light blue background)
    calc_text = "Example: Risk £100, make £300 = 3R"
    calc_x = width - 350
    calc_y = height - 80

    # Draw calculation box
    bbox = draw.textbbox((0, 0), calc_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    padding = 8

    calc_rect = [
        calc_x - padding,
        calc_y - padding,
        calc_x + text_width + padding,
        calc_y + text_height + padding
    ]
    draw.rectangle(calc_rect, fill=LIGHT_BLUE, outline=BLACK, width=2)
    draw.text((calc_x, calc_y), calc_text, fill=BLACK, font=font)

    return img


def annotate_portfolio_heat(image_path):
    """
    Annotate portfolio heat gauge screenshot:
    - Highlight 10% threshold line (red circle)
    - Label: "Portfolio Heat: Total risk across all positions"
    - Label threshold: "10% limit (never exceed)"
    - Show current heat percentage with arrow
    """
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        font = ImageFont.load_default()
        font_large = font

    width, height = img.size

    # Main label at top
    draw_label(draw, (width // 2 - 150, 20),
               "Portfolio Heat: Total risk across all positions",
               font_large, bg_color=DARK_BG, text_color=WHITE)

    # Circle around 10% threshold (assuming gauge is centered)
    threshold_x = width // 2
    threshold_y = height // 2
    circle_radius = 40

    # Draw red circle around threshold
    draw.ellipse([
        threshold_x - circle_radius,
        threshold_y - circle_radius,
        threshold_x + circle_radius,
        threshold_y + circle_radius
    ], outline=RED, width=4)

    # Threshold label
    draw_label(draw, (threshold_x + 50, threshold_y - 50),
               "10% limit (never exceed)",
               font, bg_color=RED, text_color=WHITE)

    # Arrow to current heat value (assuming it's above the gauge)
    arrow_start = (threshold_x - 100, threshold_y - 80)
    arrow_end = (threshold_x - 50, threshold_y - 60)
    draw_arrow(draw, arrow_start, arrow_end, color=RED, width=3)

    draw_label(draw, (threshold_x - 150, threshold_y - 100),
               "Current heat %",
               font, bg_color=DARK_BG, text_color=WHITE)

    return img


def annotate_trade_distribution(image_path):
    """
    Annotate trade distribution histogram:
    - Label x-axis: "R-multiple (profit/loss in R)"
    - Label y-axis: "Number of trades"
    - Highlight positive R side (green) and negative R side (red)
    - Label: "Goal: More trades on right (winners) than left (losers)"
    """
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        font = ImageFont.load_default()
        font_large = font

    width, height = img.size

    # Axis labels
    draw_label(draw, (width // 2 - 100, height - 30),
               "R-multiple (profit/loss in R)", font_large)
    draw_label(draw, (10, 50), "Number of trades", font_large)

    # Highlight negative R side (left, red)
    left_rect = [20, 100, width // 2 - 50, height - 60]
    draw.rectangle(left_rect, outline=RED, width=3)
    draw_label(draw, (50, 110), "Losers (negative R)",
               font, bg_color=RED, text_color=WHITE)

    # Highlight positive R side (right, green)
    right_rect = [width // 2 + 50, 100, width - 20, height - 60]
    draw.rectangle(right_rect, outline="#00FF00", width=3)
    draw_label(draw, (width - 200, 110), "Winners (positive R)",
               font, bg_color="#006400", text_color=WHITE)

    # Goal label at top
    draw_label(draw, (width // 2 - 200, 20),
               "Goal: More trades on right (winners) than left (losers)",
               font_large, bg_color=DARK_BG, text_color=WHITE)

    return img


def main():
    """Process all 4 GUIDE-005 screenshots."""

    screenshots = [
        ("guide-005_01_equity-curve.png", annotate_equity_curve),
        ("guide-005_02_metrics-summary.png", annotate_metrics_summary),
        ("guide-005_03_portfolio-heat-gauge.png", annotate_portfolio_heat),
        ("guide-005_04_trade-distribution.png", annotate_trade_distribution)
    ]

    annotated_count = 0

    for filename, annotate_func in screenshots:
        input_path = os.path.join(IMAGES_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        print(f"Processing {filename}...")

        try:
            annotated_img = annotate_func(input_path)

            # Convert back to RGB for PNG saving
            if annotated_img.mode == 'RGBA':
                rgb_img = Image.new('RGB', annotated_img.size, (255, 255, 255))
                rgb_img.paste(annotated_img, mask=annotated_img.split()[3])
                rgb_img.save(output_path, 'PNG', optimize=True)
            else:
                annotated_img.save(output_path, 'PNG', optimize=True)

            print(f"✓ Saved to {output_path}")
            annotated_count += 1

        except Exception as e:
            print(f"✗ Error processing {filename}: {e}")

    print(f"\n{'='*60}")
    print(f"Annotation complete: {annotated_count}/4 screenshots processed")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}")

    # Report specific labels added
    print("\nLabels added per image:")
    print("\n1. equity-curve.png:")
    print("   - X-axis: 'Time'")
    print("   - Y-axis: 'Portfolio Value (£)'")
    print("   - Arrow + label: 'Upward trend = profitable system'")

    print("\n2. metrics-summary.png:")
    print("   - R-multiple definition")
    print("   - Expectancy definition")
    print("   - Win Rate definition")
    print("   - Profit Factor definition")
    print("   - Example calculation: 'Risk £100, make £300 = 3R'")

    print("\n3. portfolio-heat-gauge.png:")
    print("   - Main label: 'Portfolio Heat: Total risk across all positions'")
    print("   - Red circle around 10% threshold")
    print("   - Threshold label: '10% limit (never exceed)'")
    print("   - Arrow to current heat percentage")

    print("\n4. trade-distribution.png:")
    print("   - X-axis: 'R-multiple (profit/loss in R)'")
    print("   - Y-axis: 'Number of trades'")
    print("   - Red box highlighting negative R (losers)")
    print("   - Green box highlighting positive R (winners)")
    print("   - Goal label at top")


if __name__ == "__main__":
    main()
