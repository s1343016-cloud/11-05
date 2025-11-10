# 文件路徑：pages/首頁.py
import solara

TITLE = "Solara 台北 GIS 儀表板"

# 共用側邊欄
@solara.component
def Sidebar():
    with solara.Column(gap="1rem"):
        solara.Markdown(f"### {TITLE}")
        solara.Markdown("切換頁面：")
        solara.Link(path="/首頁", label="🏠 首頁")
        solara.Link(path="/02_2D台北捷運圖", label="🗺️ 2D 台北捷運圖")
        solara.Link(path="/03_3D台北建築圖", label="🏙️ 3D 台北建築圖")

# 首頁主內容
@solara.component
def HomeContent():
    router = solara.use_router()

    with solara.Column(gap="1rem"):
        solara.Title(TITLE)
        solara.Markdown(
            """
**作業目標**  
建立三頁式 Solara WebGIS，並部署到 Hugging Face Spaces（Docker）。

**頁面清單**  
1. 首頁（本頁）  
2. 2D 台北捷運圖  
3. 3D 台北建築圖
            """
        )

        with solara.HBox(gap="0.5rem"):
            solara.Button("前往 2D 台北捷運圖", on_click=lambda: router.push("/02_2D台北捷運圖"))
            solara.Button("前往 3D 台北建築圖", on_click=lambda: router.push("/03_3D台北建築圖"))

        solara.Markdown(
            """
**開發與部署重點**  
- 使用 GitHub Codespaces 開發  
- 必用 Solara  
- 部署到 Hugging Face Spaces（Docker 模式）
            """
        )

# Page 入口（Solara MPA 需要）
@solara.component
def Page():
    with solara.AppLayout(title=TITLE, sidebar=Sidebar()):
        HomeContent()
