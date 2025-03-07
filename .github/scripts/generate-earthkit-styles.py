#!/usr/bin/env python3

import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def main():
    # Load configuration files
    styles_config = load_yaml("config/styles.yml")
    identities_config = load_yaml("config/cads-definitions.yml")

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("src/templates"), trim_blocks=True, lstrip_blocks=True
    )

    # Create output directories if they don't exist
    Path("src/cams/styles").mkdir(parents=True, exist_ok=True)
    Path("src/cams/identities").mkdir(parents=True, exist_ok=True)

    # Load templates
    style_template = env.get_template("styles/style-template.yml")
    identity_template = env.get_template("identities/identity-template.yml")

    # Process each variable
    for var_name, style_config in styles_config.items():
        # Find matching identity config
        identity_config = next(
            (
                item
                for item in identities_config
                if item["frontend_api_name"] == var_name
            ),
            None,
        )

        if not identity_config:
            print(f"Warning: No identity configuration found for {var_name}")
            continue

        # Generate style file
        style_content = style_template.render(name=var_name, **style_config)
        with open(f"src/cams/styles/{var_name}.yml", "w") as f:
            f.write(style_content)

        # Generate identity file
        identity_content = identity_template.render(**identity_config)
        with open(f"src/cams/identities/{var_name}.yml", "w") as f:
            f.write(identity_content)

        print(f"Generated files for {var_name}")


if __name__ == "__main__":
    main()
