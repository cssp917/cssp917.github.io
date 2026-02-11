COPY_RIGHT = "&copy; 2026 CSSP Laboratory, NYCU. All rights reserved."
# 定義不同課程類別對應的 Bootstrap Badge 顏色樣式
TAG_STYLE_MAP = {
    "電機系": "badge-primary",   # 藍色
    "電機專": "badge-success",   # 綠色
    "電控碩": "badge-dark",      # 深色
    "電機共同": "badge-warning", # 黃色
    "電控系": "badge-danger",    # 紅色
    "其他": "badge-secondary"    # 灰色
}

# 定義各區塊內容的文字顏色樣式 (Bootstrap class)
# 用於統一管理不同資訊區塊的視覺主題
SECTION_COLOR_MAP = {
    "announcement": "text-warning",   # 公告：黃色系
    "homework":     "text-primary",   # 作業：藍色系
    "quiz":         "text-success",   # 小考：綠色系
    "textbook":     "text-dark",      # 教科書：深色系
    "grading":      "text-info",      # 評分：淺藍色系
    "ta":           "text-secondary", # 助教：灰色系
    "resource":     "text-danger"     # 資源：紅色系
}

MEMBER_TAG_MAP = {
    "professor": "badge-success",   # 教授 (綠色)
    "phd": "badge-primary",         # 博士生 (藍色)
    "master": "badge-info",         # 碩士生 (淺藍)
    "ra": "badge-dark",             # 研究助理 (深色)
    "aa": "badge-warning",          # 行政助理 (黃色)
    "alumni": "badge-secondary",    # 校友 (灰色)
}


def get_navbar(is_course_page=False, course_title=""):
    """
    is_course_page: 布林值，True 表示課程頁面
    course_title: 如果是課程頁面，顯示課程英文名稱
    """
    if is_course_page:
        return f"""
    <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top" style="border-bottom: 1px solid #eee;">
      <div class="container">
        <a class="navbar-brand" href="../../../courses.html" style="font-weight: 700;">&larr; 回首頁 (Back to Lab)</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item"><span class="nav-link" style="font-weight: bold;">{course_title}</span></li>
          </ul>
        </div>
      </div>
    </nav>
    """
    # 尚未整合
    # 
    # else:
    #     return """
    # <nav class="navbar navbar-expand-lg navbar-light bg-white fixed-top" style="border-bottom: 1px solid #eee;">
    #   <div class="container">
    #     <a class="navbar-brand" href="#" style="font-weight: 700; font-size: 1.5rem;">CSSP Lab.</a>
    #     <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    #       <span class="navbar-toggler-icon"></span>
    #     </button>
    #     <div class="collapse navbar-collapse" id="navbarNav">
    #       <ul class="navbar-nav ml-auto">
    #         <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
    #         <li class="nav-item"><a class="nav-link" href="#news">最新消息</a></li>
    #         <li class="nav-item"><a class="nav-link" href="#members">研究團隊</a></li>
    #         <li class="nav-item"><a class="nav-link" href="#courses">課程資訊</a></li>
    #         <li class="nav-item"><a class="nav-link" href="#links">相關連結</a></li>
    #       </ul>
    #     </div>
    #   </div>
    # </nav>
    # """
