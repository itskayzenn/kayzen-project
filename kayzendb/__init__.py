"""
KayzenDB
~~~~~~~~

Database engine file-based yang ringan, aman (AES-256), dan ACID-lite.
"""

from .core import KayzenDB

# Metadata Package
__version__ = "1.0.0"
__author__ = "Kayzen Architect"
__license__ = "MIT"

# Menentukan apa yang diekspor saat user melakukan: from kayzendb import *
__all__ = ["KayzenDB"]
