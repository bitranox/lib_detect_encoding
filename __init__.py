# this __init__.py is only meant for local package development
try:
    from .lib_detect_encoding import *
# this we need for pip install --install-option test
except ImportError:
    import lib_detect_encoding
