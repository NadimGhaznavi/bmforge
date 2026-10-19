"""BMForge version, CMDB metadata, and installation defaults."""

from typing import Final


class DBMForge:
    VERSION: Final[str] = "0.1.0"
    CMDB_TYPE: Final[str] = "Application"
    CMDB_SUBTYPE: Final[str] = "SDLC Framework"
    CMDB_SUPPLIER: Final[str] = "Nadim-Daniel"
    CMDB_CODENAME: Final[str] = "Queqiao"
    CMDB_COMPONENTS = ()
    CMDB_DATABASES = ()
    BASE_DIR: Final[str] = "/opt/prod/bmforge"
