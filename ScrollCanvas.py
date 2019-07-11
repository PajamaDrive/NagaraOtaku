import tkinter as tk

class ScrollCanvas:
    def __init__(self, parent, parent_width, parent_height):
        self.__parent = parent
        self.__canvas_width = parent_width
        self.__canvas_height = parent_height
        #全体をキャンバスで覆う
        self.__scroll_canvas = tk.Canvas(self.__parent, width = self.__canvas_width, height = self.__canvas_height)
        self.__scroll_canvas.grid(column = 0, row = 0, sticky = "nwse")
        #スクロールバーの設置
        self.__scrollbar_x = tk.Scrollbar(self.__parent, orient = "horizontal", command = self.__scroll_canvas.xview)
        self.__scrollbar_x.grid(column = 0, row = 1, sticky = "we")
        self.__scrollbar_y = tk.Scrollbar(self.__parent, orient = "vertical", command = self.__scroll_canvas.yview)
        self.__scrollbar_y.grid(column = 1, row = 0, sticky = "ns")
        self.__scroll_canvas.config(xscrollcommand = self.__scrollbar_x.set)
        self.__scroll_canvas.config(yscrollcommand = self.__scrollbar_y.set)
        self.__scroll_frame = tk.Frame(self.__scroll_canvas)
        self.__scroll_canvas.create_window((0, 0), window = self.__scroll_frame)
        self.__scroll_frame.bind("<Configure>", self.scrollCanvas)

    @property
    def frame(self):
        return self.__scroll_frame

    @property
    def scrollbar_x(self):
        return self.__scrollbar_x

    @property
    def scrollbar_y(self):
        return self.__scrollbar_y

    def scrollCanvas(self, event):
        self.__scroll_canvas.config(scrollregion = self.__scroll_canvas.bbox("all"), height = self.__canvas_height * 2)
