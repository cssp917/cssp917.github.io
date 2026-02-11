import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from config import COPY_RIGHT, TAG_STYLE_MAP, SECTION_COLOR_MAP, get_navbar

# 輸出檔案路徑
FILENAME = 'assets/html/course/course_114_ACS.html'

# --- 課程資料來源 ---
# 包含課程的所有資訊，結構類似 JSON，方便日後替換成資料庫讀取
COURSE_DATA = {
    "title_zh": "自動控制系統",
    "title_en": "Automatic Control Systems",
    "semester": "2025 Fall (114學年度上學期)",
    "tag": "電機系", # 對應 TAG_STYLE_MAP
    "time_loc": "M2W34 @ 工程五館 623 室 (EE623)",
    "prerequisites": "訊號與系統、線性代數",
    "textbooks": [
        "F. Golnaraghi and B. C. Kuo, <i>Automatic Control Systems</i>, 10th ed. New York, NY: McGraw-Hill Education, 2017."
    ],
    "files": [ # 供下載的檔案列表
        # {"title": "課程注意事項 (Course Notice)", "url": "assets/files/ACS_Notice_2018.pdf", "note": "PDF"},
        # {"title": "期末專題分組名單", "url": "assets/files/Group_List.pdf", "note": "12/20"}
    ],
    "resources": [ # 外部連結列表
        # {"title": "成績查詢與解答系統", "url": "https://script.google.com/macros/s/AKfycbxP0Mi77MI6mYSEq_mxDavRtQaMv8tikTPVSC43ep0kzZi5TJ-RIPBVu1qfcAq6tqRV/exec", "desc": "Grade Inquiry System"},
    ],
    "grading": [ # 評分標準與權重
        {"item": "作業 (Homework)", "percent": 10, "note": "兩次(含)零分，此部分以零分計"},
        {"item": "小考 (Quiz)", "percent": 40, "note": "兩次(含)零分，此部分以零分計"},
        {"item": "期中考 (Midterm)", "percent": 25, "note": ""},
        {"item": "期末考 (Final)", "percent": 25, "note": ""}
    ],
    "office_hours": {
        "teacher": "Mon. 19:00 - 21:00 at EE773",
        "ta": "Thu. 18:00 - 20:00 at EE917"
    },
    "tas": [ # 助教名單
        {"name": "林芝嫻", "email": "jslin.ee13@nycu.edu.tw"},
        {"name": "吳沛熏", "email": "wu2001.en13@nycu.edu.tw"},
        {"name": "林宗佑", "email": "yoyo010528@gmail.com"}
    ],
    "ta_office": "工程五館 917 室 (分機 54428)",
    "announcements": [ # 公告內容
        {"date": "2025/10/29", "title": "期中考 (Midterm Exam)"},
        {"date": "2025/12/24", "title": "期末考 (Final Exam)"},
        {"date": "2025/12/30", "title": "原始成績公佈 (Raw Grade Post)"},
        {"date": "2025/12/31", "title": "學期成績公佈 (Final Grade Post)"},
    ],
    "homeworks": [ # 作業列表
        {"title": "HW 1", "due": "2025/10/15"},
        {"title": "HW 2", "due": "2025/10/22"},
        {"title": "HW 3", "due": "2025/11/03"},
        {"title": "HW 4", "due": "2025/11/12"},
        {"title": "HW 5", "due": "2025/12/03"},
    ],
    "quizzes": [ # 小考列表
        {"title": "Quiz 1", "date": "2025/09/17"},
        {"title": "Quiz 2", "date": "2025/09/22"},
        {"title": "Quiz 3", "date": "2025/10/08"},
        {"title": "Quiz 4", "date": "2025/10/15"},
        {"title": "Quiz 5", "date": "2025/11/05"},
        {"title": "Quiz 6", "date": "2025/11/12"},
        {"title": "Quiz 7", "date": "2025/11/19"},
        {"title": "Quiz 8", "date": "2025/12/01"},
        {"title": "Quiz 9", "date": "2025/12/03"},    
        {"title": "Quiz 10", "date": "2025/12/10"},    
    ]
}

# --- 輔助函式 (HTML Generators) ---

def _render_textbooks(books, color_class="text-dark"):
    """
    生成教科書列表 HTML
    """
    items = "".join([
        f'<li class="list-group-item px-0 border-0"><i class="fas fa-book-open {color_class} mr-2"></i> {book}</li>'
        for book in books
    ])
    return f'<ul class="list-group list-group-flush">{items}</ul>'

def _render_grading(grading_list, color_class="text-info"):
    """
    生成評分標準 HTML
    包含：項目名稱、百分比數值、視覺化進度條 (Progress Bar) 以及備註
    """
    # 將文字顏色轉換為背景顏色 class (例: text-info -> bg-info) 用於進度條
    bg_color = color_class.replace("text-", "bg-")
    html = ""
    for item in grading_list:
        html += f"""
        <div class="mb-3">
            <div class="d-flex justify-content-between mb-1">
                <span class="font-weight-bold">{item['item']}</span>
                <span class="font-weight-bold">{item['percent']}%</span>
            </div>
            <div class="progress" style="height: 8px; border-radius: 4px;">
                <div class="progress-bar {bg_color}" role="progressbar" style="width: {item['percent']}%;" 
                     aria-valuenow="{item['percent']}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <small class="text-muted">{item['note']}</small>
        </div>
        """
    return html

def _render_tas(tas, office, color_class="text-secondary"):
    """
    生成助教資訊 HTML
    包含：辦公室地點資訊、助教卡片 (顯示姓名首字圓形頭像、姓名、Email)
    """
    ta_cards = ""
    bg_color = color_class.replace("text-", "bg-")
    for ta in tas:
        # 取得姓名第一個字作為頭像文字
        initial = ta['name'][0] if ta['name'] else "TA"
        ta_cards += f"""
        <div class="col-12 mb-2">
            <div class="media p-2 rounded bg-light border align-items-center" style="height: 100%;">
                <div class="avatar-circle {bg_color} mr-3">{initial}</div>
                <div class="media-body text-truncate" style="min-width: 0;">
                    <h6 class="mt-0 mb-0 font-weight-bold text-dark">{ta['name']}</h6>
                    <a href="mailto:{ta['email']}" class="small text-muted text-truncate d-block" title="{ta['email']}">{ta['email']}</a>
                </div>
            </div>
        </div>
        """
    return f'<p class="mb-3 small text-muted"><i class="fas fa-map-marker-alt text-danger mr-2"></i> {office}</p><div class="row">{ta_cards}</div>'

def _render_announcements(news_list, color_class="text-warning"):
    """
    生成公告列表 HTML
    包含：標題 (帶顏色箭頭)、日期 Badge、備註
    """
    html = '<div class="list-group list-group-flush">'
    for news in news_list:
        # 若有備註則顯示，否則為空字串
        note_html = f'<div class="mt-1 small text-muted"><i class="fas fa-info-circle mr-1"></i> {news["note"]}</div>' if "note" in news else ""
        html += f"""
        <div class="list-group-item px-0">
            <div class="d-flex w-100 justify-content-between align-items-center">
                <h5 class="mb-1 text-dark" style="font-size: 1.05rem;"><i class="fas fa-caret-right {color_class} mr-2"></i>{news['title']}</h5>
                <span class="badge badge-light border">{news['date']}</span>
            </div>
            {note_html}
        </div>
        """
    html += '</div>'
    return html

def _render_grid_items(items, icon_name, color_class="text-primary"):
    """
    生成多欄位列表 HTML (用於作業與小考)
    1. 讀取 items 中的 due 或 date
    2. 若 items 為空，顯示 E3 連結
    """
    if not items:
        return '<p class="text-muted"><i class="fas fa-info-circle mr-2"></i>本學年暫無詳細列表。請參考 <a href="https://e3.nycu.edu.tw" target="_blank">E3 平台</a>取得最新的作業與小考資訊。</p>'
    
    content = ""
    for item in items:
        # 直接讀取資料中的日期，不依賴外部傳入的預設文字
        badge_text = item.get('due') or item.get('date') or ""
        
        # 若有備註則顯示，否則為空字串
        note_text = item.get('note')
        note_html = f'<div class="mt-1 small text-muted"><i class="fas fa-info-circle mr-1"></i> {note_text}</div>' if note_text else ""

        content += f"""
        <div class="grid-item py-2 border-bottom">
            <div class="d-flex justify-content-between align-items-center">
                <span class="text-truncate pr-2">
                    <i class="{icon_name} {color_class} mr-2"></i> {item['title']}
                </span>
                <span class="badge badge-light border text-muted badge-pill flex-shrink-0" style="font-size: 0.75rem;">{badge_text}</span>
            </div>
            {note_html}
        </div>
        """
    return f'<div class="multi-column-container">{content}</div>'

def _render_resources(files, links, color_class="text-danger"):
    """
    生成資源區塊 HTML
    整合了「檔案下載」與「外部連結」兩個部分，中間以虛線分隔
    """
    content = ""
    # 處理檔案下載部分
    if files:
        for f in files:
            # 根據副檔名判斷圖示 (PDF 或一般檔案)
            icon = "fa-file-pdf" if f['url'].endswith('.pdf') else "fa-file-alt"
            note = f'<span class="badge badge-light border ml-2">{f["note"]}</span>' if "note" in f else ""
            content += f"""
            <a href="{f['url']}" class="list-group-item list-group-item-action border-0 px-0 d-flex justify-content-between align-items-center">
                <div class="text-truncate">
                    <i class="fas {icon} {color_class} mr-2 fixed-width-icon"></i>
                    <span style="font-weight: 500; color: #333;">{f['title']}</span>
                </div>
                {note}
            </a>
            """
    
    # 若同時有檔案和連結，加入分隔線
    if links:
        if files: 
            content += '<div class="w-100 my-2" style="border-top: 1px dashed #e0e0e0;"></div>'
        # 處理外部連結部分
        for res in links:
            content += f"""
            <a href="{res['url']}" target="_blank" class="list-group-item list-group-item-action border-0 px-0 d-flex justify-content-between align-items-center">
                <div class="text-truncate" style="max-width: 90%;">
                    <i class="fas fa-external-link-alt {color_class} mr-2 fixed-width-icon"></i>
                    <span style="font-weight: 500; color: #0056b3;">{res['title']}</span>
                    <span class="text-muted small ml-1 d-none d-sm-inline">- {res['desc']}</span>
                </div>
                <i class="fas fa-chevron-right text-muted small"></i>
            </a>
            """
    
    if not content: return ""
    
    return f"""
    <section class="section-box">
        <h4><i class="fas fa-link text-secondary mr-2"></i> 相關資源 (Resources)</h4>
        <div class="list-group list-group-flush">{content}</div>
    </section>
    """

# --- 主程式邏輯 (HTML 組合) ---

def get_course_acs_html():
    """
    組裝完整的 HTML 字串
    """
    # 1. 取得導航列
    navbar = get_navbar(is_course_page=True, course_title=COURSE_DATA['title_en'])
    
    # 2. 取得課程標籤樣式
    tag_class = TAG_STYLE_MAP.get(COURSE_DATA['tag'], "badge-secondary")
    hr_class = tag_class.replace("badge-", "bg-")

    # 3. 建立頁首 (Jumbotron)
    # 包含課程名稱、時間、地點、先修課程等資訊
    header_html = f"""
    <div class="jumbotron jumbotron-fluid bg-light" style="margin-top: 60px; padding: 3rem 0; border-bottom: 1px solid #e9ecef;">
        <div class="container">
            <div class="d-flex align-items-center mb-2">
                <h6 class="text-muted text-uppercase mb-0 mr-3" style="letter-spacing: 1px;">{COURSE_DATA['semester']}</h6>
                <span class="badge {tag_class}">{COURSE_DATA['tag']}</span>
            </div>
            <h1 class="display-4" style="font-weight: 700; color: #000;">{COURSE_DATA['title_zh']}</h1>
            <h3 style="font-weight: 300; color: #555;">{COURSE_DATA['title_en']}</h3>
            <hr class="my-4 {hr_class}" style="height: 2px; border: 0; width: 50px; margin-left: 0;">
            <div class="row text-secondary">
                <div class="col-md-6">
                    <p><i class="fas fa-clock mr-2 text-dark"></i> <strong>時間地點：</strong> {COURSE_DATA['time_loc']}</p>
                    <p><i class="fas fa-book mr-2 text-dark"></i> <strong>先修課程：</strong> {COURSE_DATA['prerequisites']}</p>
                </div>
                <div class="col-md-6">
                    <p><i class="fas fa-chalkboard-teacher mr-2 text-dark"></i> <strong>教師 Office Hour：</strong> {COURSE_DATA['office_hours']['teacher']}</p>
                    <p><i class="fas fa-user-friends mr-2 text-dark"></i> <strong>助教 Office Hour：</strong> {COURSE_DATA['office_hours']['ta']}</p>
                </div>
            </div>
        </div>
    </div>
    """

    # 設定區塊標題 icon 的統一顏色 (灰色)
    HEADER_ICON_STYLE = "text-secondary"

    # 4. 呼叫輔助函式生成各區塊內容
    # 傳入對應的資料與顏色設定
    announcements_html = _render_announcements(COURSE_DATA['announcements'], SECTION_COLOR_MAP['announcement'])
    homework_html = _render_grid_items(COURSE_DATA['homeworks'], "fas fa-file-alt", SECTION_COLOR_MAP['homework'])
    quiz_html = _render_grid_items(COURSE_DATA['quizzes'], "fas fa-pen-square", SECTION_COLOR_MAP['quiz'])
    textbooks_html = _render_textbooks(COURSE_DATA['textbooks'], SECTION_COLOR_MAP['textbook'])
    grading_html = _render_grading(COURSE_DATA['grading'], SECTION_COLOR_MAP['grading'])
    tas_html = _render_tas(COURSE_DATA['tas'], COURSE_DATA['ta_office'], SECTION_COLOR_MAP['ta'])
    
    # 資源區塊 (標題顏色在函式內部定義，內容使用紅色系)
    resources_section = _render_resources(COURSE_DATA.get('files'), COURSE_DATA.get('resources'), SECTION_COLOR_MAP['resource'])

    # 5. 組合最終 HTML
    # 包含 Head, CSS Styles, Body 結構 (主要內容區 col-lg-8 與 側邊欄 col-lg-4), Scripts
    full_html = f"""
    <!doctype html>
    <html lang="zh-TW">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>{COURSE_DATA['title_en']} - CSSP Lab</title>
      
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
      
      <style>
        /* 全域字體與背景設定 */
        body {{ font-family: 'Inter', 'Noto Sans TC', sans-serif; color: #333; background-color: #f4f5f7; }}
        h4 {{ font-weight: 700; font-size: 1.25rem; margin-bottom: 20px; color: #222; }}
        
        /* Navbar 客製化：強制在小螢幕也展開選單項目，隱藏漢堡選單 */
        .navbar-toggler {{ display: none !important; }}
        .navbar-collapse {{ display: flex !important; flex-basis: auto; }}
        .navbar-nav {{ flex-direction: row; }}
        
        /* 白色內容卡片樣式 */
        .section-box {{ 
            background: #fff; 
            padding: 30px; 
            border-radius: 8px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.03); 
            margin-bottom: 30px; 
            border: 1px solid #eaeaea; 
        }}
        
        /* 列表互動效果 */
        .list-group-item-action:hover {{ background-color: #f8f9fa; color: #0056b3; }}
        
        /* 多欄位排版 (Masonry-like) 用於作業與小考 */
        .multi-column-container {{ column-count: 2; column-gap: 2rem; }}
        .grid-item {{ break-inside: avoid; page-break-inside: avoid; }}
        @media (max-width: 768px) {{ .multi-column-container {{ column-count: 1; }} }}
        
        /* 助教頭像樣式 */
        .avatar-circle {{
            width: 42px; height: 42px;
            color: #fff;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 600; font-size: 1.1rem;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .fixed-width-icon {{ width: 24px; text-align: center; }}
        @media (max-width: 576px) {{ .navbar-brand {{ font-size: 1rem; margin-right: 0; }} }}
      </style>
    </head>
    <body class="bg-light">
      
      {navbar}
      {header_html}
      
      <div class="container" style="margin-bottom: 50px;">
        <div class="row">
            <main class="col-lg-8">
                <section class="section-box">
                    <h4><i class="fas fa-bullhorn {HEADER_ICON_STYLE} mr-2"></i> 公告 (Announcement)</h4>
                    {announcements_html}
                </section>

                <section class="section-box">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="mb-0"><i class="fas fa-pencil-alt {HEADER_ICON_STYLE} mr-2"></i> 作業 (Homework)</h4>
                        <span class="badge badge-light border">{len(COURSE_DATA['homeworks'])} assignments</span>
                    </div>
                    {homework_html}
                </section>

                <section class="section-box">
                      <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="mb-0"><i class="fas fa-clipboard-list {HEADER_ICON_STYLE} mr-2"></i> 小考 (Quiz)</h4>
                        <span class="badge badge-light border">{len(COURSE_DATA['quizzes'])} quizzes</span>
                    </div>
                    {quiz_html}
                </section>
                
                <section class="section-box">
                    <h4><i class="fas fa-book {HEADER_ICON_STYLE} mr-2"></i> 教科書 (Textbook)</h4>
                    {textbooks_html}
                </section>
            </main>
            
            <aside class="col-lg-4">
                <section class="section-box">
                    <h4><i class="fas fa-tasks {HEADER_ICON_STYLE} mr-2"></i> 評分標準 (Grading)</h4>
                    {grading_html}
                </section>
                
                <section class="section-box">
                    <h4><i class="fas fa-users {HEADER_ICON_STYLE} mr-2"></i> 課程助教 (TA)</h4>
                    {tas_html}
                </section>

                {resources_section}
            </aside>
        </div>
      </div>

      <footer class="text-center py-5 text-muted" style="border-top:1px solid #eee;">
          <div class="mb-3">
              <img src="../../brand/logo.jpg" alt="Lab Logo" style="height: 60px; width: auto; opacity: 0.9;">
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
    """
    將生成的 HTML 寫入檔案
    """
    # 確保目標資料夾存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    s = get_course_acs_html()
    
    # 寫入檔案，指定 utf-8 編碼
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'Successfully generated {filename}.')

if __name__ == '__main__':
    write_course_acs_html(filename=FILENAME)
