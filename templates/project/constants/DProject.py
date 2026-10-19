from typing import Final


class DProject:
    VERSION: Final[str] = "0.0.0"
    CMDB_TYPE: Final[str] = "Application"
    CMDB_SUBTYPE: Final[str] = "__PROJECT_SUBTYPE__"
    CMDB_SUPPLIER: Final[str] = "Nadim-Daniel"
    CMDB_CODENAME: Final[str] = "Initial development"
    CMDB_COMPONENTS = ()
    CMDB_DATABASES = ()
    BASE_DIR: Final[str] = "/opt/prod/__PROJECT_SLUG__"
