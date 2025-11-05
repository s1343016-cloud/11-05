# 文件路徑：pages/03_3D台北建築圖.py
import json
from typing import List, Dict

import solara
import leafmap

TITLE = "3D 台北建築圖（MapLibre + deck.gl）"

# 預設示例：兩棟位於信義區附近的多邊形，含高度屬性，保證離線可視
# 注意：這只是示意多邊形，非真實邊界
DEMO_BUILDINGS: Dict = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Demo Tower A", "height": 180},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [121.5638, 25.0333],
                    [121.5643, 25.0333],
                    [121.5643, 25.0338],
                    [121.5638, 25.0338],
                    [121.5638, 25.0333],
                ]]
            },
        },
        {
            "type": "Feature",
            "properties": {"name": "Demo Tower B", "height": 120},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [121.5646, 25.0336],
                    [121.5650, 25.0336],
                    [121.5650, 25.0340],
                    [121.5646, 25.0340],
                    [121.5646, 25.0336],
                ]]
            },
        },
    ],
}

# Sidebar 與其他頁一致
@solara.component
def Sidebar():
    with solara.Column(gap="1rem"):
        solara.Markdown("### Solara 台北 GIS 儀表板")
        solara.Markdown("切換頁面：")
        solara.Link(path="/首頁", label="🏠 首頁")
        solara.Link(path="/02_2D台北捷運圖", label="🗺️ 2D 台北捷運圖")
        solara.Link(path="/03_3D台北建築圖", label="🏙️ 3D 台北建築圖")

def geojson_to_deck_polygon_data(fc: Dict, height_keys: List[str] = ["height", "ele"]) -> List[Dict]:
    """把 GeoJSON FeatureCollection 轉成 deck.gl PolygonLayer 可用的資料列。
    需具備 Polygon 幾何與高度屬性（height 或 ele），若缺則給預設 30m。
    """
    rows = []
    for f in fc.get("features", []):
        if f.get("geometry", {}).get("type") != "Polygon":
            continue
        props = f.get("properties", {}) or {}
        h = None
        for k in height_keys:
            if k in props:
                try:
                    h = float(props[k])
                except Exception:
                    pass
        if h is None:
            h = 30.0
        rows.append({
            "name": props.get("name", "building"),
            "height": h,
            # deck.gl 直接吃 polygon 座標
            "polygon": f["geometry"]["coordinates"][0],
        })
    return rows

# 主要內容
@solara.component
def Content():
    # 允許從外部 GeoJSON URL 載入（需有 CORS 且回傳有效 GeoJSON）
    url_state = solara.use_reactive("")
    status = solara.use_reactive("已載入範例建築（離線可看）")

    # 建 MapLibre 地圖
    m = leafmap.Map(use_maplibregl=True, center=(25.033968, 121.564468), zoom=15)
    # Positron 底圖（免 token）
    m.add_basemap("CartoDB.Positron")

    # 建立 deck.gl 3D PolygonLayer 的 spec
    def add_buildings_from_geojson(fc: Dict):
        data = geojson_to_deck_polygon_data(fc)
        spec = {
            "initialViewState": {
                "latitude": 25.033968,
                "longitude": 121.564468,
                "zoom": 15,
                "pitch": 60,
                "bearing": 20,
            },
            "layers": [
                {
                    "@@type": "PolygonLayer",
                    "id": "taipei-buildings",
                    "data": data,
                    "getPolygon": "polygon",
                    "getElevation": "height",
                    "extruded": True,
                    "wireframe": True,
                    "opacity": 0.8,
                    "pickable": True,
                    "getFillColor": [180, 180, 200],
                    "getLineColor": [60, 60, 80],
                }
            ],
        }
        # leafmap 封裝的 maplibregl + deck.gl
        # 新版 leafmap 提供 add_deckgl_layer，舊版可用 add_deckgl_json
        if hasattr(m, "add_deckgl_layer"):
            m.add_deckgl_layer(spec)
        else:
            m.add_deckgl_json(json.dumps(spec))

    # 預設載入內建示例
    add_buildings_from_geojson(DEMO_BUILDINGS)

    # 事件：從 URL 載入
    def load_from_url():
        import requests  # HF Space 可用；若無網路會回退
        try:
            resp = requests.get(url_state.value, timeout=10)
            resp.raise_for_status()
            fc = resp.json()
            # 先清圖層再重加底圖與 deck.gl
            m.clear_layers()
            m.add_basemap("CartoDB.Positron")
            add_buildings_from_geojson(fc)
            status.value = "已從 URL 載入 3D 建築"
        except Exception as e:
            status.value = f"載入失敗，已回退示例：{e}"
            m.clear_layers()
            m.add_basemap("CartoDB.Positron")
            add_buildings_from_geojson(DEMO_BUILDINGS)

    with solara.Column(gap="1rem"):
        solara.Title(TITLE)
        solara.Markdown(
            "底圖：`CartoDB Positron`。可貼上含 `height` 或 `ele` 欄位的建築 GeoJSON URL，按「載入 3D 建築」。"
        )
        with solara.HBox(gap="0.5rem"):
            solara.InputText(label="建築 GeoJSON URL", value=url_state, placeholder="https://.../buildings.geojson")
            solara.Button("載入 3D 建築", on_click=load_from_url)
        if status.value:
            solara.Info(status.value)

        # 把 maplibregl 視圖嵌入到 Solara
        solara.IpyWidget(m.to_widget())

# Solara 多頁入口
@solara.component
def Page():
    with solara.AppLayout(title=TITLE, sidebar=Sidebar()):
        Content()

