from pathlib import Path
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    root = Path(args.name)

    folders = [
        "config",
        "docs",
        "notebooks",
        "workflow/rules",
        "data/raw",
        "data/interim",
        "data/tokenized",
        "results",
        "logs"
    ]

    for f in folders:
        (root / f).mkdir(parents=True, exist_ok=True)

    template_dir = Path(__file__).parent / "templates/basic"
    shutil.copy(template_dir / "Snakefile", root / "Snakefile")
    shutil.copy(template_dir / "config.yaml", root / "config/config.yaml")

    print(f"✅ Project created: {args.name}")

if __name__ == "__main__":
    main()