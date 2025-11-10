import solara

# 1. 建立一個「響應式」變數
count = solara.reactive(0)

# 2. 定義 Solara 元件
@solara.component
def Page():
    solara.Title("我的 Solara App")
    solara.Markdown(f"## 按鈕被點擊了 {count.value} 次！")

    def increment():
        count.value += 1  # 改變狀態值

    solara.Button("點我！", on_click=increment)


# ✅ 3. 啟動應用入口（這是 Hugging Face 會找的 main）
if __name__ == "__main__":
    solara.run()
