"""Adapt paths and targets to the project's actual deployment."""

from deployment_tools.DeploymentConfig import DeploymentConfig
from deployment.DependencyMap import DEPENDENCIES, TARGETS


CONFIG = DeploymentConfig(
    targets=TARGETS,
    dependencies=DEPENDENCIES,
    manifest="deployment/releases.json",
    version_marker=".deployment-version",
    version_file="__PROJECT_SLUG__/constants/D__PROJECT_NAME__.py",
    version_pattern=rb'(    VERSION: Final\[str\] = )"[^"\n]+"',
    scan_roots=("__PROJECT_SLUG__",),
    package_roots=("__PROJECT_SLUG__",),
    setup_files=(),
    full_setup_target="filesystem",
)
