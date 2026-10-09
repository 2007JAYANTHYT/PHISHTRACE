import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors matching the MLH / Ramaiah / IEEE template
    C_BG = RGBColor(255, 255, 255)
    C_TITLE = RGBColor(15, 23, 42)        # Very dark navy #0F172A
    C_ORANGE = RGBColor(234, 88, 12)       # Accent orange #EA580C
    C_TEAL = RGBColor(13, 148, 136)        # Teal badge #0D9488
    C_CARD_BG = RGBColor(248, 250, 252)    # Slate light card #F8FAFC
    C_CARD_BORDER = RGBColor(203, 213, 225)# Slate border #CBD5E1
    C_TEXT = RGBColor(30, 41, 59)          # Dark slate #1E293B
    C_MUTED = RGBColor(100, 116, 139)      # Muted slate #64748B
    C_WHITE = RGBColor(255, 255, 255)
    C_RED = RGBColor(225, 29, 72)          # Rose/Red for MLH accent #E11D48
    C_BLUE = RGBColor(2, 132, 199)         # IEEE Blue #0284C7
    C_GREEN = RGBColor(22, 163, 74)        # Green #16A34A

    def add_header(slide, title_text):
        # Header banner with Ramaiah, MLH, and IEEE text representations
        h_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(4.0), Inches(0.7))
        tf = h_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "RAMAIAH Institute of Technology"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = RGBColor(180, 20, 30)

        # Center MLH Badge
        mlh_box = slide.shapes.add_textbox(Inches(5.6), Inches(0.3), Inches(2.2), Inches(0.8))
        tf_m = mlh_box.text_frame
        p_m = tf_m.paragraphs[0]
        p_m.alignment = PP_ALIGN.CENTER
        p_m.text = "MLH"
        p_m.font.name = "Arial Black"
        p_m.font.size = Pt(32)
        p_m.font.bold = True
        p_m.font.color.rgb = RGBColor(234, 88, 12)

        # Right IEEE Badge
        ieee_box = slide.shapes.add_textbox(Inches(9.2), Inches(0.4), Inches(3.3), Inches(0.7))
        tf_i = ieee_box.text_frame
        p_i = tf_i.paragraphs[0]
        p_i.alignment = PP_ALIGN.RIGHT
        p_i.text = "IEEE Computational Intelligence Society"
        p_i.font.name = "Arial"
        p_i.font.size = Pt(11)
        p_i.font.bold = True
        p_i.font.color.rgb = C_BLUE

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(0.8))
        tf_t = t_box.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Arial Black"
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TITLE

        # Footer
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.35))
        tf_f = f_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.alignment = PP_ALIGN.CENTER
        p_f.text = "Hacktoberfest Hack Day Bengaluru × IEEE RIT"
        p_f.font.name = "Arial"
        p_f.font.size = Pt(10)
        p_f.font.color.rgb = C_MUTED

    def draw_card(slide, left, top, width, height, title="", badge="", body_lines=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_CARD_BG
        shape.line.color.rgb = C_CARD_BORDER
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        first = True
        if badge:
            p = tf.paragraphs[0]
            p.text = badge.upper()
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = C_TEAL
            first = False

        if title:
            p = tf.add_paragraph() if not first else tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.space_after = Pt(4)
            first = False

        if body_lines:
            for line in body_lines:
                p = tf.add_paragraph() if not first else tf.paragraphs[0]
                p.text = line
                p.font.name = "Arial"
                p.font.size = Pt(11)
                p.font.color.rgb = C_TEXT
                p.space_after = Pt(3)
                first = False

    # ==========================================
    # SLIDE 1: TEAM + IDEA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_header(s1, "TEAM + IDEA")

    # Big Orange Title Banner
    banner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.05), Inches(11.733), Inches(0.75))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(255, 247, 237)
    banner.line.color.rgb = RGBColor(253, 186, 116)
    banner.line.width = Pt(1.5)

    tb_b = s1.shapes.add_textbox(Inches(1.0), Inches(2.15), Inches(11.3), Inches(0.55))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "PROJECT TITLE: PhishTrace – AI Email Threat Forensics"
    p_b.font.name = "Arial Black"
    p_b.font.size = Pt(18)
    p_b.font.color.rgb = C_ORANGE

    # Domain & Team Subtitles
    st_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.9), Inches(11.7), Inches(0.7))
    tf_st = st_box.text_frame
    p1 = tf_st.paragraphs[0]
    p1.text = "SELECTED DOMAIN / TRACK: Cybersecurity & AI"
    p1.font.name = "Arial"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = C_TEAL

    p2 = tf_st.add_paragraph()
    p2.text = "TEAM NAME: Team Dark"
    p2.font.name = "Arial Black"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_TITLE

    # Team Members (4 stacked pills)
    members = [
        ("LEAD", "JAYANTH.D", "jayanthedu1116@gmail.com (Full-Stack & Architecture)"),
        ("MEMBER 2", "DHANUSH.R", "Backend Systems, Header Parsers & Forensic Engine"),
        ("MEMBER 3", "VISHAL.R", "AI Training, NVIDIA NIM Integration & LLM Consensus"),
        ("MEMBER 4", "ARPITHA", "Cybersecurity Research, Threat Feeds & RFC 3161 Verification")
    ]

    top_m = 3.7
    for role, name, info in members:
        pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_m), Inches(11.733), Inches(0.6))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CARD_BG
        pill.line.color.rgb = C_CARD_BORDER
        pill.line.width = Pt(1)

        tb_m = s1.shapes.add_textbox(Inches(1.0), Inches(top_m + 0.08), Inches(11.3), Inches(0.45))
        tf_m = tb_m.text_frame
        p = tf_m.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"{role:<12} |  "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_TEAL

        r2 = p.add_run()
        r2.text = f"{name} "
        r2.font.bold = True
        r2.font.size = Pt(12)
        r2.font.color.rgb = C_TITLE

        r3 = p.add_run()
        r3.text = f"—  {info}"
        r3.font.size = Pt(11)
        r3.font.color.rgb = C_MUTED
        top_m += 0.72

    note_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.58), Inches(11.7), Inches(0.35))
    p_n = note_box.text_frame.paragraphs[0]
    p_n.text = "NOTE: ALL TEAM MEMBERS REGISTERED INDIVIDUALLY ON ORGANIZERHQ."
    p_n.font.size = Pt(10)
    p_n.font.bold = True
    p_n.font.color.rgb = C_TEAL

    # ==========================================
    # SLIDE 2: THE PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "THE PROBLEM")

    draw_card(s2, Inches(0.8), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Target Audience",
              body_lines=[
                  "Security Operations Centers (SOC), incident response teams, enterprise fraud departments, financial institutions, and universities.",
                  "Also protects students and non-technical staff targeted by daily phishing campaigns."
              ])

    draw_card(s2, Inches(6.85), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Core Friction",
              body_lines=[
                  "Filters block spam but do not trace attacker origins.",
                  "Header forensics is manual, fragmented, and performed one email at a time.",
                  "Zero existing open-source tools correlate detection, MTA relay origin tracing, campaign clustering, and court-admissible cryptographic evidence."
              ])

    draw_card(s2, Inches(0.8), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="Current Reality",
              body_lines=[
                  "Adversaries leverage generative AI for hyper-personalized social engineering and lookalike domains that cleanly bypass SPF/DKIM filters.",
                  "Investigators waste 20-40 minutes per incident manually inspecting Received headers, IP lookups, and hop timing."
              ])

    draw_card(s2, Inches(6.85), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="Metric / Evidence",
              body_lines=[
                  "FBI IC3 2025: Business Email Compromise (BEC) losses hit $3.05 Billion.",
                  "Phishing remains the #1 most reported cybercrime with 191,000+ complaints.",
                  "Manual triage backlogs leave 80% of reported phishing alerts uninvestigated."
              ])

    # ==========================================
    # SLIDE 3: PROPOSED SOLUTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "PROPOSED SOLUTION")

    # Left Core Concept card
    draw_card(s3, Inches(0.8), Inches(2.1), Inches(4.5), Inches(4.65),
              badge="Core Concept",
              body_lines=[
                  "An open-source, full-stack intelligence platform that detects phishing and BEC, traces probable geographic origin with confidence scores, and links attacks into campaigns with hashed evidence.",
                  "",
                  "KEY CAPABILITIES:",
                  "• Feature 01: Explainable Threat Detection (SPF/DKIM/DMARC auth + NLP heuristics)",
                  "• Feature 02: Origin Relay Tracing + Geo-Confidence Leaflet Map",
                  "• Feature 03: Dynamic Campaign Clustering + Cryptographic SHA-256 PDF Evidence"
              ])

    # Right 3 Workflow pipeline cards
    draw_card(s3, Inches(5.6), Inches(2.1), Inches(2.2), Inches(4.65),
              badge="User Input",
              body_lines=[
                  "• .eml email files",
                  "• Raw RFC 822 headers",
                  "• Plaintext & HTML body",
                  "• Hyperlinks & URLs",
                  "• Attachments",
                  "• Direct Gmail API sync"
              ])

    arrow1 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7.9), Inches(4.3), Inches(0.25), Inches(0.25))
    arrow1.fill.solid()
    arrow1.fill.fore_color.rgb = C_TEAL
    arrow1.line.fill.background()

    draw_card(s3, Inches(8.25), Inches(2.1), Inches(2.2), Inches(4.65),
              badge="Processing Engine",
              body_lines=[
                  "• Deep header parser",
                  "• SPF/DKIM/DMARC checks",
                  "• Hop latency calculation",
                  "• NVIDIA NIM Cloud AI",
                  "• 5-LLM Consensus",
                  "• Campaign similarity graph"
              ])

    arrow2 = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.55), Inches(4.3), Inches(0.25), Inches(0.25))
    arrow2.fill.solid()
    arrow2.fill.fore_color.rgb = C_TEAL
    arrow2.line.fill.background()

    draw_card(s3, Inches(10.9), Inches(2.1), Inches(1.63), Inches(4.65),
              badge="Delivered Outcome",
              body_lines=[
                  "• 0-100 Risk Gauge",
                  "• Hop Leaflet Map",
                  "• AI SOC Co-Pilot",
                  "• Verifiable PDF",
                  "• RFC 3161 hashes"
              ])

    # ==========================================
    # SLIDE 4: OPEN-SOURCE AI APPROACH
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "OPEN-SOURCE AI APPROACH")

    draw_card(s4, Inches(0.8), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Model Selection & Ensemble",
              body_lines=[
                  "• NVIDIA NIM Cloud Accelerator: meta/llama-3.2-11b-vision-instruct",
                  "• 5-Model Multi-LLM Consensus: Llama 3.2, Gemma 2, Mistral, Qwen 2.5, DeepSeek R1",
                  "• Zero-Latency NLP Engine: Deterministic rule and token analysis",
                  "• LightGBM Multi-Signal Classifier for calibrated 0-100 risk scoring."
              ])

    draw_card(s4, Inches(6.85), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Pipeline Role",
              body_lines=[
                  "• Cloud NIM extracts deception intent, urgency indicators, and wire requests.",
                  "• Multi-LLM consensus prevents single-model hallucinations.",
                  "• TF-IDF feature embeddings correlate shared attack infrastructure across campaigns.",
                  "• AI SOC Co-Pilot assists analysts with explainable incident summaries."
              ])

    draw_card(s4, Inches(0.8), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="Technical Rationale",
              body_lines=[
                  "• Sub-350ms response latency with NVIDIA NIM hardware acceleration.",
                  "• 100% offline zero-latency fallback: operates air-gapped without API keys.",
                  "• Open-weight transparency: fully inspectable and auditable reasoning.",
                  "• Zero telemetry leakage: user emails are never stored or fine-tuned upon."
              ])

    draw_card(s4, Inches(6.85), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="External Services / APIs",
              body_lines=[
                  "• NVIDIA NIM Open Inference (integrate.api.nvidia.com)",
                  "• IP-API & DB-IP Lite Geolocation with offline local caching",
                  "• Tor Exit Node, Proxy, and Known Malicious Relay Blocklists",
                  "• RFC 3161 SHA-256 cryptographic chain of custody hashing"
              ])

    # ==========================================
    # SLIDE 5: ONE-DAY BUILD PLAN
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "ONE-DAY BUILD PLAN")

    # Left MVP Card
    draw_card(s5, Inches(0.8), Inches(2.1), Inches(4.5), Inches(3.8),
              badge="Minimum Viable Demo (Built & Ready)",
              body_lines=[
                  "Upload any phishing .eml email file:",
                  "",
                  "✅ 0-100 Risk Score with explainable reasons",
                  "✅ Hop-by-Hop MTA relay geolocation trace map",
                  "✅ 5-Model Open-Source LLM Consensus verdict",
                  "✅ Interactive AI SOC Co-Pilot & prompt sandbox",
                  "✅ Cryptographically hashed, court-ready PDF report"
              ])

    # Right Milestones
    m_data = [
        ("01", "MILESTONE 01 (MORNING) — COMPLETE",
         "FastAPI setup, RFC 822 .eml parser, SPF/DKIM/DMARC checks, IP Geolocation caching, and baseline deterministic threat engine."),
        ("02", "MILESTONE 02 (AFTERNOON) — COMPLETE",
         "Trust-boundary logic, hop latency calculation, NVIDIA NIM integration, multi-model consensus, and SHA-256 evidence vault."),
        ("03", "MILESTONE 03 (EVENING) — COMPLETE",
         "React 18 + Vite dashboard, Leaflet interactive threat map, AI Co-Pilot chat, PDF export, 11/11 automated tests passing, cloud deploy ready.")
    ]

    top_mile = 2.1
    for num, title_m, desc_m in m_data:
        # circle number
        num_c = s5.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.6), Inches(top_mile + 0.1), Inches(0.55), Inches(0.55))
        num_c.fill.solid()
        num_c.fill.fore_color.rgb = C_ORANGE
        num_c.line.fill.background()
        tf_nc = num_c.text_frame
        p_nc = tf_nc.paragraphs[0]
        p_nc.alignment = PP_ALIGN.CENTER
        p_nc.text = num
        p_nc.font.bold = True
        p_nc.font.size = Pt(13)
        p_nc.font.color.rgb = C_WHITE

        # milestone text box
        mb = s5.shapes.add_textbox(Inches(6.3), Inches(top_mile), Inches(6.2), Inches(1.1))
        tf_mb = mb.text_frame
        tf_mb.word_wrap = True
        p_mbt = tf_mb.paragraphs[0]
        p_mbt.text = title_m
        p_mbt.font.name = "Arial"
        p_mbt.font.size = Pt(12)
        p_mbt.font.bold = True
        p_mbt.font.color.rgb = C_TEAL

        p_mbd = tf_mb.add_paragraph()
        p_mbd.text = desc_m
        p_mbd.font.name = "Arial"
        p_mbd.font.size = Pt(10.5)
        p_mbd.font.color.rgb = C_TEXT
        top_mile += 1.25

    # Bottom Feedback Banner
    f_banner = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.75))
    f_banner.fill.solid()
    f_banner.fill.fore_color.rgb = RGBColor(255, 247, 237)
    f_banner.line.color.rgb = RGBColor(253, 186, 116)
    f_banner.line.width = Pt(1.5)

    tb_fb = s5.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_fb = tb_fb.text_frame
    p_fb = tf_fb.paragraphs[0]
    r_fb1 = p_fb.add_run()
    r_fb1.text = "FEEDBACK & VALIDATION:  "
    r_fb1.font.bold = True
    r_fb1.font.size = Pt(11)
    r_fb1.font.color.rgb = C_ORANGE

    r_fb2 = p_fb.add_run()
    r_fb2.text = "Zero-latency fallback guarantees demo reliability without cloud dependencies. Tested on 6 realistic enterprise samples (BEC, Scholarship scam, O365 harvest, malicious macro payload, spoofed MTA relay)."
    r_fb2.font.size = Pt(10.5)
    r_fb2.font.color.rgb = C_TEXT

    # ==========================================
    # SLIDE 6: IMPACT + FEASIBILITY
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "IMPACT + FEASIBILITY")

    draw_card(s6, Inches(0.8), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Measurable Impact",
              body_lines=[
                  "• Benefits enterprise SOC teams, financial fraud units, and student communities.",
                  "• Targets: Precision > 96%, False Positives < 1.5%, Sub-350ms analysis per email.",
                  "• Slashes manual phishing triage time from 30 minutes to under 5 seconds."
              ])

    draw_card(s6, Inches(6.85), Inches(2.1), Inches(5.65), Inches(2.2),
              badge="Ethics & Safety",
              body_lines=[
                  "• Privacy: Ephemeral processing, zero cloud data retention, PII redaction.",
                  "• Guardrails: LLM outputs strictly anchored to RFC 822 cryptographic headers.",
                  "• Confidence Scoring: Objective probabilistic indicators rather than false attribution.",
                  "• Human-in-the-Loop: AI Co-Pilot provides explainable advice; human analyst confirms."
              ])

    draw_card(s6, Inches(0.8), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="Open-Source Contribution",
              body_lines=[
                  "• Public MIT Licensed Repository: github.com/2007JAYANTHYT/PHISHTRACE",
                  "• Fully documented architecture, roadmap, API schemas, and sample attack vectors.",
                  "• 1-click cloud deployment blueprints for Vercel and Render."
              ])

    draw_card(s6, Inches(6.85), Inches(4.55), Inches(5.65), Inches(2.2),
              badge="Technical Risk & Workaround",
              body_lines=[
                  "• Risk: Attack origins disguised behind VPNs, Tor, or commercial webmail relays.",
                  "• Workaround: Proprietary trust-boundary hop subtraction, detecting intermediate relay injection points, and downgrading confidence on known anonymizers."
              ])

    output_path = os.path.abspath("PhishTrace_Hacktoberfest_Team_Dark.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
