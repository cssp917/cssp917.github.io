import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import COPY_RIGHT, TAG_STYLE_MAP, SECTION_COLOR_MAP, get_navbar

# 輸出檔案路徑
FILENAME = "assets/html/course/course_114_CSD.html"

# --- 課程資料來源 ---
COURSE_DATA = {
    "title_zh": "控制系統設計",
    "title_en": "Design and Simulation of Control Systems",
    "semester": "2026 Spring (114學年度下學期)",
    "tag": "電機系",  # 對應 TAG_STYLE_MAP
    "time_loc": "M2W34 @ 工程五館 623 室 (EE623)",
    "prerequisites": "自動控制系統、線性代數、訊號與系統",
    "textbooks": [
        "F. Golnaraghi and B. C. Kuo, <i>Automatic Control Systems</i>, 10th ed. New York, NY: McGraw-Hill Education, 2017.",
        # "C. L. Phillips, H. T. Nagle, and A. Chakrabortty, <i>Digital Control System Analysis and Design</i>, 4th ed., Global Edition. Harlow, UK: Pearson Education Limited, 2015.",
    ],
    "files": [
        # {"title": "課程注意事項 (Course Notice)", "url": "assets/files/ACS_Notice_2018.pdf", "note": "PDF"},
        # {"title": "期末專題分組名單", "url": "assets/files/Group_List.pdf", "note": "12/20"}
    ],
    "resources": [
        {
            "title": "成績查詢(無痕開啟)",
            "url": "https://script.google.com/macros/s/AKfycbxP0Mi77MI6mYSEq_mxDavRtQaMv8tikTPVSC43ep0kzZi5TJ-RIPBVu1qfcAq6tqRV/exec",
            "desc": "Grade Inquiry System",
        },
    ],
    "grading": [
        {"item": "作業 (Homework)", "percent": 20, "note": "兩次(含)沒交和零分者，此部分以零分計"},
        {"item": "第一次期中考 (1st Midterm)", "percent": 25, "note": ""},
        {"item": "第二次期中考 (2nd Midterm)", "percent": 25, "note": ""},
        {"item": "期末考 (Final)", "percent": 30, "note": ""}
    ],
    "office_hours": {"teacher": "Mon. 19:00 - 21:00 at EE773", "ta": "Wed. 19:00 - 21:00 at EE917"},
    "tas": [
        {"name": "李長鑫", "email": "lee313512028.ee13@nycu.edu.tw"},
        {"name": "吳欣諺", "email": "jamiepatty0315@gmail.com"},
    ],
    "ta_office": "工程五館 917 室 (分機 54428)",
    "announcements": [
        {"date": "2026/04/01", "title": "期中考 (1st Midterm Exam)"},
        {"date": "2026/05/06", "title": "期中考 (2nd Midterm Exam)"},
        {"date": "2026/06/10", "title": "期末考 (Final Exam)"},
        {"date": "2026/06/17", "title": "原始成績公布 (Raw Grade Post)"},
        {"date": "2026/06/18", "title": "學期成績公布 (Final Grade Post)"},
    ],
    "homeworks": [
        # {"title": "HW 1", "due": "2024/03/10"},
    ],
    "quizzes": [
        # {"title": "Quiz 1", "date": "2024/03/11"},
    ],
}

# --- 輔助函式 (HTML Generators) ---


def _empty_state(icon: str, msg: str) -> str:
    return f"""
    <div class="empty-state">
        <div class="empty-icon"><i class="{icon}"></i></div>
        <div class="empty-text">{msg}</div>
    </div>
    """


def _render_textbooks(books, color_class="text-dark"):
    if not books:
        return _empty_state("fas fa-book-open", "本學期尚未提供教科書清單。")
    items = "".join(
        [
            f'<li class="list-group-item px-0 border-0 d-flex align-items-start">'
            f'  <i class="fas fa-book-open {color_class} mr-3 mt-1"></i>'
            f'  <div class="text-body">{book}</div>'
            f"</li>"
            for book in books
        ]
    )
    return f'<ul class="list-group list-group-flush">{items}</ul>'


def _render_grading(grading_list, color_class="text-info"):
    if not grading_list:
        return _empty_state("fas fa-tasks", "本學期評分標準尚未公布，請以 E3 公告為準。")

    bg_color = color_class.replace("text-", "bg-")
    html = ""
    for item in grading_list:
        note = item.get("note", "")
        note_html = f'<small class="text-muted d-block mt-2">{note}</small>' if note else ""
        html += f"""
        <div class="grading-item">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="font-weight-bold text-dark">{item['item']}</div>
                <div class="badge badge-soft">{item['percent']}%</div>
            </div>
            <div class="progress progress-thin">
                <div class="progress-bar {bg_color}" role="progressbar"
                     style="width: {item['percent']}%;"
                     aria-valuenow="{item['percent']}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            {note_html}
        </div>
        """
    return html


def _render_tas(tas, office, color_class="text-secondary"):
    if not tas:
        return _empty_state("fas fa-user-friends", "本學期尚未提供助教資訊。")

    ta_cards = ""
    bg_color = color_class.replace("text-", "bg-")
    for ta in tas:
        initial = ta["name"][0] if ta.get("name") else "TA"
        email = ta.get("email", "")
        name = ta.get("name", "TA")
        email_html = (
            f'<a href="mailto:{email}" class="small text-muted text-truncate d-block" title="{email}">{email}</a>'
            if email
            else '<div class="small text-muted">（未提供 Email）</div>'
        )
        ta_cards += f"""
        <div class="col-12 mb-3">
            <div class="ta-card">
                <div class="avatar-circle {bg_color}">{initial}</div>
                <div class="ta-info">
                    <div class="font-weight-bold text-dark">{name}</div>
                    {email_html}
                </div>
            </div>
        </div>
        """
    office_html = f"""
    <div class="d-flex align-items-start mb-3">
        <div class="mr-2 mt-1 text-danger"><i class="fas fa-map-marker-alt"></i></div>
        <div class="small text-muted">{office}</div>
    </div>
    """
    return f"{office_html}<div class='row'>{ta_cards}</div>"


def _render_announcements(news_list, color_class="text-warning"):
    if not news_list:
        return _empty_state("fas fa-bullhorn", "目前尚無公告。")

    html = '<div class="list-group list-group-flush">'
    for news in news_list:
        note = news.get("note")
        note_html = (
            f'<div class="mt-2 small text-muted"><i class="fas fa-info-circle mr-1"></i> {note}</div>' if note else ""
        )
        html += f"""
        <div class="list-group-item px-0 announcement-item">
            <div class="d-flex w-100 justify-content-between align-items-center">
                <div class="d-flex align-items-center" style="min-width: 0;">
                    <span class="bullet {color_class} mr-2"></span>
                    <h5 class="mb-0 text-dark text-truncate" style="font-size: 1.05rem;">{news['title']}</h5>
                </div>
                <span class="badge badge-light border flex-shrink-0 ml-3">{news['date']}</span>
            </div>
            {note_html}
        </div>
        """
    html += "</div>"
    return html


def _render_grid_items(items, icon_name, color_class="text-primary"):
    if not items:
        return """
        <div class="alert alert-light border-0 mb-0" style="background: rgba(255,255,255,0.6);">
            <div class="d-flex align-items-start">
                <div class="mr-3 text-muted"><i class="fas fa-info-circle"></i></div>
                <div class="text-muted">
                    本學年暫無詳細列表。請參考
                    <a href="https://e3.nycu.edu.tw" target="_blank">E3 平台</a>
                    取得最新的作業與小考資訊。
                </div>
            </div>
        </div>
        """

    content = ""
    for item in items:
        badge_text = item.get("due") or item.get("date") or ""
        note_text = item.get("note")
        note_html = (
            f'<div class="mt-2 small text-muted"><i class="fas fa-info-circle mr-1"></i> {note_text}</div>'
            if note_text
            else ""
        )
        content += f"""
        <div class="grid-item">
            <div class="d-flex justify-content-between align-items-center">
                <div class="text-truncate pr-2">
                    <i class="{icon_name} {color_class} mr-2"></i>
                    <span class="text-dark" style="font-weight: 600;">{item['title']}</span>
                </div>
                <span class="badge badge-light border text-muted badge-pill flex-shrink-0">{badge_text}</span>
            </div>
            {note_html}
        </div>
        """
    return f'<div class="multi-column-container">{content}</div>'


def _render_resources(files, links, color_class="text-danger"):
    has_files = bool(files)
    has_links = bool(links)

    if not has_files and not has_links:
        return ""

    content = ""

    if has_files:
        for f in files:
            icon = "fa-file-pdf" if f.get("url", "").lower().endswith(".pdf") else "fa-file-alt"
            note = f.get("note")
            note_html = f'<span class="badge badge-light border ml-2">{note}</span>' if note else ""
            content += f"""
            <a href="{f['url']}" class="resource-item d-flex justify-content-between align-items-center">
                <div class="text-truncate">
                    <i class="fas {icon} {color_class} mr-2 fixed-width-icon"></i>
                    <span class="resource-title">{f['title']}</span>
                </div>
                {note_html}
            </a>
            """

    if has_links:
        if has_files:
            content += '<div class="divider-dashed"></div>'

        for res in links:
            desc = res.get("desc", "")
            desc_html = f'<span class="text-muted small ml-2 d-none d-sm-inline">— {desc}</span>' if desc else ""
            content += f"""
            <a href="{res['url']}" target="_blank" class="resource-item d-flex justify-content-between align-items-center">
                <div class="text-truncate" style="max-width: 92%;">
                    <i class="fas fa-external-link-alt {color_class} mr-2 fixed-width-icon"></i>
                    <span class="resource-title link-title">{res['title']}</span>
                    {desc_html}
                </div>
                <i class="fas fa-chevron-right text-muted small"></i>
            </a>
            """

    return f"""
    <section class="section-box">
        <div class="section-head">
            <div class="section-icon"><i class="fas fa-link"></i></div>
            <h4 class="mb-0">相關資源 (Resources)</h4>
        </div>
        <div class="resource-list">{content}</div>
    </section>
    """


# --- 主程式邏輯 (HTML 組合) ---


def get_course_acs_html():
    # 1) Navbar
    navbar = get_navbar(is_course_page=True, course_title=COURSE_DATA["title_en"])

    # 2) Tag style
    tag_class = TAG_STYLE_MAP.get(COURSE_DATA["tag"], "badge-secondary")
    accent_class = tag_class.replace("badge-", "bg-")

    # 3) Header / Hero
    header_html = f"""
    <header class="hero">
        <div class="hero-bg"></div>
        <div class="container hero-inner">
            <div class="d-flex flex-wrap align-items-center mb-3">
                <div class="hero-kicker">{COURSE_DATA['semester']}</div>
                <span class="badge {tag_class} hero-tag ml-2">{COURSE_DATA['tag']}</span>
            </div>

            <div class="hero-title">{COURSE_DATA['title_zh']}</div>
            <div class="hero-subtitle">{COURSE_DATA['title_en']}</div>

            <div class="hero-divider {accent_class}"></div>

            <div class="row hero-meta">
                <div class="col-md-6 mb-2 mb-md-0">
                    <div class="meta-item">
                        <div class="meta-ic"><i class="fas fa-clock"></i></div>
                        <div class="meta-txt"><strong>時間地點：</strong> {COURSE_DATA['time_loc']}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-ic"><i class="fas fa-book"></i></div>
                        <div class="meta-txt"><strong>先修課程：</strong> {COURSE_DATA['prerequisites']}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="meta-item">
                        <div class="meta-ic"><i class="fas fa-chalkboard-teacher"></i></div>
                        <div class="meta-txt"><strong>教師 Office Hour：</strong> {COURSE_DATA['office_hours']['teacher']}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-ic"><i class="fas fa-user-friends"></i></div>
                        <div class="meta-txt"><strong>助教 Office Hour：</strong> {COURSE_DATA['office_hours']['ta']}</div>
                    </div>
                </div>
            </div>
        </div>
    </header>
    """

    # 4) Sections content
    HEADER_ICON_STYLE = "text-secondary"

    announcements_html = _render_announcements(COURSE_DATA["announcements"], SECTION_COLOR_MAP["announcement"])
    homework_html = _render_grid_items(COURSE_DATA["homeworks"], "fas fa-file-alt", SECTION_COLOR_MAP["homework"])
    quiz_html = _render_grid_items(COURSE_DATA["quizzes"], "fas fa-pen-square", SECTION_COLOR_MAP["quiz"])
    textbooks_html = _render_textbooks(COURSE_DATA["textbooks"], SECTION_COLOR_MAP["textbook"])
    grading_html = _render_grading(COURSE_DATA["grading"], SECTION_COLOR_MAP["grading"])
    tas_html = _render_tas(COURSE_DATA["tas"], COURSE_DATA["ta_office"], SECTION_COLOR_MAP["ta"])
    resources_section = _render_resources(
        COURSE_DATA.get("files"), COURSE_DATA.get("resources"), SECTION_COLOR_MAP["resource"]
    )

    # 5) Final HTML
    full_html = f"""
    <!doctype html>
    <html lang="zh-TW">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>{COURSE_DATA['title_en']} - CSSP Lab</title>

      <!-- Icons + Bootstrap 4 -->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;600;700&display=swap" rel="stylesheet">

      <style>
        :root {{
            --bg: #0b1220;
            --panel: rgba(255, 255, 255, 0.86);
            --panel-solid: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --line: rgba(15, 23, 42, 0.08);
            --shadow: 0 10px 30px rgba(2, 6, 23, 0.12);
            --shadow-soft: 0 6px 18px rgba(2, 6, 23, 0.10);
            --r: 16px;
        }}

        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            color: var(--text);
            background:
                radial-gradient(1000px 600px at 10% -10%, rgba(59, 130, 246, 0.25), transparent 60%),
                radial-gradient(900px 600px at 90% 0%, rgba(168, 85, 247, 0.22), transparent 60%),
                radial-gradient(1100px 700px at 50% 120%, rgba(16, 185, 129, 0.18), transparent 55%),
                #f6f7fb;
        }}

        /* --- Navbar：維持原本「小螢幕也展開」邏輯，但讓視覺更乾淨 --- */
        .navbar {{
            backdrop-filter: blur(12px);
            background: rgba(255,255,255,0.75) !important;
            border-bottom: 1px solid rgba(0,0,0,0.06);
        }}
        .navbar-toggler {{ display: none !important; }}
        .navbar-collapse {{ display: flex !important; flex-basis: auto; }}
        .navbar-nav {{ flex-direction: row; }}

        /* --- Hero --- */
        .hero {{
            position: relative;
            padding-top: 92px; /* 預留 navbar */
            padding-bottom: 28px;
        }}
        .hero-bg {{
            position: absolute;
            inset: 0;
            background:
                radial-gradient(1000px 520px at 10% 10%, rgba(59, 130, 246, 0.35), transparent 60%),
                radial-gradient(900px 520px at 85% 10%, rgba(168, 85, 247, 0.28), transparent 60%),
                linear-gradient(180deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
            pointer-events: none;
        }}
        .hero-inner {{
            position: relative;
            padding: 26px 0 10px 0;
        }}
        .hero-kicker {{
            font-size: 0.82rem;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: rgba(15, 23, 42, 0.55);
            font-weight: 600;
        }}
        .hero-tag {{
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
        }}
        .hero-title {{
            font-weight: 800;
            font-size: 2.4rem;
            line-height: 1.15;
            color: #0b1220;
            margin-top: 6px;
        }}
        .hero-subtitle {{
            font-weight: 500;
            font-size: 1.15rem;
            color: rgba(15, 23, 42, 0.68);
            margin-top: 8px;
        }}
        .hero-divider {{
            width: 56px;
            height: 4px;
            border-radius: 999px;
            margin: 18px 0 18px 0;
        }}
        .hero-meta .meta-item {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin: 10px 0;
        }}
        .hero-meta .meta-ic {{
            width: 34px;
            height: 34px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 6px 14px rgba(2,6,23,0.08);
            color: rgba(15, 23, 42, 0.72);
            flex-shrink: 0;
        }}
        .hero-meta .meta-txt {{
            color: rgba(15, 23, 42, 0.72);
        }}

        /* --- Cards / Sections --- */
        .section-box {{
            background: var(--panel);
            border: 1px solid rgba(255,255,255,0.55);
            box-shadow: var(--shadow-soft);
            border-radius: var(--r);
            padding: 26px;
            margin-bottom: 22px;
        }}
        .section-head {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
        }}
        .section-icon {{
            width: 36px;
            height: 36px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(15, 23, 42, 0.06);
            color: rgba(15, 23, 42, 0.75);
        }}
        h4 {{
            font-weight: 800;
            font-size: 1.15rem;
            margin: 0;
            color: #0f172a;
        }}

        /* --- List interactions --- */
        .list-group-item-action:hover {{
            background-color: rgba(2, 6, 23, 0.02);
            color: #0b5ed7;
        }}

        /* --- Announcement --- */
        .announcement-item {{
            border: 0 !important;
            background: transparent;
        }}
        .bullet {{
            width: 10px;
            height: 10px;
            border-radius: 999px;
            display: inline-block;
            background: #f59e0b; /* fallback */
        }}
        .text-warning.bullet {{ background: #f59e0b; }}
        .text-info.bullet {{ background: #0ea5e9; }}
        .text-primary.bullet {{ background: #3b82f6; }}
        .text-danger.bullet {{ background: #ef4444; }}
        .text-success.bullet {{ background: #10b981; }}

        /* --- Multi-column homework/quiz --- */
        .multi-column-container {{
            column-count: 2;
            column-gap: 1.6rem;
        }}
        .grid-item {{
            break-inside: avoid;
            page-break-inside: avoid;
            padding: 14px 0;
            border-bottom: 1px solid var(--line);
        }}
        .grid-item:last-child {{ border-bottom: 0; }}
        @media (max-width: 768px) {{
            .multi-column-container {{ column-count: 1; }}
            .hero-title {{ font-size: 2.0rem; }}
        }}

        /* --- Grading --- */
        .grading-item {{
            padding: 14px 0;
            border-bottom: 1px solid var(--line);
        }}
        .grading-item:last-child {{ border-bottom: 0; }}
        .progress-thin {{
            height: 10px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.07);
        }}
        .progress-thin .progress-bar {{
            border-radius: 999px;
        }}
        .badge-soft {{
            background: rgba(15, 23, 42, 0.06);
            border: 1px solid rgba(15, 23, 42, 0.06);
            color: rgba(15, 23, 42, 0.78);
            font-weight: 700;
            padding: 0.35rem 0.55rem;
            border-radius: 999px;
        }}

        /* --- TA cards --- */
        .ta-card {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,0.78);
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: 0 10px 20px rgba(2,6,23,0.06);
        }}
        .avatar-circle {{
            width: 42px; height: 42px;
            color: #fff;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 1.05rem;
            flex-shrink: 0;
            box-shadow: 0 6px 14px rgba(2,6,23,0.15);
        }}
        .ta-info {{
            min-width: 0;
        }}

        /* --- Resources --- */
        .resource-list {{
            border-radius: 14px;
            overflow: hidden;
        }}
        .resource-item {{
            padding: 12px 0;
            border-bottom: 1px solid var(--line);
            text-decoration: none !important;
        }}
        .resource-item:hover .resource-title {{
            text-decoration: underline;
        }}
        .resource-item:last-child {{ border-bottom: 0; }}
        .resource-title {{
            font-weight: 650;
            color: #0f172a;
        }}
        .link-title {{
            color: #0b5ed7;
        }}
        .divider-dashed {{
            width: 100%;
            margin: 10px 0 8px 0;
            border-top: 1px dashed rgba(15, 23, 42, 0.18);
        }}
        .fixed-width-icon {{ width: 22px; text-align: center; }}

        /* --- Empty State --- */
        .empty-state {{
            border: 1px dashed rgba(15, 23, 42, 0.18);
            border-radius: 14px;
            padding: 16px;
            background: rgba(255,255,255,0.55);
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }}
        .empty-icon {{
            width: 38px;
            height: 38px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(15, 23, 42, 0.06);
            color: rgba(15, 23, 42, 0.7);
            flex-shrink: 0;
        }}
        .empty-text {{
            color: rgba(15, 23, 42, 0.65);
            font-weight: 600;
        }}

        /* --- Sidebar sticky (大螢幕更好用) --- */
        @media (min-width: 992px) {{
            .sidebar-sticky {{
                position: sticky;
                top: 92px;
            }}
        }}

        /* --- Footer --- */
        footer {{
            color: rgba(15, 23, 42, 0.6);
        }}
      </style>
    </head>
    <body>

      {navbar}
      {header_html}

      <div class="container" style="margin-bottom: 48px;">
        <div class="row">
            <main class="col-lg-8">

                <section class="section-box">
                    <div class="section-head">
                        <div class="section-icon"><i class="fas fa-bullhorn"></i></div>
                        <h4>公告 (Announcement)</h4>
                    </div>
                    {announcements_html}
                </section>

                <section class="section-box">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="section-head mb-0">
                            <div class="section-icon"><i class="fas fa-pencil-alt"></i></div>
                            <h4>作業 (Homework)</h4>
                        </div>
                        <span class="badge badge-soft">{len(COURSE_DATA['homeworks'])} assignments</span>
                    </div>
                    {homework_html}
                </section>

                <section class="section-box">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="section-head mb-0">
                            <div class="section-icon"><i class="fas fa-clipboard-list"></i></div>
                            <h4>小考 (Quiz)</h4>
                        </div>
                        <span class="badge badge-soft">{len(COURSE_DATA['quizzes'])} quizzes</span>
                    </div>
                    {quiz_html}
                </section>

                <section class="section-box">
                    <div class="section-head">
                        <div class="section-icon"><i class="fas fa-book"></i></div>
                        <h4>教科書 (Textbook)</h4>
                    </div>
                    {textbooks_html}
                </section>

            </main>

            <aside class="col-lg-4">
                <div class="sidebar-sticky">
                    <section class="section-box">
                        <div class="section-head">
                            <div class="section-icon"><i class="fas fa-tasks"></i></div>
                            <h4>評分標準 (Grading)</h4>
                        </div>
                        {grading_html}
                    </section>

                    <section class="section-box">
                        <div class="section-head">
                            <div class="section-icon"><i class="fas fa-users"></i></div>
                            <h4>課程助教 (TA)</h4>
                        </div>
                        {tas_html}
                    </section>

                    {resources_section}
                </div>
            </aside>
        </div>
      </div>

      <footer class="text-center py-5" style="border-top:1px solid rgba(15, 23, 42, 0.08);">
          <div class="mb-3">
              <img src="../../brand/logo.jpg" alt="Lab Logo" style="height: 56px; width: auto; opacity: 0.92;">
          </div>
          {COPY_RIGHT}
      </footer>

      <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

    </body>
    </html>
    """
    return full_html


def write_course_acs_html(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    s = get_course_acs_html()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"Successfully generated {filename}.")


if __name__ == "__main__":
    write_course_acs_html(filename=FILENAME)
