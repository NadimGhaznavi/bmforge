"""Initialize, check, or update deployment history using project policy."""

import argparse
from importlib import import_module
from pathlib import Path

from deployment_tools.DeploymentConfig import DeploymentConfig
from deployment_tools.DeploymentImpact import DeploymentImpact
from deployment_tools.ReleaseDeployment import ReleaseDeployment
from deployment_tools.ReleaseFiles import ReleaseFiles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Project module exposing CONFIG")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("initialize", "check"):
        commands.add_parser(name).add_argument("version")
    for name in ("prepare", "upgrade"):
        command = commands.add_parser(name)
        command.add_argument("previous")
        command.add_argument("version")
    commands.add_parser("manifest")
    args = parser.parse_args()
    try:
        config = import_module(args.config).CONFIG
        if not isinstance(config, DeploymentConfig):
            raise ValueError("Project CONFIG must be a DeploymentConfig")
        files = ReleaseFiles(Path.cwd(), config)
        if args.command == "manifest":
            print(config.manifest)
        elif args.command == "initialize":
            if (files.checkout / config.manifest).exists():
                raise ValueError("Deployment history already exists; do not reset it")
            if files.installed_version(files.checkout) != args.version:
                raise ValueError("Initial version must match the project constants")
            impact = DeploymentImpact(config.targets, config.dependencies)
            files.write({"releases": [{"version": args.version, "targets": []}], "artifacts": {
                name: {"digest": digest, "targets": sorted(impact.affected_targets(name))}
                for name, digest in files.snapshot().items()}})
            print("Initialized deployment history.")
        elif args.command == "check":
            if files.read()['releases'][-1]['version'] != args.version:
                raise ValueError("Release baseline does not match the current version")
            files.snapshot()
            print("Deployment history and inputs are ready.")
        else:
            releases = ReleaseDeployment(files)
            if args.command == "prepare":
                if files.installed_version(files.checkout) != args.version:
                    raise ValueError("Prepared version must match the project constants")
                targets = releases.prepare(args.previous, args.version)
            else:
                targets = releases.upgrade_targets(args.previous, args.version)
            print("\n".join(sorted(targets)))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, ImportError, SyntaxError) as error:
        parser.exit(1, f"Deployment check failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
