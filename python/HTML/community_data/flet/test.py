import flet as ft

def main(page: ft.Page):
    page.title = "小型城市資訊"
    page.window.width = 400
    page.window.height = 300
    page.window.resizable = False
    
    # 提示框內容
    def show_city_info(e):
        # 創建提示框
        alert = ft.AlertDialog(
            title=ft.Text("🏙️ 台北市"),
            content=ft.Text(
                "台北市是台灣的首都\n"
                "人口約260萬人\n"
                "著名景點：101大樓、故宮博物院\n"
                "美食：牛肉麵、小籠包、夜市小吃"
            ),
            actions=[
                ft.TextButton("關閉", on_click=lambda e: close_dialog())
            ]
        )
        
        # 顯示提示框
        page.overlay.append(alert)
        alert.open = True
        page.update()
    
    # 關閉提示框
    def close_dialog():
        page.overlay.clear()
        page.update()
    
    # 主要介面
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "🌆 歡迎來到城市資訊站",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.ElevatedButton(
                    text="📍 查看台北市資訊",
                    width=200,
                    height=50,
                    on_click=show_city_info,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE
                    )
                ),
                ft.Container(height=20),
                ft.Text(
                    "點擊按鈕查看城市詳細資訊",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=400,
            height=300,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_50
        )
    )

if __name__ == "__main__":
    ft.app(target=main)