from gui import *
from test_models import *
import tkinter as tk


# Запуск приложения
if __name__ == "__main__":

    root = tk.Tk()
    root.title('Управление интернет магазином')
    app = MainApp(root)
    root.mainloop()
    unittest.main()