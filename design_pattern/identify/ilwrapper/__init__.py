# Öffentliche API: nur das hier ist "sichtbar" beim from soapclient import *

from design_pattern.identify.ilwrapper.ilwrapper import ILWrapper
from design_pattern.identify.ilwrapper import ILWrapperConfig, ILWrapperJobtype

__all__ = [
    "ILWrapper",
    "ILWrapperConfig",
    "ILWrapperJobtype",
]


