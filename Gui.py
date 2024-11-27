import tkinter as tk
from tkinter import messagebox
from Constant import SIZE, CELL_WIDTH, BACKGROUND_COLOR, CELL_COLOR, LINE_COLOR, INFO_MESSAGE, INTRODUCE_MESSAGE, AI_VALUE, USER_VALUE
from ChessBoard.State import State
from CaroAI.AI import CaroAI
from PIL import Image, ImageTk


class GameGUI:
    def __init__(self):
        """Khởi tạo giao diện."""
        self.state = State()  # Trạng thái bàn cờ
        self.ai = CaroAI(mode=0)
        self.size = SIZE  # Kích thước bàn cờ (số ô)
        self.cell_size = CELL_WIDTH  # Kích thước mỗi ô
        self.root = tk.Tk()  # Tạo cửa sổ Tkinter
        self.root.title("Cờ Caro")  # Tiêu đề cửa sổ
        self.root.resizable(False, False)  # Ngăn thay đổi kích thước cửa sổ

        # Đặt logo cho cửa sổ
        self.root.iconbitmap("logo.ico")

        # Gắn sự kiện khi đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Tạo các thành phần giao diện
        self.create_widgets()

        self.user_turn = True  # Xác định lượt chơi (User đi trước mặc định)

    def create_widgets(self):
        """Tạo giao diện."""
        # Frame chứa bàn cờ
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        # Canvas vẽ bàn cờ
        self.canvas = tk.Canvas(
            self.board_frame,
            width=self.size * self.cell_size,
            height=self.size * self.cell_size,
            bg=BACKGROUND_COLOR,
        )
        self.canvas.pack()
        # Sự kiện click chuột
        self.canvas.bind("<Button-1>", self.handle_click)

        # Frame chứa thanh cài đặt
        self.control_frame = tk.Frame(
            self.root, bg="lightgray", padx=10, pady=10)
        self.control_frame.grid(row=0, column=1, sticky="ns")

         # Hiển thị trạng thái
        self.status_label = tk.Label(
            self.control_frame,
            text="Welcome to Cờ Caro!",
            font=("Arial", 10),
            wraplength=150,
            justify="center",
        )
        self.status_label.pack(pady=20)
        
        # Hiển thị ảnh
        image = Image.open("image.jpg")
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.control_frame, image=self.photo, bg="lightgray")
        self.image_label.pack(pady=20)

        # Nút "New Game"
        self.new_game_button = tk.Button(
            self.control_frame, text="New Game", command=self.confirm_new_game, font=("Arial", 12), width=15
        )
        self.new_game_button.pack(pady=10)

        # Nút "Info"
        self.info_button = tk.Button(
            self.control_frame, text="Info", command=self.show_info, font=("Arial", 12), width=15
        )
        self.info_button.pack(pady=10)

        # Nút "Introduce"
        self.introduce_button = tk.Button(
            self.control_frame, text="Introduce", command=self.show_introduce, font=("Arial", 12), width=15
        )
        self.introduce_button.pack(pady=10)

        # Nút "Exit Game"
        self.exit_button = tk.Button(
            self.control_frame, text="Exit Game", command=self.on_close, font=("Arial", 12), width=15
        )
        self.exit_button.pack(pady=10)

        # Vẽ bàn cờ
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline=LINE_COLOR, fill=CELL_COLOR
                )

                # Hiển thị trạng thái X hoặc O
                cell = self.state.get_cell(i, j)
                if cell.get_selected() == 1:  # User
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="X",
                        fill="red",
                        font=("Arial", 18),
                    )
                elif cell.get_selected() == 2:  # AI
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="O",
                        fill="blue",
                        font=("Arial", 18),
                    )

    def handle_click(self, event):
        """Xử lý sự kiện click chuột."""
        x, y = event.y // self.cell_size, event.x // self.cell_size

        if self.state.is_clickable(x, y):
            self.state.update(x, y, USER_VALUE)
            self.ai.root.update(x, y, USER_VALUE)
            self.draw_board()
            
            if self.state.check_winner(1):
                self.ai.root = State()
                messagebox.showinfo("Kết quả", "Bạn đã thắng!")
                self.confirm_new_game()
                return

            if self.state.is_over():
                self.ai.root = State()
                messagebox.showinfo("Kết quả", "Hòa cờ!")
                self.confirm_new_game()
                return

            self.ai_turn()

    def ai_turn(self):
        """Lượt đi của AI."""
        
        self.ai.next_step()
        x, y = self.ai.get_next_x(), self.ai.get_next_y()

        if x is not None and y is not None:
            self.state.update(x, y, AI_VALUE)
            self.ai.root.update(x, y, AI_VALUE)
            self.draw_board()

            if self.state.check_winner(2):
                self.ai.root = State()
                messagebox.showinfo("Kết quả", "AI đã thắng!")
                self.confirm_new_game()
            elif self.state.is_over():
                self.ai.root = State()
                messagebox.showinfo("Kết quả", "Hòa cờ!")
                self.confirm_new_game()

    def confirm_new_game(self):
        """Hiển thị xác nhận trước khi bắt đầu game mới."""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn bắt đầu game mới?"):
            self.new_game()

    def new_game(self):
        """Khởi tạo lại trạng thái bàn cờ."""
        self.state = State()
        self.draw_board()

    def show_info(self):
        """Hiển thị thông tin nhóm."""
        messagebox.showinfo("Thông tin nhóm", INFO_MESSAGE)

    def show_introduce(self):
        """Hiển thị luật chơi."""
        messagebox.showinfo("Luật chơi", INTRODUCE_MESSAGE)

    def on_close(self):
        """Hiển thị xác nhận trước khi thoát game."""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát?"):
            self.root.destroy()

    def run(self):
        """Chạy giao diện."""
        self.root.mainloop()
