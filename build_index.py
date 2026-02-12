import uuid
import sys
from pybtex.database.input import bibtex
from cssp.course_data import COURSES_DATA
from cssp.config import COPY_RIGHT, TAG_STYLE_MAP, MEMBER_TAG_MAP

# ==========================================
#  全域設定與靜態資料 (Configuration)
#  說明：此區塊存放網頁的靜態內容，如標題、輪播圖片連結、外部連結等。
#  若只需修改文字或圖片，通常在此區塊調整即可。
# ==========================================

LAB_INFO = {
    "title_en": "CSSP Lab",
    "subtitle_en": "Chaotic Systems and Signal Processing",
    "title_zh": "國立陽明交通大學 混沌系統與信號處理實驗室",
    "email": "csspcssp917ap@gmail.com",
    "copyright": f"{COPY_RIGHT}",
    # 定義各頁面所需的 .bib 資料來源路徑
    "files": {
        "members": "cssp/members_list.bib", 
        "gar_members": "cssp/gar_members_list.bib", 
        "gallery": "cssp/gallery_list.bib",
        "publications": "cssp/publications_list.bib",
        "media": "cssp/media_list.bib"
    },
    # 首頁關於實驗室的詳細介紹文字 (支援 HTML 標籤如 <br>)
    "TL;DR":"""本實驗室致力於影像辨識、智慧型控制、智慧型運輸系統(ITS)及非接觸式生理訊號監測與應用的研究。
    電機工程學是應用科學，將學術研究成果，轉化為改進社會生活品質與提昇台灣產業技術，希望做對社會有貢獻(Society Contribution Index, SCI)的研究。
    <br>
    2002年起開發台灣第一輛實際上路經驗的自動駕駛的智慧車，讓台灣擠身國際智慧車研究與車用電子領域。
    研發智慧車的過程，看到車用電子是主要藍海市場，台灣應該應用我國在資通訊科技的優勢，積極切入車用電子市場。
    所以開發系列「即時全方位主動式影像辨識車輛安全技術」，透過技術移轉與專利授權重要車用電子廠商與法人研究單位，帶動台灣影像式車輛主動安全產業。
    <br>
    另外一個創新之處是將實驗室的研究成果：非接觸式的「影像式生理訊號量測技術」，商品化並帶到產業。
    成立創新公司，鉅怡智慧(股), FaceHeart Corp，讓人才有自己的揮灑舞台，也為國家未來培育領袖級的人才。
    2023年我們順利以 SaMD (Software as a Medical Device) 方式，獲得全球第一個美國FDA認證的可見光生理訊號量測技術。
    這個重要的 milestone，讓我們領先國際競爭對手至少 2 年時間。2024/2025年均獲得 CES Innovation Awards，讓世界看到我們台灣在數位健康領域的科技能量。
"""
}

# 首頁「最新消息」列表 (格式: 日期, 標題)
NEWS_ITEMS = [
    ("2026.02", "🎉 恭喜 實驗室網站全新改版上線。"),
]
# 首頁輪播照片 (Carousel)
# 注意：若使用 Google Drive 圖片，需確保權限已開啟並使用 thumbnail 連結格式

HOME_CAROUSEL_IMAGES = [
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=1ENTWuHXiW1f4iggK1wFmjieEOGXEG3WM", "caption": "2026 實驗室尾牙聚餐 @ 新竹-芙洛麗大飯店"},
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=19Y-JbPWhpC58I6RcmFWjrI8v_UQIFrFi", "caption": "2026 同學慶生活動 @ 新竹-禧樂橙"},
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=1A4TNKI0TIl8rVe9TgMU1S1lV2m02ORRy", "caption": "2025 老師慶生活動 @ EE773"},
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=1Ae6ojjuO5LLWkSkB6-Z-cnpOP4f2yOIb", "caption": "2025 917討論會 @ EE917"},
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=18SLQAqth93cRcpOrhUG5fMtPJq_5sWrQ", "caption": "2025 團隊榮獲 NAVSIM v2 創新獎 @ ICCV 2025"},
    {"src": "https://drive.google.com/thumbnail?sz=w1000&id=1jRxrb62pIFfASK-1FdKkxQklckCZu-AP", "caption": "2024 新生迎新聚餐 @ 新竹-新天地美食館"},
    # {"src": "https://drive.google.com/thumbnail?sz=w1000&id=1vZPlcmt0KKgQGES-xm1IUlYmwkB-xgs6", "caption": "2024 老師慶生活動 @ EE773"},
]

# Resources 頁面的外部連結區塊
EXTERNAL_LINKS = [
    ("國立陽明交通大學 (NYCU)", "https://www.nycu.edu.tw/"),
    ("IEEE Xplore", "https://ieeexplore.ieee.org/"),
    ("Google Scholar", "https://scholar.google.com/"),
    ("給新生的大禮包(請使用實驗室專屬帳號)", "https://drive.google.com/drive/folders/141FJXSjk3v-vb_CxveQFMri6FY5JqaCZ?usp=sharing"),
]

# ==========================================
#  資料處理層 (Data Processing Layer)
#  說明：負責讀取 .bib 檔案並轉換為 Python Dictionary 供前端渲染使用。
# ==========================================

class BibDataLoader:
    """封裝 Pybtex 的讀取邏輯，處理檔案不存在的例外狀況。"""
    @staticmethod
    def load_entries(filepath):
        try:
            parser = bibtex.Parser()
            bib_data = parser.parse_file(filepath)
            return bib_data.entries
        except Exception as e:
            # 若檔案讀取失敗，回傳空字典，避免整個網頁生成程式崩潰
            print(f"[Warning] Failed to load {filepath}: {e}", file=sys.stderr)
            return {}

def group_alumni_data(entries):
    """將畢業成員資料依照 'year' 欄位進行分組 (用於歷屆成員頁面)。"""
    groups = {}
    for key, entry in entries.items():
        year_str = entry.fields.get('year', '0')
        if year_str not in groups:
            groups[year_str] = []
        groups[year_str].append((key, entry))
        
    # 依照年份倒序排列 (最新的年份在最上面)
    return sorted(groups.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0, reverse=True)

def str_to_bool(s):
    """輔助函式：將字串轉為布林值 (處理 'true', '1', 'yes' 等情況)。"""
    return str(s).lower() in ['true', '1', 'yes', 't']

def parse_authors(entry):
    """ 
    解析 BibTeX 的作者欄位並轉為 HTML 字串。
    功能包含：
    1. 組合 First/Middle/Last Name。
    2. 將實驗室指導教授或特定成員名字加粗 (Bold)。
    3. 標示通訊作者 (Corresponding Author) 加上星號。
    """
    
    # [設定] 在此列表中加入需要加粗顯示的名字 (通常是指導教授)
    MY_NAMES = [
        "Bing-Fei Wu", 
    ]

    # 讀取 BibTeX 中的 'corresponding' 欄位
    corr_field = entry.fields.get('corresponding', '').lower()

    if 'author' not in entry.persons:
        return ""
    
    authors = []
    for person in entry.persons['author']:
        # 組合名字各部分
        parts = (
            person.first_names + 
            person.middle_names + 
            person.prelast_names + 
            person.last_names + 
            person.lineage_names
        )
        original_name = " ".join(parts)
        display_name = original_name 

        # 邏輯 1: 是否變粗體
        if original_name.lower() in [m.lower() for m in MY_NAMES]:
            display_name = f"<b>{display_name}</b>"

        # 邏輯 2: 是否為通訊作者 (比對 corresponding 欄位)
        if corr_field and (original_name.lower() in corr_field):
            display_name += "*" 
            
        authors.append(display_name)
        
    return ", ".join(authors)

def _safe_get(entry, field, default=''):
    """安全地從 BibTeX Entry 或 Dictionary 中取得欄位值。"""
    if hasattr(entry, 'fields'):
        return entry.fields.get(field, default)
    if isinstance(entry, dict):
        return entry.get(field, default)
    return default

# --- 資料載入與轉換函式 (特定頁面用) ---

def load_gallery_data():
    """載入活動剪影資料，並按年份分組。"""
    entries = BibDataLoader.load_entries(LAB_INFO['files']['gallery'])
    gallery_dict = {}
    
    for key, entry in entries.items():
        year = _safe_get(entry, 'year', 'Others')
        item = {
            "img": _safe_get(entry, 'url'),
            "title": _safe_get(entry, 'title')
        }
        if year not in gallery_dict:
            gallery_dict[year] = []
        gallery_dict[year].append(item)
    
    # 依年份倒序排列
    sorted_items = sorted(gallery_dict.items(), key=lambda x: x[0], reverse=True)
    return dict(sorted_items)

def load_publications_data():
    """載入論文列表，並處理作者格式與 Highlight 標記。"""
    entries = BibDataLoader.load_entries(LAB_INFO['files']['publications'])
    pub_list = []
    
    for key, entry in entries.items():
        booktitle = _safe_get(entry, 'booktitle')
        journal = _safe_get(entry, 'journal')
        
        item = {
            "type": entry.type,
            "author": parse_authors(entry),
            "title": _safe_get(entry, 'title'),
            "booktitle": booktitle if booktitle else journal, # 優先使用 booktitle
            "year": _safe_get(entry, 'year'),
            "img": _safe_get(entry, 'img'),
            "html": _safe_get(entry, 'html', '#'),
            "highlight": str_to_bool(_safe_get(entry, 'highlight', 'false'))
        }
        pub_list.append(item)
    
    # 依年份排序 (新的在前)
    return sorted(pub_list, key=lambda x: x['year'], reverse=True)

def load_media_data():
    """載入媒體報導資料。"""
    entries = BibDataLoader.load_entries(LAB_INFO['files']['media'])
    media_list = []
    
    for key, entry in entries.items():
        item = {
            "title": _safe_get(entry, 'title'),
            "source": _safe_get(entry, 'source'),
            "date": _safe_get(entry, 'date'),
            "url": _safe_get(entry, 'url'),
            "thumbnail": _safe_get(entry, 'thumbnail')
        }
        media_list.append(item)
        
    return sorted(media_list, key=lambda x: x['date'], reverse=True)

# ==========================================
#  視圖渲染層 (View / HTML Generation)
#  說明：負責將資料組合成 HTML 字串。所有 CSS 樣式與 HTML 結構皆在此定義。
# ==========================================

def render_badge(text, style_map=None, default_class="badge-secondary"):
    """產生 Bootstrap Badge 小標籤 (用於顯示課程分類或成員身份)。"""
    if not text: return ""
    css_class = style_map.get(text.lower(), default_class) if style_map else default_class
    return f'<span class="badge {css_class} mr-1" style="font-weight:normal; font-size:0.8em;">{text}</span>'

def render_icon_link(url, icon_class, title=""):
    """產生帶有圖示的連結 (如 Email, Website, Scholar)。"""
    if not url: return ""
    return f'<a href="{url}" target="_blank" title="{title}" style="color: #333; margin: 0 5px;"><i class="{icon_class}"></i></a>'

# --- 核心：導覽列生成 ---
def get_custom_navbar(active_page='home'):
    """生成上方導覽列，並根據 active_page 設定當前頁面樣式。"""
    menu_items = [
        ('home', 'index.html', '首頁 Home'),
        ('members', 'members.html', '成員 Members'),
        ('courses', 'courses.html', '課程 Courses'),
        ('gallery', 'gallery.html', '活動剪影 Gallery'),
        ('resources', 'resources.html', '成果與資源 Resources'),
    ]
    
    nav_links = ""
    for key, url, label in menu_items:
        is_active = "active" if key == active_page else ""
        nav_links += f'<li class="nav-item {is_active}"><a class="nav-link" href="{url}">{label}</a></li>'

    return f"""
    <nav class="navbar navbar-expand-md navbar-light fixed-top" style="background-color: #fff; border-bottom: 1px solid #eee;">
      <div class="container">
        <a class="navbar-brand" href="index.html" style="font-weight: 700; font-size: 1.5rem;">{LAB_INFO['title_en']}</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">{nav_links}</ul>
        </div>
      </div>
    </nav>
    """

# --- 共用版面配置 (Master Layout) ---
def base_html_layout(content, active_page='home', title_suffix=""):
    """
    網頁的骨架 (Skeleton)。
    包含 <head> (CSS引用)、導覽列、主要內容區塊 ({content}) 以及 Footer。
    若需修改全域 CSS 樣式，請修改此函式內的 <style> 區塊。
    """
    navbar = get_custom_navbar(active_page)
    return f"""
    <!doctype html>
    <html lang="zh-TW">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>{LAB_INFO['title_en']} {title_suffix}</title>
      
      <link rel="shortcut icon" href="assets/favicon.ico" type="image/x-icon">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Noto+Sans+TC:wght@300;400;700&display=swap" rel="stylesheet">
      <style>
        body {{ font-family: 'Inter', 'Noto Sans TC', sans-serif; color: #222; padding-top: 70px; }}
        h3, h4 {{ font-weight: 700; margin-bottom: 30px; letter-spacing: -0.5px; }}
        .section-padding {{ padding: 60px 0; }}
        .bg-light-gray {{ background-color: #f9f9f9; }}
        a {{ color: #000; transition: color 0.2s; }}
        a:hover {{ color: #555; text-decoration: none; }}

        /* 導覽列 Active 樣式 */
        .navbar-nav .nav-item.active .nav-link {{
            color: #000 !important;
            font-weight: 700;
            border-bottom: 2px solid #000;
        }}
        .navbar-nav .nav-link {{
            margin: 0 10px;
            color: #555;
        }}

        /* 校友頭像樣式 */
        .alumni-avatar-circle {{
            width: 85px; height: 85px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            position: relative; overflow: hidden;
            color: white; font-weight: bold; font-size: 1.6rem;
            margin: 0 auto 15px;
            background-color: #6c757d;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .alumni-avatar-circle img {{
            width: 100%; height: 100%;
            object-fit: cover;
            position: absolute; top: 0; left: 0;
            z-index: 2;
        }}
        .alumni-thesis-text {{
            display: block; overflow: visible; text-overflow: clip;
            min-height: 3em; line-height: 1.5; font-size: 0.75rem;
            color: #777; margin-top: 5px; text-align: left; padding: 0 5px;
            word-break: break-all;
        }}

        /* 輪播樣式 */
        .carousel-item {{ height: 400px; background-color: #333; }}
        .carousel-item img {{ width: 100%; height: 100%; object-fit: contain; opacity: 0.9; }}
        .carousel-caption {{ background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; }}

        /* 論文列表樣式 */
        .pub-item {{ border-left: 3px solid #eee; transition: all 0.2s; }}
        .pub-item:hover {{ border-left: 3px solid #007bff; background: #f8f9fa; }}
        .pub-img-box {{ width: 160px; height: 100px; background: #eee; flex-shrink: 0; overflow: hidden; border-radius: 4px; }}
        .pub-img-box img {{ width: 100%; height: 100%; object-fit: contain; background-color: #f8f9fa; }}
        
        /* 照片畫廊樣式 */
        .gallery-img {{ width: 100%; height: 220px; object-fit: cover; border-radius: 6px; transition: transform 0.2s; }}
        .gallery-img:hover {{ transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}

        /* 媒體卡片樣式 */
        .media-card {{ transition: transform 0.2s; border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .media-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}

        @media (max-width: 768px) {{ .carousel-item {{ height: 250px; }} .pub-img-box {{ display: none; }} }}
      </style>
    </head>
    <body data-spy="scroll" data-target=".navbar">
      {navbar}
      {content}

      <footer class="text-center py-5 text-muted" style="border-top:1px solid #eee;">
          <div class="mb-3">
              <img src="assets/brand/logo.jpg" alt="Lab Logo" style="height: 60px; width: auto; opacity: 0.9;">
          </div>
          {LAB_INFO['copyright']}
      </footer> 

      <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    </body>
    </html>
    """

# --- 各頁面組件 (Page Components) ---

def get_home_carousel():
    """ 
    生成首頁輪播圖元件。
    邏輯：將照片列表每 2 張分為一組 (Chunk)，在大螢幕上一次顯示兩張。
    """
    
    chunks = [HOME_CAROUSEL_IMAGES[i:i + 2] for i in range(0, len(HOME_CAROUSEL_IMAGES), 2)]
    
    indicators = ""
    items = ""
    
    for i, chunk in enumerate(chunks):
        active_cls = "active" if i == 0 else ""
        
        # 建立指示器 (Slide Indicators)
        indicators += f'<li data-target="#homeCarousel" data-slide-to="{i}" class="{active_cls}"></li>'
        
        # 建立內部圖片欄位
        cols_html = ""
        for img_data in chunk:
            cols_html += f"""
            <div class="col-6 p-0 position-relative" style="height: 100%;">
                <img src="{img_data['src']}" alt="{img_data['caption']}" 
                     style="width: 100%; height: 100%; object-fit: cover;"
                     onerror="this.src='https://via.placeholder.com/600x400?text=No+Image'">
                <div class="carousel-caption d-none d-md-block" style="left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); padding: 5px;">
                    <h6 class="mb-0">{img_data['caption']}</h6>
                </div>
            </div>
            """
        
        # 若該組圖片不足 2 張，補上灰色區塊以維持版面平衡
        if len(chunk) < 2:
            cols_html += '<div class="col-6 p-0" style="background:#333;"></div>'

        items += f"""
        <div class="carousel-item {active_cls}">
            <div class="row m-0" style="height: 100%;">
                {cols_html}
            </div>
        </div>
        """
    
    return f"""
    <div id="homeCarousel" class="carousel slide" data-ride="carousel" style="margin-top: -10px;">
        <ol class="carousel-indicators">{indicators}</ol>
        <div class="carousel-inner">{items}</div>
        
        <a class="carousel-control-prev" href="#homeCarousel" role="button" data-slide="prev" style="width: 5%;">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        </a>
        <a class="carousel-control-next" href="#homeCarousel" role="button" data-slide="next" style="width: 5%;">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
        </a>
    </div>
    """

def get_bio_component():
    """ 
    首頁主要區塊：
    包含：1. 輪播圖 (Top Carousel)  2. 實驗室簡介的三欄式卡片 (Modern 3-Column Cards)
    """
    
    # 簡介內容拆解 (對應首頁的三個卡片)
    
    # 卡片 1：核心技術與理念
    card_1_content = """
    本實驗室致力於影像辨識、智慧型控制與 AI 演算法研究。
    我們深信電機工程是應用科學，致力於將學術成果轉化為提升社會品質的技術，
    實踐做對社會有貢獻 (Society Contribution Index, SCI) 的研究理念。
    """

    # 卡片 2：智慧運輸 (ITS)
    card_2_content = """
    2002 年開發台灣第一輛具備實路經驗的自駕車，讓台灣躋身國際智慧車研究領域。
    我們看準車用電子藍海市場，開發「即時全方位主動式影像辨識」，
    透過技術移轉帶動國內車輛主動安全產業發展。
    """

    # 卡片 3：智慧醫療與新創
    card_3_content = """
    成功孵化新創「鉅怡智慧(股) (FaceHeart Corp)」，讓人才擁有發揮舞台。
    2023 年以 SaMD 獲全球首個 FDA 認證之影像生理偵測技術，領先國際對手 2 年。
    並蟬聯 2024/2025 CES Innovation Awards，展現台灣數位健康科技能量。
    """

    return f"""
    {get_home_carousel()}
    
    <section id="about" class="section-padding bg-white">
        <div class="container">
            
            <div class="row justify-content-center text-center mb-5">
                <div class="col-lg-10">
                    <h2 class="font-weight-bold display-4 mb-3" style="color: #222;">CSSP Lab</h2>
                    <h5 class="text-primary font-weight-bold mb-4" style="letter-spacing: 1px;">{LAB_INFO['title_zh']}</h5>
                    <p class="lead text-muted mx-auto" style="max-width: 800px;">
                        Chaotic Systems and Signal Processing Laboratory
                    </p>
                </div>
            </div>

            <div class="row">
                
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100 border-0 shadow-sm hover-card" style="transition: transform 0.3s;">
                        <div class="card-body text-center p-4">
                            <div class="mb-4 text-primary">
                                <i class="fas fa-microchip fa-3x"></i>
                            </div>
                            <h5 class="card-title font-weight-bold mb-3">核心技術 & 理念</h5>
                            <p class="card-text text-muted text-left" style="font-size: 0.95rem; line-height: 1.6;">
                                {card_1_content}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100 border-0 shadow-sm hover-card" style="transition: transform 0.3s;">
                        <div class="card-body text-center p-4">
                            <div class="mb-4 text-success">
                                <i class="fas fa-car fa-3x"></i>
                            </div>
                            <h5 class="card-title font-weight-bold mb-3">智慧運輸 (ITS)</h5>
                            <p class="card-text text-muted text-left" style="font-size: 0.95rem; line-height: 1.6;">
                                {card_2_content}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6 mb-4 mx-auto">
                    <div class="card h-100 border-0 shadow-sm hover-card" style="transition: transform 0.3s;">
                        <div class="card-body text-center p-4">
                            <div class="mb-4 text-danger">
                                <i class="fas fa-heartbeat fa-3x"></i>
                            </div>
                            <h5 class="card-title font-weight-bold mb-3">智慧醫療 & 新創</h5>
                            <p class="card-text text-muted text-left" style="font-size: 0.95rem; line-height: 1.6;">
                                {card_3_content}
                            </p>
                        </div>
                    </div>
                </div>

            </div>

            <div class="row text-center mt-5 py-4 bg-light rounded align-items-center">
                <div class="col-4 border-right">
                    <h2 class="font-weight-bold text-dark">2002</h2>
                    <small class="text-uppercase text-muted font-weight-bold">台灣首輛自駕車</small>
                </div>
                <div class="col-4 border-right">
                    <h2 class="font-weight-bold text-dark">FDA</h2>
                    <small class="text-uppercase text-muted font-weight-bold">全球首項認證 SaMD</small>
                </div>
                <div class="col-4">
                    <h2 class="font-weight-bold text-dark">2<span style="font-size:0.6em">yr</span></h2>
                    <small class="text-uppercase text-muted font-weight-bold">CES 創新大獎</small>
                </div>
            </div>

            <div class="row mt-5">
                <div class="col-12 text-center">
                    <a href="mailto:{LAB_INFO['email']}" class="btn btn-primary rounded-pill px-5 py-2 shadow-sm" style="font-weight: 600;">
                        <i class="fas fa-envelope mr-2"></i> Contact Us
                    </a>
                </div>
            </div>

        </div>
        
        <style>
            .hover-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
            }}
        </style>
    </section>
    """

def get_news_component():
    """生成首頁的最新消息區塊。"""
    rows = [f'<div class="py-2 border-bottom"><span class="badge badge-info mr-2">{d}</span>{t}</div>' for d, t in NEWS_ITEMS]
    return f'<section class="py-5 container"><h3>最新消息 News</h3>{"".join(rows)}</section>'

def get_courses_component(show_archive=True):
    """
    生成課程資訊 HTML。
    參數:
      show_archive=False: 僅顯示本學期課程 (用於首頁)。
      show_archive=True:  顯示本學期課程 + 歷年課程 Tabs (用於獨立課程頁面)。
    """
    # 1. 當前課程區塊 (Current)
    curr_items = []
    if not COURSES_DATA['current']:
        curr_items.append('<div class="col-12"><p class="text-muted">本學期暫無課程。</p></div>')
    else:
        for c in COURSES_DATA['current']:
            tag_html = render_badge(c.get("tag"), TAG_STYLE_MAP)
            curr_items.append(f"""
            <div class="col-md-6" style="margin-bottom: 20px;">
                <div class="card h-100 shadow-sm" style="border: 1px solid #eee;">
                    <div class="card-body">
                        <h5 class="card-title font-weight-bold">{c['name']}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">{tag_html} {c['code']}</h6>
                        <p class="card-text">{c['desc']}</p>
                        <a href="{c['link']}" class="btn btn-sm btn-outline-primary">課程網頁</a>
                    </div>
                </div>
            </div>
            """)
    current_html = f'<div class="row">{"".join(curr_items)}</div>'

    # 若只需顯示當前課程 (首頁模式)
    if not show_archive:
        return f"""
        <section id="courses" class="section-padding">
            <div class="container">
                <h3>本學期課程 <small class="text-muted" style="font-size: 0.6em;">Current Courses</small></h3>
                {current_html}
                <div class="text-center mt-4">
                    <a href="courses.html" class="btn btn-outline-dark">查看歷年課程列表 &raquo;</a>
                </div>
            </div>
        </section>
        """

    # 2. 歷年課程區塊 (Archive, 用於內頁模式)
    archive_items = []
    for year_title, courses in COURSES_DATA['archive'].items():
        u_id = str(uuid.uuid4())[:8] # 產生獨立 ID 以控制 Accordion
        list_items = []
        for c in courses:
            tag_html = render_badge(c.get("tag"), TAG_STYLE_MAP)
            list_items.append(f"""
            <li class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                        <a href="{c['link']}" style="font-weight:bold; color:#0056b3;">{c['name']}</a>
                        <div class="text-muted" style="font-size:0.9em;">{tag_html} {c['code']}</div>
                    </div>
                    <small class="text-muted d-none d-sm-block">{c['desc']}</small>
                </div>
            </li>
            """)
        
        archive_items.append(f"""
        <div class="card" style="margin-bottom: 5px; border: 1px solid #eee;">
            <div class="card-header" id="heading_{u_id}" style="padding: 0; background-color: #fff;">
                <h5 class="mb-0">
                    <button class="btn btn-link btn-block text-left collapsed" data-toggle="collapse" data-target="#collapse_{u_id}" style="color:#333; font-weight:bold; padding: 15px; text-decoration:none;">
                        <i class="fas fa-calendar-alt mr-2 text-muted"></i> {year_title}
                        <i class="fas fa-chevron-down float-right mt-1 text-muted" style="font-size: 0.8em;"></i>
                    </button>
                </h5>
            </div>
            <div id="collapse_{u_id}" class="collapse" data-parent="#accordionCourses">
                <ul class="list-group list-group-flush">{"".join(list_items)}</ul>
            </div>
        </div>
        """)
    
    archive_html = f'<div id="accordionCourses">{"".join(archive_items)}</div>'

    # 組合 Tabs
    tabs_html = f"""
    <ul class="nav nav-tabs" id="courseTabs" role="tablist" style="margin-bottom: 20px;">
      <li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#current" style="color:#333; font-weight:bold;">當前課程</a></li>
      <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#archive" style="color:#777;">歷年課程</a></li>
    </ul>
    <div class="tab-content">
      <div class="tab-pane fade show active" id="current">{current_html}</div>
      <div class="tab-pane fade" id="archive">{archive_html}</div>
    </div>
    """

    return f"""
    <section id="courses-full" class="section-padding">
        <div class="container">
             <h3>課程資訊 <small class="text-muted" style="font-size: 0.6em;">All Courses</small></h3>
             {tabs_html}
        </div>
    </section>
    """

def get_members_component():
    """生成現任實驗室成員的卡片列表。"""
    
    def get_member_card_html(entry):
        name = _safe_get(entry, 'name', 'Unknown')
        role = _safe_get(entry, 'role')
        img = _safe_get(entry, 'img', 'assets/img/default.jpg')
        group = _safe_get(entry, 'group', 'other').lower()
        scholar = _safe_get(entry, 'scholar') .strip()

        badge_html = render_badge(group.upper(), MEMBER_TAG_MAP)
        email_link = render_icon_link(f"mailto:{_safe_get(entry, 'email')}", "fas fa-envelope") if 'email' in entry.fields else ""
        web_link = render_icon_link(_safe_get(entry, 'website'), "fas fa-globe")
        scholar_link = render_icon_link(scholar, "fas fa-graduation-cap", "Google Scholar")

        return f"""
        <div class="col-md-3 col-sm-6 text-center" style="margin-bottom: 40px;">
            <div style="width: 150px; height: 150px; margin: 0 auto 15px; overflow: hidden; border-radius: 50%; border: 3px solid #f8f9fa;">
                <img src="{img}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.onerror=null;this.src='https://via.placeholder.com/150';">
            </div>
            <h5 style="font-weight: 700; margin-bottom: 5px;">{name}</h5>
            <div style="margin-bottom: 10px;">{badge_html}</div>
            <div style="color: #666; font-size: 0.9rem; margin-bottom: 10px; min-height: 21px;">{role if role else ''}</div>
            <div>{email_link}{web_link}{scholar_link}</div>
        </div>
        """

    entries = BibDataLoader.load_entries(LAB_INFO['files']['members'])
    if not entries:
        content = '<div class="alert alert-warning">無法讀取成員資料。</div>'
    else:
        cards = [get_member_card_html(entry) for entry in entries.values()]
        content = f'<div class="row">{"".join(cards)}</div>'

    return f"""
    <section id="members" class="section-padding">
        <div class="container">
             <h3>研究團隊 <small class="text-muted" style="font-size: 0.6em;">Members</small></h3>
             {content}
        </div>
    </section>
    """

def get_alumni_component():
    """生成歷屆畢業成員 (Alumni) 的列表，依年份分頁 (Pills) 顯示。"""
    entries_all = BibDataLoader.load_entries(LAB_INFO['files']['gar_members'])
    if not entries_all: 
        return ""

    sorted_groups = group_alumni_data(entries_all)
    
    nav_items = []
    content_items = []

    for i, (year, alumni_list) in enumerate(sorted_groups):
        active = "active" if i == 0 else ""
        show = "show active" if i == 0 else ""
        safe_id = f"yr_{year}"
        
        # 建立年份按鈕
        nav_items.append(f'<li class="nav-item"><a class="nav-link {active}" data-toggle="pill" href="#pane-{safe_id}" style="margin:2px; font-size:0.9rem; border:1px solid #ddd;">{year}</a></li>')

        # 分離博士與碩士
        phd_list = [e for key, e in alumni_list if key.startswith('phd_')]
        master_list = [e for key, e in alumni_list if key.startswith('master_')]

        def render_cards(m_list, is_phd=False):
            cards = ""
            bg_color = "bg-primary" if is_phd else "bg-secondary"
            card_col = "col-md-3" if is_phd else "col-md-2"
            for e in m_list:
                name = _safe_get(e, 'name', 'Unknown')
                img = _safe_get(e, 'img')
                role = _safe_get(e, 'role')
                thesis = _safe_get(e, 'thesis')
                initial = name[0] if name else "?"
                img_html = ""
                if img and "default" not in img:
                    img_html = f'<img src="{img}" onerror="this.style.display=\'none\';">'
                cards += f"""
                <div class="col-6 {card_col} text-center mb-5">
                    <div class="alumni-avatar-circle {bg_color} {'border border-primary' if is_phd else ''}">{initial}{img_html}</div>
                    <div class="font-weight-bold text-dark" style="font-size: 1rem;">{name}</div>
                    {f'<div class="small font-weight-bold text-dark mt-1"><i class="fas fa-briefcase mr-1 text-muted"></i>{role}</div>' if role else ''}
                    <div class="alumni-thesis-text" title="{thesis}"><i class="fas fa-book mr-1 text-muted" style="font-size:0.8em;"></i>{thesis}</div>
                </div>
                """
            return cards

        phd_html = f'<div class="row"><div class="col-12"><h6 class="text-primary font-weight-bold border-bottom pb-2 mb-3">博士班 PhD</h6></div>{render_cards(phd_list, True)}</div>' if phd_list else ""
        master_html = f'<div class="row mt-3"><div class="col-12"><h6 class="text-muted font-weight-bold border-bottom pb-2 mb-3">碩士班 Master</h6></div>{render_cards(master_list, False)}</div>' if master_list else ""

        content_items.append(f"""
        <div class="tab-pane fade {show}" id="pane-{safe_id}">
            <div class="p-4 bg-white border rounded shadow-sm">
                {phd_html}
                {master_html}
            </div>
        </div>
        """)

    tabs_html = f"""
    <ul class="nav nav-pills justify-content-center mb-4" role="tablist">{"".join(nav_items)}</ul>
    <div class="tab-content">{"".join(content_items)}</div>
    """
    
    # 說明文字與免責聲明
    notice_html = f"""
    <div class="alert alert-light border shadow-sm mb-4" role="alert" style="font-size: 0.95rem; border-left: 5px solid #17a2b8 !important;">
        <h6 class="alert-heading font-weight-bold" style="font-size: 1rem;">
            <i class="fas fa-info-circle text-info mr-1"></i> 說明與免責聲明
        </h6>
        <p class="mb-1 text-muted">
            本頁面資訊僅供參考，可能未即時更新。請注意：<strong>年份是以「畢業時間」記錄，而非畢業學年度。</strong>
        </p>
        <hr class="my-2">
        <p class="mb-0">
            <i class="fas fa-bullhorn text-warning mr-2"></i>
            歡迎畢業學長姐將目前現況及聯絡方法留下~ 請將資訊寄給 
            <a href="mailto:{LAB_INFO['email']}" class="font-weight-bold text-dark" style="text-decoration: underline;">網頁管理者</a>。
        </p>
    </div>
    """
    return f"""
    <section id="alumni" class="section-padding bg-light-gray">
        <div class="container">
             <h3>歷屆成員 <small class="text-muted" style="font-size: 0.6em;">Alumni</small></h3>
             {notice_html}
             {tabs_html}
        </div>
    </section>
    """

def get_publications_html(publications_data):
    """ 生成論文列表 HTML (左側圖片、右側資訊)。 """
    items = []
    for pub in publications_data:
        # 處理圖片
        img_src = pub.get('img') if pub.get('img') else "https://via.placeholder.com/160x100?text=Paper"
        
        # 處理連結
        link_html = f'<a href="{pub["html"]}" target="_blank" class="btn btn-sm btn-outline-primary mt-2">View Paper</a>' if pub.get('html') else ""
        
        # 處理 Highlight 標記
        highlight_badge = '<span class="badge badge-warning text-white mr-2">Highlight</span>' if pub.get('highlight') else ""
        
        items.append(f"""
        <div class="media mb-4 p-3 pub-item bg-white rounded">
            <div class="pub-img-box mr-4 border">
                <img src="{img_src}" alt="Paper Image">
            </div>
            <div class="media-body">
                <h5 class="mt-0 font-weight-bold" style="font-size: 1.1rem;">
                    {highlight_badge}
                    {pub['title']}
                </h5>
                <div class="text-muted mb-1 small">{pub['author']}</div>
                <div class="text-info font-italic small mb-2">{pub['booktitle']} ({pub['year']})</div>
                {link_html}
            </div>
        </div>
        """)
    
    return "".join(items)

def get_media_html(media_data):
    """ 生成媒體報導卡片 (YouTube / News / Instagram)。 """
    cards = ""
    for media in media_data:
        # 根據 source 設定不同的 FontAwesome 圖示與顏色
        source_lower = media['source'].lower()
        if source_lower == 'youtube':
            icon = "fab fa-youtube text-danger"
        elif source_lower == 'instagram':
            icon = "fab fa-instagram text-primary" 
        else:
            icon = "fas fa-newspaper text-info"
            
        display_date = media.get('date') if media.get('date') else "精選文章"
        thumbnail = media.get('thumbnail') if media.get('thumbnail') else "https://via.placeholder.com/300x180?text=No+Image"

        cards += f"""
        <div class="col-md-4 mb-4">
            <div class="card h-100 media-card">
                <a href="{media['url']}" target="_blank" style="overflow: hidden; height: 180px; display: block;">
                    <img class="card-img-top" src="{thumbnail}" alt="Thumbnail" style="height: 100%; width: 100%; object-fit: cover;">
                </a>
                <div class="card-body">
                    <div class="small text-muted mb-1">
                        <i class="{icon} mr-1"></i> {media['source']} | {display_date}
                    </div>
                    <h6 class="card-title font-weight-bold">
                        <a href="{media['url']}" target="_blank" class="text-dark" style="text-decoration: none;">{media['title']}</a>
                    </h6>
                </div>
            </div>
        </div>
        """
    return f'<div class="row">{cards}</div>'

def get_resources_component(publications_data, media_data):
    """
    整合 Resources 頁面的三大區塊：
    1. 精選論文 (Selected Publications)
    2. 媒體報導與影音 (Media & Talks)
    3. 常用連結 (External Links)
    """
    pub_html = get_publications_html(publications_data)
    media_html = get_media_html(media_data)
    
    links_html = "".join([f'<li class="mb-2"><a href="{url}" target="_blank" class="text-dark"><i class="fas fa-external-link-alt mr-2 text-muted"></i>{name}</a></li>' for name, url in EXTERNAL_LINKS])

    return f"""
    <section class="section-padding bg-light-gray">
        <div class="container">
            
            <div class="mb-5">
                <h3>精選論文 <small class="text-muted" style="font-size:0.6em">Selected Publications</small></h3>
                {pub_html}
            </div>

            <hr class="my-5">

            <div class="mb-5">
                <h3>媒體報導與影音 <small class="text-muted" style="font-size:0.6em">Media & Talks</small></h3>
                {media_html}
            </div>

            <hr class="my-5">

            <div>
                <h3>常用資源連結 <small class="text-muted" style="font-size:0.6em">External Links</small></h3>
                <ul class="list-unstyled row">
                    <div class="col-md-6">{links_html}</div>
                </ul>
            </div>

        </div>
    </section>
    """

def get_gallery_component(gallery_data):
    """ 生成活動剪影頁面 (按年份分頁)。 """
    nav_pills = []
    tab_contents = []

    # 遍歷資料建立分頁
    for i, (year, photos) in enumerate(gallery_data.items()):
        active = "active" if i == 0 else ""
        show = "show active" if i == 0 else ""
        
        nav_pills.append(f"""
        <li class="nav-item">
            <a class="nav-link {active}" data-toggle="pill" href="#gallery-{year}" 
               style="border-radius: 20px; margin: 0 5px; font-weight: 500;">{year}</a>
        </li>
        """)
        
        # 建立該年份的照片 Grid
        photo_grid = ""
        for p in photos:
            photo_grid += f"""
            <div class="col-md-4 col-sm-6 mb-4">
                <a href="{p['img']}" target="_blank" title="點擊查看大圖">
                    <img src="{p['img']}" class="gallery-img" alt="{p['title']}" 
                         onerror="this.src='https://via.placeholder.com/400x300?text=Image'">
                </a>
                <div class="text-center mt-2 small text-muted">{p['title']}</div>
            </div>
            """
        
        tab_contents.append(f"""
        <div class="tab-pane fade {show}" id="gallery-{year}">
            <div class="row">{photo_grid}</div>
        </div>
        """)
    
    return f"""
    <section class="section-padding">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h3>實驗室活動剪影 <small class="text-muted" style="font-size:0.6em">Gallery</small></h3>
            </div>
            <ul class="nav nav-pills mb-4 justify-content-center" id="gallery-tab" role="tablist">
                {"".join(nav_pills)}
            </ul>
            <div class="tab-content">
                {"".join(tab_contents)}
            </div>
        </div>
    </section>
    """

# ==========================================
#  頁面生成與寫入 (Main Execution)
#  說明：呼叫對應的生成函式，並寫入 HTML 檔案。
# ==========================================

def generate_home_page():
    # 首頁結構: 輪播圖 + 實驗室簡介 + 最新消息 + 當前課程
    content = get_bio_component()
    content += get_news_component()
    content += get_courses_component(show_archive=False) 
    return base_html_layout(content, active_page='home')

def generate_members_page():
    # 成員頁結構: 現任成員 + 歷屆校友
    content = get_members_component()
    content += get_alumni_component()
    return base_html_layout(content, active_page='members', title_suffix="- Members")

def generate_courses_page():
    # 課程頁結構: 顯示完整課程 (包含歷年封存)
    content = get_courses_component(show_archive=True) 
    return base_html_layout(content, active_page='courses', title_suffix="- Courses")

def generate_gallery_page():
    # 剪影頁結構: 讀取並顯示照片牆
    gallery_data = load_gallery_data()
    content = get_gallery_component(gallery_data)
    return base_html_layout(content, active_page='gallery', title_suffix="- Gallery")

def generate_resources_page():
    # 資源頁結構: 論文 + 媒體 + 連結
    publications_data = load_publications_data()
    media_data = load_media_data()
    content = get_resources_component(publications_data, media_data)
    return base_html_layout(content, active_page='resources', title_suffix="- Publications & Resources")

def write_html(filename, content):
    """將生成的 HTML 字串寫入檔案。"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Successfully generated {filename}.')
    except Exception as e:
        print(f'Error generating {filename}: {e}')

if __name__ == '__main__':
    write_html('index.html', generate_home_page())
    write_html('members.html', generate_members_page()) 
    write_html('courses.html', generate_courses_page()) 
    write_html('gallery.html', generate_gallery_page()) 
    write_html('resources.html', generate_resources_page())