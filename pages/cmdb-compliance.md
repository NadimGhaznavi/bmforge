---
title: CMDB Compliance
lang: en
locale: en-US
language_name: English
translation_key: bmforge-cmdb-compliance
---

Make every new project discoverable by the CMDB. Establish its application name, constants file, and installation path during setup.

## Name the Application

Choose one canonical application name matching `[A-Za-z_][A-Za-z0-9_]*`. Spaces and hyphens are unsupported by application discovery. Preserve the name's capitalization in the constants filename and use its lowercase form for the package and installation directory.

| Item | Convention | Example |
| --- | --- | --- |
| CMDB registered name | Canonical application name | `MyCount` |
| New repository name | Lowercase application name | `mycount` |
| Python package | Lowercase application name | `mycount` |
| Development checkout | `/opt/dev/<lowercase-name>` | `/opt/dev/mycount` |
| Installation root | `/opt/prod/<lowercase-name>` | `/opt/prod/mycount` |
| Constants file in the project | `<lowercase-name>/constants/D<Name>.py` | `mycount/constants/DMyCount.py` |
| Constants class | `D<Name>` | `DMyCount` |

Discovery derives the installed constants path from the registered name. It does not scan development checkouts or infer application names from repository URLs. Register the exact canonical name through the CMDB's **Add Application** action.

## Declare the Metadata

Copy the [constants template]({{ '/templates/project/constants/DProject.py' | relative_url }}) to the project's constants path. Rename its class and replace its placeholders. Keep `VERSION` and `CMDB_CODENAME` as independent, single-line literal string assignments; the release script updates those values while preserving annotations and surrounding text.

| Constant | Requirement |
| --- | --- |
| `VERSION` | Semantic version without a leading `v`; initially `0.0.0` |
| `CMDB_TYPE` | Always exactly `"Application"` |
| `CMDB_SUBTYPE` | Short description of the application's function |
| `CMDB_SUPPLIER` | Supplier name; the template defaults to `Nadim-Daniel` |
| `CMDB_CODENAME` | Initial development label; replaced by the release message when releasing |
| `BASE_DIR` | Literal `/opt/prod/<lowercase-name>` installation root |

The five version and CMDB strings must be nonempty, at most 255 characters, and contain no control characters. CMDB parses literal values at module or class scope without importing the file. Computed expressions, imported values, and environment lookups are unsuitable for these fields. The scanner requires only `VERSION`; BMForge requires the complete metadata above.

## Declare Persistent Data

Use empty tuples when the project has no filesystem data components or databases. Otherwise declare literal `(name, value)` pairs, as in MyCount:

```python
CMDB_COMPONENTS = (("Marketing Screenshots", "pages/marketing"),)
CMDB_DATABASES = (("MyCount", "mycount"),)
```

Component paths may be relative to the installation root or absolute. Names are limited to 255 characters and paths to 4096; parent traversal and the relative path `.` are unsupported. These declarations make filesystem components available for CMDB inventory and backup scheduling. Discovery records the declaration without checking that the path exists.

Database pairs identify an application connection label and the exact, case-sensitive MariaDB catalog name, limited to 64 characters. CMDB creates new connections only for catalogs observed on that same host. Missing catalogs and failed reads retain prior connections.

## Verify Discovery

Copy the [metadata checker]({{ '/templates/project/scripts/check-cmdb.py' | relative_url }}) to `scripts/check-cmdb.py`. From the project root, run it with the project's actual name and path:

```sh
python3 -B scripts/check-cmdb.py --name MyCount mycount/constants/DMyCount.py
```

For an installation, use `--root /opt/prod/mycount` with the same relative constants path. The local check validates the metadata and declared paths; it does not contact CMDB or prove remote access.

Deploy the constants file as readable Python source at the derived path, even if the executable is bundled. The `cmdbagent` account needs directory traversal and file read access. Keep credentials in separate protected configuration files.

Provide the required [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) to deploy, update, and remove the local installation consistently.

After installation, register the application, run an application scan, and verify the host, version, subtype, supplier, codename, and declared data components. `CMDB_CODENAME` is stored as the release's `VERSION_CODENAME` tag. A release publication and a verified installation are separate outcomes.

---

[Back]({{ site.baseurl }}{% link index.md %})
