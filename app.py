"""
TimeFlow - Desktop Widget Native Launcher (PyWebView)
Runs as a frameless, draggable floating desktop plugin on Windows.
"""

import webview
import os
import sys

class WidgetApi:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def set_on_top(self, on_top):
        if self.window:
            self.window.on_top = bool(on_top)

    def resize_mini(self):
        if self.window:
            self.window.resize(360, 68)

    def resize_full(self):
        if self.window:
            self.window.resize(380, 580)

    def close(self):
        if self.window:
            self.window.destroy()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'index.html')

    api = WidgetApi()

    # Create frameless floating desktop window
    window = webview.create_window(
        title='TimeFlow Widget',
        url=f'file:///{html_path.replace("\\", "/")}',
        js_api=api,
        width=380,
        height=580,
        frameless=True,
        easy_drag=True,
        transparent=True,
        on_top=False,
        background_color='#0f172a'
    )
    
    api.set_window(window)
    webview.start(debug=False)


if __name__ == '__main__':
    main()
