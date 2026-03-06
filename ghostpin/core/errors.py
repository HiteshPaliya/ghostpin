"""
GhostPin — Typed Exception Hierarchy
All modules should raise these instead of bare RuntimeError / Exception.
"""

class GhostPinError(Exception):
    """Base exception for all GhostPin errors."""
    pass

class DeviceError(GhostPinError):
    """Raised when an ADB device operation fails."""
    pass

class FridaError(GhostPinError):
    """Raised when a Frida attach / script injection fails."""
    pass

class DownloadError(GhostPinError):
    """Raised when a binary or release download fails."""
    pass

class ScanError(GhostPinError):
    """Raised when a static or dynamic scan cannot complete."""
    pass

class DecompileError(GhostPinError):
    """Raised when JADX decompilation fails."""
    pass

class AuthError(GhostPinError):
    """Raised on authentication/authorization failures."""
    pass

class PatchError(GhostPinError):
    """Raised when APK/IPA patching fails."""
    pass
