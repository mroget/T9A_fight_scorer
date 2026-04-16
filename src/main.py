import flet as ft


class Counter(ft.Container):
    def __init__(self, parent_update):
        self.value = 0
        self.text = ft.Text(str(self.value), size=30, weight=ft.FontWeight.W_600)
        self.parent_update = parent_update

        super().__init__()
        

    def init(self):
        row = ft.Row(
            controls=[
                ft.FloatingActionButton(icon=ft.Icons.REMOVE, on_click=self.sub, mini=True),
                self.text, 
                ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add, mini=True)
            ],
            spacing=10,
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.content = row


        self.border=ft.border.all(2, ft.Colors.GREY)
        self.border_radius=8
        self.padding=10
        self.height=70
        self.width=140
        #self.bgcolor=ft.Colors.GREY_200

        #self.alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        #self.vertical_alignment=ft.CrossAxisAlignment.CENTER

    async def add(self, e):
        self.value += 1
        self.update_text()

    async def sub(self, e):
        self.value -= 1
        self.update_text()

    def update_text(self):
        self.text.value = str(self.value)
        self.update()
        self.parent_update()



class Array(ft.Container):
    def __init__(self, items, width):
        self.items = items
        self.width_ = width
        
        super().__init__()

    def init(self):
        self.left_counters = [Counter(self.update_total) for i in self.items]
        self.right_counters = [Counter(self.update_total) for i in self.items]

        col_width = 140

        w = (self.width_ - col_width*2 - 60)//2
        print(w)

        self.total_left = ft.Text("", size=30, weight=ft.FontWeight.W_600)
        self.total_right = ft.Text("", size=30, weight=ft.FontWeight.W_600)
        self.total = ft.Text("Total:", size=30, weight=ft.FontWeight.W_600, text_align="CENTER")

        row = ft.Row([
                ft.Column(
                    [ft.Container(content=ft.Column([ft.FloatingActionButton(icon=ft.Icons.REFRESH, on_click=self.reset_counters, mini=False)], alignment=ft.CrossAxisAlignment.CENTER), height=70, width=60, alignment=ft.Alignment.CENTER)] +
                    [ft.Container(content=ft.Text(i, size=15, weight=ft.FontWeight.W_400), height=70, width=60, alignment=ft.Alignment.CENTER) for i in self.items] +
                    [ft.Container(content=ft.Text("", size=15, weight=ft.FontWeight.W_400), height=70, width=60, alignment=ft.Alignment.CENTER)]
                    ,alignment=ft.Alignment.CENTER
                ),
                ft.Column(
                    [ft.Container(content=ft.Text("Me", size=25, weight=ft.FontWeight.W_400, text_align="CENTER"), height=70, width=col_width, alignment=ft.Alignment.CENTER)] +
                    self.left_counters + 
                    [ft.Container(content=self.total_left, height=70, width=col_width, alignment=ft.Alignment.CENTER)],
                    alignment=ft.Alignment.CENTER
                ),
                ft.Column(
                    [ft.Container(content=ft.Text("Opponent", size=25, weight=ft.FontWeight.W_400), height=70, width=col_width, alignment=ft.Alignment.CENTER)] +
                    self.right_counters +
                    [ft.Container(content=self.total_right, height=70, width=col_width, alignment=ft.Alignment.CENTER)],
                    alignment=ft.Alignment.CENTER
                )
            ],
            spacing=w)



        self.content = ft.Column([
            row,
            ft.Container(content=self.total, width=self.width_, alignment=ft.Alignment.CENTER)
        ], alignment=ft.Alignment.CENTER)
        #self.alignment=ft.Alignment.CENTER

    def update_total(self):
        l = sum([i.value for i in self.left_counters])
        r = sum([i.value for i in self.right_counters])
        tot = l-r
        self.total_left.value = str(l)
        self.total_right.value = str(r)
        self.total.value = f"Total: {tot}"
        self.update()

    def reset_counters(self, e):
        for c in self.left_counters+self.right_counters:
            c.value = 0
            c.update_text()


def main(page: ft.Page):
    array = Array(["Charge", "Banners", "Ranks", "Wounds", "Other"], 370)
    page.add(
        ft.SafeArea(
            expand=True,
            content=array,
        )
    )


ft.run(main)
