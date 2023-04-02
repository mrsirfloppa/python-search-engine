import sys
import tkinter as tk
from cefpython3 import cefpython as cef

class MainFrame(tk.Frame):
    def __init__(self, root):
        self.browser_frame = None
        self.navigation_bar = None

        tk.Frame.__init__(self, root)
        self.root = root

        self.init_browser()
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def init_browser(self):
        window_info = cef.WindowInfo()
        window_info.SetAsChild(self.winfo_id())

        self.browser = cef.CreateBrowserSync(window_info=window_info, url="https://www.google.com/")
        self.browser.SetClientHandler(LoadHandler(self))

    def on_focus_in(self, _):
        pass

    def on_focus_out(self, _):
        pass

class LoadHandler(object):
    def __init__(self, main_frame):
        self.main_frame = main_frame

def main():
    sys.excepthook = cef.ExceptHook
    cef.Initialize()

    root = tk.Tk()
    root.geometry("900x600")

    main_frame = MainFrame(root)
    main_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def on_back_click():
        main_frame.browser.GoBack()

    def on_forward_click():
        main_frame.browser.GoForward()

    def on_reload_click():
        main_frame.browser.Reload()

    def on_home_click():
        main_frame.browser.LoadUrl("https://www.google.com/")

    back_button = tk.Button(root, text="Back", command=on_back_click)
    back_button.pack(side=tk.LEFT)

    forward_button = tk.Button(root, text="Forward", command=on_forward_click)
    forward_button.pack(side=tk.LEFT)

    reload_button = tk.Button(root, text="Reload", command=on_reload_click)
    reload_button.pack(side=tk.LEFT)

    home_button = tk.Button(root, text="Home", command=on_home_click)
    home_button.pack(side=tk.LEFT)

    root.mainloop()
    cef.Shutdown()

if __name__ == "__main__":
    main()
