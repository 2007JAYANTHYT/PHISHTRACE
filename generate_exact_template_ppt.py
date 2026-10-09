import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_exact_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors exact to the template
    C_WHITE = RGBColor(255, 255, 255)
    C_TITLE = RGBColor(15, 23, 42)          # Bold dark #0F172A
    C_ORANGE = RGBColor(234, 88, 12)        # Primary orange #EA580C
    C_TEAL = RGBColor(13, 148, 136)         # Teal #0D9488
    C_CARD_BG = RGBColor(255, 255, 255)     # Clean white card
    C_CARD_BORDER = RGBColor(226, 232, 240) # Slate-200 border #E2E8F0
    C_PILL_BORDER = RGBColor(20, 184, 166)  # Teal border #14B8A6
    C_TEXT = RGBColor(30, 41, 59)           # Charcoal #1E293B
    C_MUTED = RGBColor(71, 85, 105)         # Muted #475569
    C_MLH_RED = RGBColor(231, 60, 39)       # MLH Red
    C_MLH_YELLOW = RGBColor(245, 158, 11)   # MLH Yellow/Gold
    C_IEEE_BLUE = RGBColor(2, 132, 199)     # IEEE Blue
    C_RAMAIAH_RED = RGBColor(190, 24, 43)   # Ramaiah Red

    def add_top_logos(slide):
        # Left: RAMAIAH
        r_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(3.5), Inches(0.8))
        tf_r = r_box.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r1 = tf_r.paragraphs[0]
        p_r1.text = "RAMAIAH"
        p_r1.font.name = "Arial Black"
        p_r1.font.size = Pt(14)
        p_r1.font.bold = True
        p_r1.font.color.rgb = C_RAMAIAH_RED

        p_r2 = tf_r.add_paragraph()
        p_r2.text = "Institute of Technology"
        p_r2.font.name = "Arial"
        p_r2.font.size = Pt(11)
        p_r2.font.color.rgb = C_TITLE

        # Center: MLH
        mlh_box = slide.shapes.add_textbox(Inches(5.6), Inches(0.3), Inches(2.133), Inches(0.9))
        tf_m = mlh_box.text_frame
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
        p_m = tf_m.paragraphs[0]
        p_m.alignment = PP_ALIGN.CENTER
        
        # ML in Red, H in Gold
        run_ml = p_m.add_run()
        run_ml.text = "ML"
        run_ml.font.name = "Arial Black"
        run_ml.font.size = Pt(36)
        run_ml.font.bold = True
        run_ml.font.color.rgb = C_MLH_RED

        run_h = p_m.add_run()
        run_h.text = "H"
        run_h.font.name = "Arial Black"
        run_h.font.size = Pt(36)
        run_h.font.bold = True
        run_h.font.color.rgb = C_MLH_YELLOW

        # Right: IEEE CIS
        ieee_box = slide.shapes.add_textbox(Inches(9.5), Inches(0.4), Inches(3.0), Inches(0.8))
        tf_i = ieee_box.text_frame
        tf_i.margin_left = tf_i.margin_top = tf_i.margin_right = tf_i.margin_bottom = 0
        tf_i.word_wrap = True
        p_i1 = tf_i.paragraphs[0]
        p_i1.alignment = PP_ALIGN.RIGHT
        p_i1.text = "IEEE"
        p_i1.font.name = "Arial Black"
        p_i1.font.size = Pt(12)
        p_i1.font.bold = True
        p_i1.font.color.rgb = C_IEEE_BLUE

        p_i2 = tf_i.add_paragraph()
        p_i2.alignment = PP_ALIGN.RIGHT
        p_i2.text = "Computational Intelligence Society"
        p_i2.font.name = "Arial"
        p_i2.font.size = Pt(10)
        p_i2.font.bold = True
        p_i2.font.color.rgb = C_TITLE

    def add_title(slide, title_text):
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.733), Inches(0.75))
        tf = t_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial Black"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = C_TITLE

    def add_footer(slide):
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf = f_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "Hacktoberfest Hack Day Bengaluru × IEEE RIT"
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_MUTED

    def draw_card_with_pill(slide, left, top, width, height, pill_text, body_text, orange_highlight=None, pill_orange=False):
        # Card container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.5)

        # Pill badge
        pill_w = Inches(len(pill_text) * 0.11 + 0.5)
        if pill_w > width - Inches(0.6):
            pill_w = width - Inches(0.6)
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.25), top + Inches(0.22), pill_w, Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_WHITE
        pill.line.color.rgb = C_ORANGE if pill_orange else C_PILL_BORDER
        pill.line.width = Pt(1.5)

        tf_p = pill.text_frame
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        p_pill = tf_p.paragraphs[0]
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.text = pill_text.upper()
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(9.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_ORANGE if pill_orange else C_TEAL

        # Body text
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.68), width - Inches(0.5), height - Inches(0.78))
        tf_b = tb.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        p = tf_b.paragraphs[0]
        if orange_highlight and orange_highlight in body_text:
            parts = body_text.split(orange_highlight)
            r1 = p.add_run()
            r1.text = parts[0]
            r1.font.name = "Arial"
            r1.font.size = Pt(11.5)
            r1.font.color.rgb = C_TEXT

            r_hl = p.add_run()
            r_hl.text = orange_highlight
            r_hl.font.name = "Arial"
            r_hl.font.size = Pt(11.5)
            r_hl.font.bold = True
            r_hl.font.color.rgb = C_ORANGE

            if len(parts) > 1:
                r2 = p.add_run()
                r2.text = parts[1]
                r2.font.name = "Arial"
                r2.font.size = Pt(11.5)
                r2.font.color.rgb = C_TEXT
        else:
            p.text = body_text
            p.font.name = "Arial"
            p.font.size = Pt(11.5)
            p.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 1: TEAM + IDEA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_top_logos(s1)
    add_title(s1, "TEAM + IDEA")

    # Orange Banner Box
    b_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.05), Inches(11.733), Inches(0.75))
    b_shape.fill.solid()
    b_shape.fill.fore_color.rgb = C_WHITE
    b_shape.line.color.rgb = RGBColor(251, 146, 60) # Orange border #FB923C
    b_shape.line.width = Pt(1.5)

    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.17), Inches(11.3), Inches(0.5))
    tf_tit = tb_title.text_frame
    p_tit = tf_tit.paragraphs[0]
    p_tit.text = "PROJECT TITLE: PhishTrace – AI Email Threat Forensics"
    p_tit.font.name = "Arial Black"
    p_tit.font.size = Pt(19)
    p_tit.font.bold = True
    p_tit.font.color.rgb = C_ORANGE

    # Subtitles
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(11.733), Inches(0.75))
    tf_sub = sub_box.text_frame
    tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
    p_s1 = tf_sub.paragraphs[0]
    p_s1.text = "SELECTED DOMAIN / TRACK: Cybersecurity & AI"
    p_s1.font.name = "Arial"
    p_s1.font.size = Pt(13)
    p_s1.font.bold = True
    p_s1.font.color.rgb = C_TEAL

    p_s2 = tf_sub.add_paragraph()
    p_s2.text = "TEAM NAME: Team Dark"
    p_s2.font.name = "Arial Black"
    p_s2.font.size = Pt(14)
    p_s2.font.bold = True
    p_s2.font.color.rgb = C_TITLE

    # 4 Team Members exactly matching template
    members = [
        ("LEAD", "JAYANTH.D\njayanthedu1116@gmail.com"),
        ("MEMBER 2", "DHANUSH.R\n(BACKEND)"),
        ("MEMBER 3", "VISHAL.R (AI\nTRAINING)"),
        ("MEMBER 4", "ARPITHA (\nRESEARCHER)")
    ]

    top_pos = 3.8
    for label, details in members:
        m_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.65))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = C_WHITE
        m_card.line.color.rgb = C_PILL_BORDER
        m_card.line.width = Pt(1.5)

        # Left label (LEAD / MEMBER)
        l_box = s1.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.12), Inches(1.8), Inches(0.45))
        tf_l = l_box.text_frame
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = label
        p_l.font.name = "Arial"
        p_l.font.size = Pt(12)
        p_l.font.bold = True
        p_l.font.color.rgb = C_TEAL

        # Separator line
        sep = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.9), Inches(top_pos + 0.1), Inches(0.02), Inches(0.45))
        sep.fill.solid()
        sep.fill.fore_color.rgb = C_CARD_BORDER
        sep.line.fill.background()

        # Details
        d_box = s1.shapes.add_textbox(Inches(3.1), Inches(top_pos + 0.08), Inches(9.2), Inches(0.5))
        tf_d = d_box.text_frame
        tf_d.margin_left = tf_d.margin_top = tf_d.margin_right = tf_d.margin_bottom = 0
        lines = details.split('\n')
        p_d1 = tf_d.paragraphs[0]
        p_d1.text = lines[0]
        p_d1.font.name = "Arial Black" if label == "LEAD" else "Arial"
        p_d1.font.size = Pt(12)
        p_d1.font.bold = True
        p_d1.font.color.rgb = C_TITLE if label != "LEAD" else C_TITLE

        if len(lines) > 1:
            p_d2 = tf_d.add_paragraph()
            p_d2.text = lines[1]
            p_d2.font.name = "Arial"
            p_d2.font.size = Pt(11)
            p_d2.font.bold = True
            p_d2.font.color.rgb = RGBColor(29, 78, 216) if "@" in lines[1] else C_TITLE

        top_pos += 0.75

    # Note
    note_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.88), Inches(11.733), Inches(0.35))
    tf_n = note_box.text_frame
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.text = "NOTE: ALL TEAM MEMBERS MUST REGISTER INDIVIDUALLY ON ORGANIZERHQ."
    p_n.font.name = "Arial"
    p_n.font.size = Pt(10.5)
    p_n.font.bold = True
    p_n.font.color.rgb = C_TEAL

    # ==========================================
    # SLIDE 2: THE PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_top_logos(s2)
    add_title(s2, "THE PROBLEM")
    add_footer(s2)

    draw_card_with_pill(s2, Inches(0.8), Inches(2.05), Inches(5.65), Inches(2.3),
                        "Target Audience",
                        "Security teams, banks, institutions and investigators, plus students and staff who face phishing every day.")

    draw_card_with_pill(s2, Inches(6.88), Inches(2.05), Inches(5.65), Inches(2.3),
                        "Core Friction",
                        "Filters block but do not trace. Header analysis is manual and one email at a time, and no open tool links detection, origin tracing, campaigns and court-ready evidence.")

    draw_card_with_pill(s2, Inches(0.8), Inches(4.55), Inches(5.65), Inches(2.3),
                        "Current Reality",
                        "Attackers use AI-written text and lookalike domains to evade filters; investigators trace relay paths by hand.")

    draw_card_with_pill(s2, Inches(6.88), Inches(4.55), Inches(5.65), Inches(2.3),
                        "Metric / Evidence",
                        "FBI IC3 2025: business email compromise losses hit $3.05B; phishing was the most-reported crime (191K+ complaints).",
                        orange_highlight="$3.05B")

    # ==========================================
    # SLIDE 3: PROPOSED SOLUTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_top_logos(s3)
    add_title(s3, "PROPOSED SOLUTION")
    add_footer(s3)

    # Left Card
    left_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.05), Inches(4.6), Inches(4.8))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = C_WHITE
    left_card.line.color.rgb = C_CARD_BORDER
    left_card.line.width = Pt(1.5)

    # Core concept pill
    pill_cc = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(2.28), Inches(1.8), Inches(0.35))
    pill_cc.fill.solid()
    pill_cc.fill.fore_color.rgb = C_WHITE
    pill_cc.line.color.rgb = C_PILL_BORDER
    pill_cc.line.width = Pt(1.5)
    tf_pcc = pill_cc.text_frame
    tf_pcc.margin_left = tf_pcc.margin_top = tf_pcc.margin_right = tf_pcc.margin_bottom = 0
    p_pcc = tf_pcc.paragraphs[0]
    p_pcc.alignment = PP_ALIGN.CENTER
    p_pcc.text = "CORE CONCEPT"
    p_pcc.font.name = "Arial"
    p_pcc.font.size = Pt(9.5)
    p_pcc.font.bold = True
    p_pcc.font.color.rgb = C_TEAL

    # Core concept text
    tb_cc = s3.shapes.add_textbox(Inches(1.05), Inches(2.75), Inches(4.1), Inches(1.6))
    tf_cc = tb_cc.text_frame
    tf_cc.word_wrap = True
    tf_cc.margin_left = tf_cc.margin_top = tf_cc.margin_right = tf_cc.margin_bottom = 0
    p_cc = tf_cc.paragraphs[0]
    p_cc.text = "An open-source platform that detects phishing and business email compromise (BEC), traces probable origin with confidence scores, and links attacks into campaigns with hashed evidence."
    p_cc.font.name = "Arial"
    p_cc.font.size = Pt(11)
    p_cc.font.color.rgb = C_TEXT

    # Key features pill
    pill_kf = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(4.55), Inches(1.6), Inches(0.35))
    pill_kf.fill.solid()
    pill_kf.fill.fore_color.rgb = C_WHITE
    pill_kf.line.color.rgb = C_PILL_BORDER
    pill_kf.line.width = Pt(1.5)
    tf_pkf = pill_kf.text_frame
    tf_pkf.margin_left = tf_pkf.margin_top = tf_pkf.margin_right = tf_pkf.margin_bottom = 0
    p_pkf = tf_pkf.paragraphs[0]
    p_pkf.alignment = PP_ALIGN.CENTER
    p_pkf.text = "KEY FEATURES"
    p_pkf.font.name = "Arial"
    p_pkf.font.size = Pt(9.5)
    p_pkf.font.bold = True
    p_pkf.font.color.rgb = C_TEAL

    # Features list
    tb_kf = s3.shapes.add_textbox(Inches(1.05), Inches(5.05), Inches(4.1), Inches(1.6))
    tf_kf = tb_kf.text_frame
    tf_kf.word_wrap = True
    tf_kf.margin_left = tf_kf.margin_top = tf_kf.margin_right = tf_kf.margin_bottom = 0

    feats = [
        ("Feature 01: ", "explainable threat detection"),
        ("Feature 02: ", "origin tracing + geo-confidence"),
        ("Feature 03: ", "campaign graph + hashed evidence")
    ]
    for idx, (f_num, f_desc) in enumerate(feats):
        p = tf_kf.paragraphs[0] if idx == 0 else tf_kf.add_paragraph()
        p.space_after = Pt(8)
        r1 = p.add_run()
        r1.text = f_num
        r1.font.name = "Arial"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = C_ORANGE
        r2 = p.add_run()
        r2.text = f_desc
        r2.font.name = "Arial"
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_TEXT

    # Right 3 Workflow Cards
    w_flow = Inches(2.05)
    gap = Inches(0.35)
    start_x = Inches(5.7)

    # 1. USER INPUT
    c1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, Inches(2.05), w_flow, Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_CARD_BORDER
    c1.line.width = Pt(1.5)

    tb_flow1 = s3.shapes.add_textbox(start_x + Inches(0.15), Inches(3.2), w_flow - Inches(0.3), Inches(3.0))
    tf_fl1 = tb_flow1.text_frame
    tf_fl1.word_wrap = True
    p_h1 = tf_fl1.paragraphs[0]
    p_h1.alignment = PP_ALIGN.CENTER
    p_h1.text = "USER INPUT"
    p_h1.font.name = "Arial Black"
    p_h1.font.size = Pt(12)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_TITLE
    p_h1.space_after = Pt(14)

    p_b1 = tf_fl1.add_paragraph()
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.text = ".eml files,\nheaders, body,\nattachments and\nURLs"
    p_b1.font.name = "Arial"
    p_b1.font.size = Pt(11)
    p_b1.font.color.rgb = C_TEXT

    # Arrow 1
    arr1 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, start_x + w_flow + Inches(0.06), Inches(4.3), Inches(0.23), Inches(0.2))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = C_PILL_BORDER
    arr1.line.fill.background()

    # 2. PROCESSING & LOGIC ENGINE
    start_x2 = start_x + w_flow + gap
    c2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x2, Inches(2.05), w_flow, Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_CARD_BORDER
    c2.line.width = Pt(1.5)

    tb_flow2 = s3.shapes.add_textbox(start_x2 + Inches(0.12), Inches(3.0), w_flow - Inches(0.24), Inches(3.2))
    tf_fl2 = tb_flow2.text_frame
    tf_fl2.word_wrap = True
    p_h2 = tf_fl2.paragraphs[0]
    p_h2.alignment = PP_ALIGN.CENTER
    p_h2.text = "PROCESSING &\nLOGIC ENGINE"
    p_h2.font.name = "Arial Black"
    p_h2.font.size = Pt(11.5)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_TITLE
    p_h2.space_after = Pt(14)

    p_b2 = tf_fl2.add_paragraph()
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.text = "header forensics,\nSPF/DKIM/DMARC,\nML scoring, geo-\nconfidence,\ncampaign graph"
    p_b2.font.name = "Arial"
    p_b2.font.size = Pt(11)
    p_b2.font.color.rgb = C_TEXT

    # Arrow 2
    arr2 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, start_x2 + w_flow + Inches(0.06), Inches(4.3), Inches(0.23), Inches(0.2))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = C_PILL_BORDER
    arr2.line.fill.background()

    # 3. DELIVERED OUTCOME
    start_x3 = start_x2 + w_flow + gap
    c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x3, Inches(2.05), w_flow, Inches(4.8))
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_WHITE
    c3.line.color.rgb = C_CARD_BORDER
    c3.line.width = Pt(1.5)

    tb_flow3 = s3.shapes.add_textbox(start_x3 + Inches(0.12), Inches(3.0), w_flow - Inches(0.24), Inches(3.2))
    tf_fl3 = tb_flow3.text_frame
    tf_fl3.word_wrap = True
    p_h3 = tf_fl3.paragraphs[0]
    p_h3.alignment = PP_ALIGN.CENTER
    p_h3.text = "DELIVERED\nOUTCOME"
    p_h3.font.name = "Arial Black"
    p_h3.font.size = Pt(11.5)
    p_h3.font.bold = True
    p_h3.font.color.rgb = C_TITLE
    p_h3.space_after = Pt(14)

    p_b3 = tf_fl3.add_paragraph()
    p_b3.alignment = PP_ALIGN.CENTER
    p_b3.text = "risk score with\nreasons, relay trace\nmap, campaign view,\nhashed forensic\nreport"
    p_b3.font.name = "Arial"
    p_b3.font.size = Pt(11)
    p_b3.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 4: OPEN-SOURCE AI APPROACH
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_top_logos(s4)
    add_title(s4, "OPEN-SOURCE AI APPROACH")
    add_footer(s4)

    draw_card_with_pill(s4, Inches(0.8), Inches(2.05), Inches(5.65), Inches(2.3),
                        "Model Selection",
                        "Open-weight Qwen2.5-7B-Instruct or Llama 3.1 8B (Cloud via Ollama)/ grok/gemini ; XLM-R / MuRIL for Hindi-English text; LightGBM classifier.")

    draw_card_with_pill(s4, Inches(6.88), Inches(2.05), Inches(5.65), Inches(2.3),
                        "Pipeline Role",
                        "Local LLM extracts BEC intent and explains verdicts; embeddings cluster similar emails; LightGBM fuses signals into a risk score.")

    draw_card_with_pill(s4, Inches(0.8), Inches(4.55), Inches(5.65), Inches(2.3),
                        "Technical Rationale",
                        "Laptop-friendly with low latency; emails never leave the machine; open weights are auditable; multilingual models handle Hinglish.")

    draw_card_with_pill(s4, Inches(6.88), Inches(4.55), Inches(5.65), Inches(2.3),
                        "External Services / APIs",
                        "GeoLite2 / DB-IP Lite, RDAP/WHOIS, Tor and blocklists, public phishing corpora (Nazario, SpamAssassin), NetworkX.")

    # ==========================================
    # SLIDE 5: ONE-DAY BUILD PLAN
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_top_logos(s5)
    add_title(s5, "ONE-DAY BUILD PLAN")
    add_footer(s5)

    # Left Card: MINIMUM VIABLE DEMO
    draw_card_with_pill(s5, Inches(0.8), Inches(2.05), Inches(4.8), Inches(3.7),
                        "Minimum Viable Demo",
                        "Upload a phishing .eml:\n\nrisk score with reasons,\nrelay trace map,\nhashed forensic PDF.")

    # Vertical line connecting milestone circles
    vline = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.05), Inches(2.4), Inches(0.04), Inches(2.6))
    vline.fill.solid()
    vline.fill.fore_color.rgb = C_PILL_BORDER
    vline.line.fill.background()

    # Milestones
    m_steps = [
        ("01", "MILESTONE 01 (MORNING)", "FastAPI setup, .eml parser, SPF/DKIM/DMARC checks, GeoLite2, baseline LightGBM model.", Inches(2.1)),
        ("02", "MILESTONE 02 (AFTERNOON)", "Trust-boundary logic, geo-confidence, local LLM intent extraction, hashed evidence log.", Inches(3.2)),
        ("03", "MILESTONE 03 (EVENING)", "React dashboard (risk gauge, trace map), PDF report, edge-case tests, pitch rehearsal.", Inches(4.3))
    ]

    for num, m_tit, m_desc, y_pos in m_steps:
        # Orange circle
        circ = s5.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.82), y_pos + Inches(0.05), Inches(0.5), Inches(0.5))
        circ.fill.solid()
        circ.fill.fore_color.rgb = C_ORANGE
        circ.line.fill.background()
        tf_c = circ.text_frame
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        p_c.text = num
        p_c.font.name = "Arial Black"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = C_WHITE

        # Text
        tb_m = s5.shapes.add_textbox(Inches(6.5), y_pos, Inches(6.0), Inches(0.95))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
        p_mt = tf_m.paragraphs[0]
        p_mt.text = m_tit
        p_mt.font.name = "Arial Black"
        p_mt.font.size = Pt(11.5)
        p_mt.font.bold = True
        p_mt.font.color.rgb = C_TEAL
        p_mt.space_after = Pt(2)

        p_md = tf_m.add_paragraph()
        p_md.text = m_desc
        p_md.font.name = "Arial"
        p_md.font.size = Pt(11)
        p_md.font.color.rgb = C_TEXT

    # Bottom Banner: FEEDBACK PLAN
    f_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.85))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = C_WHITE
    f_card.line.color.rgb = RGBColor(251, 146, 60) # Orange border #FB923C
    f_card.line.width = Pt(1.5)

    pill_fp = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.05), Inches(6.2), Inches(1.8), Inches(0.35))
    pill_fp.fill.solid()
    pill_fp.fill.fore_color.rgb = C_WHITE
    pill_fp.line.color.rgb = C_ORANGE
    pill_fp.line.width = Pt(1.5)
    tf_pfp = pill_fp.text_frame
    tf_pfp.margin_left = tf_pfp.margin_top = tf_pfp.margin_right = tf_pfp.margin_bottom = 0
    p_pfp = tf_pfp.paragraphs[0]
    p_pfp.alignment = PP_ALIGN.CENTER
    p_pfp.text = "FEEDBACK PLAN"
    p_pfp.font.name = "Arial"
    p_pfp.font.size = Pt(9.5)
    p_pfp.font.bold = True
    p_pfp.font.color.rgb = C_ORANGE

    tb_fp = s5.shapes.add_textbox(Inches(3.1), Inches(6.12), Inches(9.2), Inches(0.6))
    tf_fp = tb_fp.text_frame
    tf_fp.word_wrap = True
    tf_fp.margin_left = tf_fp.margin_top = tf_fp.margin_right = tf_fp.margin_bottom = 0
    p_fp = tf_fp.paragraphs[0]
    p_fp.text = "Backup: rules + LightGBM, offline GeoLite2, sample emails (no LLM, no live lookups). Feedback: test on 10 real .eml samples; 2 mentor reviews."
    p_fp.font.name = "Arial"
    p_fp.font.size = Pt(11)
    p_fp.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 6: IMPACT + FEASIBILITY
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_top_logos(s6)
    add_title(s6, "IMPACT + FEASIBILITY")
    add_footer(s6)

    draw_card_with_pill(s6, Inches(0.8), Inches(2.05), Inches(5.65), Inches(1.5),
                        "Measurable Impact",
                        "Benefits banks, institutions and response teams. Targets: precision >90%, false positives <2%, <5 s per email.")

    draw_card_with_pill(s6, Inches(0.8), Inches(3.7), Inches(5.65), Inches(1.5),
                        "Open-Source Contribution",
                        "Public MIT/Apache-2.0 repo with roadmap, README, sample .eml set and contribution guide.")

    draw_card_with_pill(s6, Inches(0.8), Inches(5.35), Inches(5.65), Inches(1.5),
                        "Technical Risk & Workaround",
                        "Risk: origin hidden by VPN, Tor or mail providers. Workaround: trusted-boundary logic, flag anonymizers, lower confidence.")

    # Right Tall Card: ETHICS & SAFETY
    r_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.88), Inches(2.05), Inches(5.65), Inches(4.8))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = C_WHITE
    r_card.line.color.rgb = C_CARD_BORDER
    r_card.line.width = Pt(1.5)

    pill_es = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.13), Inches(2.28), Inches(1.8), Inches(0.35))
    pill_es.fill.solid()
    pill_es.fill.fore_color.rgb = C_WHITE
    pill_es.line.color.rgb = C_PILL_BORDER
    pill_es.line.width = Pt(1.5)
    tf_pes = pill_es.text_frame
    tf_pes.margin_left = tf_pes.margin_top = tf_pes.margin_right = tf_pes.margin_bottom = 0
    p_pes = tf_pes.paragraphs[0]
    p_pes.alignment = PP_ALIGN.CENTER
    p_pes.text = "ETHICS & SAFETY"
    p_pes.font.name = "Arial"
    p_pes.font.size = Pt(9.5)
    p_pes.font.bold = True
    p_pes.font.color.rgb = C_TEAL

    tb_es = s6.shapes.add_textbox(Inches(7.13), Inches(2.78), Inches(5.15), Inches(3.9))
    tf_es = tb_es.text_frame
    tf_es.word_wrap = True
    tf_es.margin_left = tf_es.margin_top = tf_es.margin_right = tf_es.margin_bottom = 0

    p_e1 = tf_es.paragraphs[0]
    p_e1.text = "Privacy: local processing, PII masking, retention limits."
    p_e1.font.name = "Arial"
    p_e1.font.size = Pt(11.5)
    p_e1.font.bold = True
    p_e1.font.color.rgb = C_TEXT
    p_e1.space_after = Pt(16)

    p_e2 = tf_es.add_paragraph()
    p_e2.text = "Bias: multilingual train and test data, per-language error checks."
    p_e2.font.name = "Arial"
    p_e2.font.size = Pt(11.5)
    p_e2.font.bold = True
    p_e2.font.color.rgb = C_TEXT
    p_e2.space_after = Pt(16)

    p_e3 = tf_es.add_paragraph()
    p_e3.text = "Guardrails: LLM output tied to header evidence; confidence scores, not accusations; human review."
    p_e3.font.name = "Arial"
    p_e3.font.size = Pt(11.5)
    p_e3.font.bold = True
    p_e3.font.color.rgb = C_TEXT

    output_path = os.path.abspath("PhishTrace_Hacktoberfest_Team_Dark.pptx")
    prs.save(output_path)
    print(f"Template exact PPTX saved to: {output_path}")

if __name__ == "__main__":
    create_exact_deck()
