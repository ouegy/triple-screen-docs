#!/usr/bin/env python3
"""
Annotate GUIDE-004 Trade Journaling screenshots
Creates annotated versions with arrows, highlights, labels, and numbered criteria
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Paths
IMAGES_DIR = "/Users/ianbutler/repos/SuperTrader/SuperClaude/triple-screen/docs/images"
OUTPUT_DIR = "/Users/ianbutler/repos/SuperTrader/SuperClaude/triple-screen/docs/images/annotated"

# Annotation colors
RED = "#FF0000"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"
BLACK = "#000000"
DARK_BG = "#1E3A5F"

# Dimensions
ARROW_WIDTH = 3
HIGHLIGHT_OPACITY = 128  # 50% opacity
CIRCLE_RADIUS = 20
FONT_SIZE_LABEL = 14
FONT_SIZE_NUMBER = 18

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size):
    """Get font with fallback to default"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/SFNSText.ttf", size)
        except:
            return ImageFont.load_default()

def draw_arrow(draw, start, end, color=RED, width=ARROW_WIDTH):
    """Draw arrow from start to end point"""
    # Draw line
    draw.line([start, end], fill=color, width=width)

    # Draw arrowhead (simple triangle)
    import math
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6

    left_x = end[0] - arrow_length * math.cos(angle - arrow_angle)
    left_y = end[1] - arrow_length * math.sin(angle - arrow_angle)
    right_x = end[0] - arrow_length * math.cos(angle + arrow_angle)
    right_y = end[1] - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([end, (left_x, left_y), (right_x, right_y)], fill=color)

def draw_highlight_box(img, draw, bbox, color=YELLOW, opacity=HIGHLIGHT_OPACITY):
    """Draw semi-transparent highlight box"""
    # Create overlay for transparency
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Convert hex to RGB
    rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    overlay_draw.rectangle(bbox, fill=rgb + (opacity,))

    # Composite overlay
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))

def draw_numbered_circle(draw, center, number, font):
    """Draw circle with number inside"""
    x, y = center

    # Draw circle
    draw.ellipse([x - CIRCLE_RADIUS, y - CIRCLE_RADIUS,
                  x + CIRCLE_RADIUS, y + CIRCLE_RADIUS],
                 fill=RED, outline=WHITE, width=2)

    # Draw number
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x - text_width // 2, y - text_height // 2),
              text, fill=WHITE, font=font)

def draw_label(draw, position, text, font, bg_color=DARK_BG, text_color=WHITE):
    """Draw label with background"""
    x, y = position

    # Get text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw background
    padding = 5
    draw.rectangle([x - padding, y - padding,
                   x + text_width + padding, y + text_height + padding],
                  fill=bg_color)

    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)

def annotate_apgar_position_dropdown(input_path, output_path):
    """Annotate screenshot 01: Position selector"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Arrow to position dropdown (assume top area)
    draw_arrow(draw, (width - 100, 80), (width // 2, 120))
    draw_label(draw, (width - 220, 60), "Select Position", font_label)

    # Highlight status filter area
    draw_highlight_box(img, draw, (20, 80, 200, 140))
    draw_label(draw, (25, 145), "Status Filter", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)}")

def annotate_apgar_criteria_scoring(input_path, output_path):
    """Annotate screenshot 02: 5 Apgar criteria with numbered circles"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_number = get_font(FONT_SIZE_NUMBER)

    width, height = img.size

    # Criteria labels (approximate positions - adjust based on actual screenshot)
    criteria = [
        ("Daily Price Action", 200),
        ("MACD Uptick", 320),
        ("Weekly Impulse", 440),
        ("RSI", 560),
        ("Perfection", 680)
    ]

    for idx, (label, y_pos) in enumerate(criteria, 1):
        # Number the criterion
        draw_numbered_circle(draw, (30, y_pos), idx, font_number)

        # Label the criterion
        draw_label(draw, (60, y_pos - 10), label, font_label)

        # Highlight scoring buttons (0, 1, 2)
        # Assume buttons are in middle area
        for button_offset in [0, 100, 200]:
            draw_highlight_box(img, draw,
                             (300 + button_offset, y_pos - 15,
                              360 + button_offset, y_pos + 15))

    # Add legend for scoring
    draw_label(draw, (320, 100), "0 points", font_label)
    draw_label(draw, (420, 100), "1 point", font_label)
    draw_label(draw, (520, 100), "2 points", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - 5 criteria numbered + scoring highlighted")

def annotate_apgar_total_score(input_path, output_path):
    """Annotate screenshot 03: Total score display"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Highlight total score area (assume center-bottom)
    score_box = (width // 2 - 100, height - 200, width // 2 + 100, height - 150)
    draw_highlight_box(img, draw, score_box)

    # Label A-trade threshold
    draw_label(draw, (width // 2 - 150, height - 130),
               "10 points = A-trade", font_label)
    draw_label(draw, (width // 2 - 150, height - 105),
               "< 7 = C-trade (consider removal)", font_label)

    # Arrow to score
    draw_arrow(draw, (width // 2 + 150, height - 175), (width // 2 + 50, height - 175))

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Score threshold labeled")

def annotate_apgar_market_context(input_path, output_path):
    """Annotate screenshot 04: Earnings/dividend fields"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Highlight earnings date field
    draw_highlight_box(img, draw, (50, 200, 300, 240))
    draw_label(draw, (310, 210), "Check Briefing.com", font_label)

    # Highlight dividend date field
    draw_highlight_box(img, draw, (50, 260, 300, 300))
    draw_label(draw, (310, 270), "Check Yahoo Finance", font_label)

    # Highlight market conditions textarea
    draw_highlight_box(img, draw, (50, 340, width - 50, 440))
    draw_label(draw, (60, 450), "Describe market/sector context", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Context fields highlighted")

def annotate_apgar_entry_reason(input_path, output_path):
    """Annotate screenshot 05: Entry rationale"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Highlight entry reason textarea
    draw_highlight_box(img, draw, (50, 150, width - 50, 300))

    # Add example annotation
    draw_label(draw, (60, 310),
               "Be specific: reference exact technical signals", font_label)

    # Arrow to Save button (assume bottom)
    draw_arrow(draw, (width - 100, height - 100), (width - 200, height - 60))
    draw_label(draw, (width - 180, height - 120), "Save", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Entry reason + Save button")

def annotate_apgar_chart_upload(input_path, output_path):
    """Annotate screenshot 06: Chart upload section"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Highlight daily chart upload
    draw_highlight_box(img, draw, (50, 150, 350, 200))
    draw_label(draw, (360, 165), "Daily chart upload", font_label)

    # Highlight weekly chart upload
    draw_highlight_box(img, draw, (50, 220, 350, 270))
    draw_label(draw, (360, 235), "Weekly chart upload", font_label)

    # Success message area (if visible)
    draw_label(draw, (60, 290),
               "✓ Upload success confirmation appears here", font_label)

    # Arrow to Save Apgar button
    draw_arrow(draw, (width - 100, height - 80), (width - 250, height - 50))
    draw_label(draw, (width - 230, height - 100), "Save Apgar & Context", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Upload fields + success message")

def annotate_journal_position_selector(input_path, output_path):
    """Annotate screenshot 07: Journal position dropdown"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)

    width, height = img.size

    # Arrow to position selector
    draw_arrow(draw, (width - 100, 100), (width // 2 + 50, 140))
    draw_label(draw, (width - 220, 80), "Select Closed Position", font_label)

    # Highlight filters
    draw_highlight_box(img, draw, (20, 80, 250, 130))
    draw_label(draw, (25, 135), "Exit Details Filter", font_label)

    draw_highlight_box(img, draw, (270, 80, 500, 130))
    draw_label(draw, (275, 135), "Review Status Filter", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)}")

def annotate_journal_section(input_path, output_path, section_letter, section_title,
                            read_only=False, has_save=True):
    """Generic journal section annotator"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_section = get_font(18)

    width, height = img.size

    # Section header label
    header_text = f"Section {section_letter}: {section_title}"
    draw_label(draw, (20, 20), header_text, font_section, bg_color=RED)

    if read_only:
        # Highlight as read-only
        draw_label(draw, (width - 150, 25), "READ-ONLY", font_label, bg_color="#666666")

    if has_save:
        # Arrow to Save button
        draw_arrow(draw, (width - 100, height - 80), (width - 200, height - 50))
        draw_label(draw, (width - 180, height - 100), "Save", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Section {section_letter}")

def annotate_journal_section_a(input_path, output_path):
    """Annotate screenshot 08: Section A - Entry reason (read-only)"""
    annotate_journal_section(input_path, output_path, "A",
                            "Reason for Entry", read_only=True, has_save=False)

def annotate_journal_section_b(input_path, output_path):
    """Annotate screenshot 09: Section B - Entry/Exit docs (auto-populated)"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_section = get_font(18)

    width, height = img.size

    # Section header
    draw_label(draw, (20, 20), "Section B: Entry/Exit Documentation",
               font_section, bg_color=RED)
    draw_label(draw, (width - 200, 25), "AUTO-POPULATED",
               font_label, bg_color="#006600")

    # Highlight key fields
    fields = [
        ("Entry Date/Price", 150),
        ("Exit Date/Price", 220),
        ("Gain/Loss %", 290),
        ("R-multiple", 360)
    ]

    for label, y_pos in fields:
        draw_highlight_box(img, draw, (50, y_pos, 250, y_pos + 30))
        draw_label(draw, (260, y_pos + 5), label, font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Section B with key fields")

def annotate_journal_section_c(input_path, output_path):
    """Annotate screenshot 10: Section C - Exit reason"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_section = get_font(18)

    width, height = img.size

    # Section header
    draw_label(draw, (20, 20), "Section C: Reason for Exit",
               font_section, bg_color=RED)

    # Highlight exit description textarea
    draw_highlight_box(img, draw, (50, 100, width - 50, 250))
    draw_label(draw, (60, 260), "Be specific about exit signals", font_label)

    # Highlight chart upload
    draw_highlight_box(img, draw, (50, 300, 350, 350))
    draw_label(draw, (360, 315), "Upload exit chart", font_label)

    # Arrow to Save button
    draw_arrow(draw, (width - 100, height - 80), (width - 200, height - 50))
    draw_label(draw, (width - 220, height - 100), "Save Exit Details", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Section C with Save button")

def annotate_journal_section_d(input_path, output_path):
    """Annotate screenshot 11: Section D - Exit tactic"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_section = get_font(18)

    width, height = img.size

    # Section header
    draw_label(draw, (20, 20), "Section D: Exit Tactic",
               font_section, bg_color=RED)

    # Highlight dropdown
    draw_highlight_box(img, draw, (50, 100, 400, 140))
    draw_label(draw, (410, 110), "Elder's 8 exit tactics", font_label)

    # Label key tactics
    tactics_y = 180
    draw_label(draw, (60, tactics_y), "2:1 Hit target", font_label)
    draw_label(draw, (60, tactics_y + 30), "2:2 Hit stop", font_label)
    draw_label(draw, (60, tactics_y + 60), "2:6 Couldn't stand the pain", font_label)

    # Arrow to Save button
    draw_arrow(draw, (width - 100, height - 80), (width - 200, height - 50))
    draw_label(draw, (width - 220, height - 100), "Save Exit Tactic", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Section D with tactics")

def annotate_journal_section_e(input_path, output_path):
    """Annotate screenshot 12: Section E - Post-trade review"""
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    font_label = get_font(FONT_SIZE_LABEL)
    font_section = get_font(18)

    width, height = img.size

    # Section header
    draw_label(draw, (20, 20), "Section E: Post-Trade Analysis",
               font_section, bg_color=RED)

    # Eligibility notice
    draw_label(draw, (50, 70), "⏱ 60-day waiting period enforced",
               font_label, bg_color="#FF6600")

    # Highlight review textarea
    draw_highlight_box(img, draw, (50, 130, width - 50, 280))
    draw_label(draw, (60, 290), "Hindsight analysis: What did you learn?", font_label)

    # Highlight follow-up chart upload
    draw_highlight_box(img, draw, (50, 330, 350, 380))
    draw_label(draw, (360, 345), "Upload follow-up chart", font_label)

    # Arrow to Save button
    draw_arrow(draw, (width - 100, height - 80), (width - 220, height - 50))
    draw_label(draw, (width - 260, height - 100), "Save Post-Trade Review", font_label)

    img.save(output_path)
    print(f"✓ Annotated: {os.path.basename(output_path)} - Section E with 60-day notice")

def main():
    """Annotate all GUIDE-004 screenshots"""
    print("GUIDE-004 Trade Journaling Screenshot Annotation")
    print("=" * 60)

    ensure_output_dir()

    screenshots = [
        ("guide-004_01_apgar-position-dropdown.png", annotate_apgar_position_dropdown),
        ("guide-004_02_apgar-criteria-scoring.png", annotate_apgar_criteria_scoring),
        ("guide-004_03_apgar-total-score.png", annotate_apgar_total_score),
        ("guide-004_04_apgar-market-context.png", annotate_apgar_market_context),
        ("guide-004_05_apgar-entry-reason.png", annotate_apgar_entry_reason),
        ("guide-004_06_apgar-chart-upload.png", annotate_apgar_chart_upload),
        ("guide-004_07_journal-position-selector.png", annotate_journal_position_selector),
        ("guide-004_08_journal-section-a.png", annotate_journal_section_a),
        ("guide-004_09_journal-section-b.png", annotate_journal_section_b),
        ("guide-004_10_journal-section-c.png", annotate_journal_section_c),
        ("guide-004_11_journal-section-d.png", annotate_journal_section_d),
        ("guide-004_12_journal-section-e.png", annotate_journal_section_e),
    ]

    annotated_count = 0
    for filename, annotator_func in screenshots:
        input_path = os.path.join(IMAGES_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(input_path):
            try:
                annotator_func(input_path, output_path)
                annotated_count += 1
            except Exception as e:
                print(f"✗ Error annotating {filename}: {e}")
        else:
            print(f"⚠ Missing: {filename}")

    print("=" * 60)
    print(f"Annotation complete: {annotated_count}/12 screenshots")
    print(f"Output directory: {OUTPUT_DIR}")

    # Summary of key annotations
    print("\nKey annotations applied:")
    print("  Apgar page (6 screenshots):")
    print("    - 5 criteria numbered (1-5 in circles)")
    print("    - Scoring buttons highlighted (0, 1, 2 points)")
    print("    - Labels: Daily Price, MACD, Weekly Impulse, RSI, Perfection")
    print("    - Total score threshold labeled (10 = A-trade, <7 = C-trade)")
    print("    - Save buttons with arrows")
    print("    - Upload success message areas")
    print("  Journal page (6 screenshots):")
    print("    - Section headers labeled (A, B, C, D, E)")
    print("    - Read-only vs editable fields differentiated")
    print("    - Save buttons with arrows")
    print("    - Key fields highlighted (R-multiple, exit tactics)")
    print("    - 60-day waiting period notice")

if __name__ == "__main__":
    main()
