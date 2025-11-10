# 文件路徑：pages/02_2D台北捷運圖.py
import solara
import leafmap

TITLE = "2D 台北捷運圖"

# 你可以換成實際的捷運 GeoJSON 連結
# 若預設無效，請在頁面輸入框貼上正確的 raw GeoJSON URL 後按「載入圖層」
DEFAULT_GEOJSON_URL = (
    "https://raw.githubusercontent.com/leoluyi/taipei_mrt/master/data/taipei_mrt.geojson"
)

# 共用側邊欄
@solara.component
def Sidebar():
    with solara.Column(gap="1rem"):
        solara.Markdown("### Solara 台北 GIS 儀表板")
        solara.Markdown("切換頁面：")
        solara.Link(path="/首頁", label="🏠 首頁")
        solara.Link(path="/02_2D台北捷運圖", label="🗺️ 2D 台北捷運圖")
        solara.Link(path="/03_3D台北建築圖", label="🏙️ 3D 台北建築圖")

# 主要內容
@solara.component
def Content():
    url_state = solara.use_reactive(DEFAULT_GEOJSON_URL)
    status = solara.use_reactive("")

    # 建立 leafmap 地圖（ipyleaflet）
    m = leafmap.Map(center=(25.0418, 121.5360), zoom=12, draw_control=False)
    m.add_basemap("CartoDB.DarkMatter")

    # 嘗試加載捷運 GeoJSON
    def load_layer():
        try:
            m.clear_layers()
            m.add_basemap("CartoDB.DarkMatter")
            m.add_geojson(url_state.value, layer_name="台北捷運")
            status.value = "已載入捷運圖層"
        except Exception as e:
            status.value = f"載入失敗：{e}"

    # 初次載入
    solara.use_effect(lambda: load_layer(), deps=[])

    with solara.Column(gap="1rem"):
        solara.Title(TITLE)
        solara.Markdown(
            "底圖：`CartoDB.DarkMatter`．如需替換資料，貼上下方 GeoJSON URL 後點「載入圖層」。"
        )
        with solara.HBox(gap="0.5rem"):
            solara.InputText(label="捷運 GeoJSON URL", value=url_state)
            solara.Button("載入圖層", on_click=load_layer)
        if status.value:
            solara.Info(status.value)

        # 將 ipyleaflet 小工具嵌入 Solara
        # leafmap 的 to_widget() 會回傳 ipywidget，Solara 用 IpyWidget 顯示
        solara.IpyWidget(m.to_widget())

# Solara 多頁入口
@solara.component
def Page():
    with solara.AppLayout(title=TITLE, sidebar=Sidebar()):
        Content()
