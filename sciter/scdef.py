"""Common Sciter declarations."""

from enum import IntEnum

from ctypes import *
from ctypes.wintypes import *

from sciter.sctypes import *
from sciter.scdom import HELEMENT
from sciter.screquest import HREQUEST
from sciter.scvalue import PSCITER_VALUE


class LOAD_RESULT(IntEnum):
    """."""
    LOAD_OK = 0       # do default loading if data not set
    LOAD_DISCARD = 1  # discard request completely
    LOAD_DELAYED = 2  # data will be delivered later by the host application.

    LOAD_MYSELF = 3   # Use sciter-x-request.h[pp] API functions with SCN_LOAD_DATA::requestId handle .


class SciterNotification(IntEnum):
    """."""
    SC_LOAD_DATA = 0x01
    SC_DATA_LOADED = 0x02
    SC_ATTACH_BEHAVIOR = 0x04
    SC_ENGINE_DESTROYED = 0x05
    SC_POSTED_NOTIFICATION = 0x06
    SC_GRAPHICS_CRITICAL_FAILURE = 0x07


class SCITER_RT_OPTIONS(IntEnum):
    SCITER_SMOOTH_SCROLL = 1       # value:TRUE - enable, value:FALSE - disable, enabled by default
    SCITER_CONNECTION_TIMEOUT = 2  # value: milliseconds, connection timeout of http client
    SCITER_HTTPS_ERROR = 3         # value: 0 - drop connection, 1 - use builtin dialog, 2 - accept connection silently
    SCITER_FONT_SMOOTHING = 4      # value: 0 - system default, 1 - no smoothing, 2 - std smoothing, 3 - clear type

    SCITER_TRANSPARENT_WINDOW = 6  # Windows Aero support, value:
                                   # 0 - normal drawing,
                                   # 1 - window has transparent background after calls DwmExtendFrameIntoClientArea() or DwmEnableBlurBehindWindow().
    SCITER_SET_GPU_BLACKLIST  = 7  # hWnd = NULL,
                                   # value = LPCBYTE, json - GPU black list, see: gpu-blacklist.json resource.
    SCITER_SET_SCRIPT_RUNTIME_FEATURES = 8,  # value - combination of SCRIPT_RUNTIME_FEATURES flags.
    SCITER_SET_GFX_LAYER = 9       # hWnd = NULL, value - GFX_LAYER
    SCITER_SET_DEBUG_MODE = 10     # hWnd, value - TRUE/FALSE
    SCITER_SET_UX_THEMING = 11     # hWnd = NULL, value - BOOL, TRUE - the engine will use "unisex" theme that is common for all platforms. 
                                   # That UX theme is not using OS primitives for rendering input elements. Use it if you want exactly
                                   # the same (modulo fonts) look-n-feel on all platforms.
    SCITER_ALPHA_WINDOW  = 12      #  hWnd, value - TRUE/FALSE - window uses per pixel alpha (e.g. WS_EX_LAYERED/UpdateLayeredWindow() window)


class SCRIPT_RUNTIME_FEATURES(IntEnum):
    ALLOW_FILE_IO = 0x00000001
    ALLOW_SOCKET_IO = 0x00000002
    ALLOW_EVAL = 0x00000004
    ALLOW_SYSINFO = 0x00000008


class GFX_LAYER(IntEnum):
    GFX_LAYER_GDI      = 1
    GFX_LAYER_WARP     = 2
    GFX_LAYER_D2D      = 3
    GFX_LAYER_AUTO     = 0xFFFF


class OUTPUT_SUBSYTEMS(IntEnum):
    DOM = 0       # html parser & runtime
    CSSS = 1      # csss! parser & runtime
    CSS = 2       # css parser
    TIS = 3       # TIS parser & runtime


class OUTPUT_SEVERITY(IntEnum):
    INFO = 0
    WARNING = 1
    ERROR = 2


class SCITER_CREATE_WINDOW_FLAGS(IntEnum):
    SW_CHILD      = (1 << 0)    # child window only, if this flag is set all other flags ignored
    SW_TITLEBAR   = (1 << 1)    # toplevel window, has titlebar
    SW_RESIZEABLE = (1 << 2)    # has resizeable frame
    SW_TOOL       = (1 << 3)    # is tool window
    SW_CONTROLS   = (1 << 4)    # has minimize / maximize buttons
    SW_GLASSY     = (1 << 5)    # glassy window ( DwmExtendFrameIntoClientArea on windows )
    SW_ALPHA      = (1 << 6)    # transparent window ( e.g. WS_EX_LAYERED on Windows )
    SW_MAIN       = (1 << 7)    # main window of the app, will terminate the app on close
    SW_POPUP      = (1 << 8)    # the window is created as topmost window.
    SW_ENABLE_DEBUG = (1 << 9)  # make this window inspector ready
    SW_OWNS_VM    = (1 << 10)   # it has its own script VM


class SCITER_CALLBACK_NOTIFICATION(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
    ]


class SCN_LOAD_DATA(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("uri", LPCWSTR),
        ("outData", LPCBYTE),
        ("outDataSize", UINT),
        ("dataType", UINT),
        ("requestId", HREQUEST),
        ("principal", HELEMENT),
        ("initiator", HELEMENT),
        ]


class SCN_DATA_LOADED(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("uri", LPCWSTR),
        ("data", LPCBYTE),
        ("dataSize", UINT),
        ("dataType", UINT),
        ("status", UINT),
        ]


class SCN_ATTACH_BEHAVIOR(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("element", HELEMENT),
        ("behaviorName", LPCSTR),
        ("elementProc", c_void_p),
        ("elementTag", LPVOID),
    ]


LPSCITER_CALLBACK_NOTIFICATION = POINTER(SCITER_CALLBACK_NOTIFICATION)
SciterHostCallback = SC_CALLBACK(UINT, LPSCITER_CALLBACK_NOTIFICATION, LPVOID)

SciterWindowDelegate = SC_CALLBACK(LRESULT, HWINDOW, UINT, WPARAM, LPARAM, LPVOID, PBOOL)

DEBUG_OUTPUT_PROC = SC_CALLBACK(VOID, LPVOID, UINT, UINT, LPCWSTR, UINT)

LPCSTR_RECEIVER = SC_CALLBACK(VOID, LPCSTR, UINT, LPVOID)
LPCWSTR_RECEIVER = SC_CALLBACK(VOID, LPCWSTR, UINT, LPVOID)
LPCBYTE_RECEIVER = SC_CALLBACK(VOID, LPCBYTE, UINT, LPVOID)

SciterElementCallback = SC_CALLBACK(BOOL, HELEMENT, LPVOID)

ElementEventProc = SC_CALLBACK(BOOL, LPVOID, HELEMENT, UINT, LPVOID)

ELEMENT_COMPARATOR = SC_CALLBACK(INT, HELEMENT, HELEMENT, LPVOID)

KeyValueCallback = SC_CALLBACK(BOOL, LPVOID, PSCITER_VALUE, PSCITER_VALUE)

NATIVE_FUNCTOR_INVOKE = CFUNCTYPE(VOID, LPVOID, UINT, PSCITER_VALUE, PSCITER_VALUE)
NATIVE_FUNCTOR_RELEASE = CFUNCTYPE(VOID, LPVOID)
