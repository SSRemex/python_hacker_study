from ctypes import cdll, windll, c_ulong

dll = windll.LoadLibrary("user32.dll")

print(dll)

dll.MessageBoxA(None, "test".encode("utf8"), "aaaa".encode("utf8"), c_ulong(0))

