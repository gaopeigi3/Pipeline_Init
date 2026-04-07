from pathlib import Path
import shutil
import argparse



def render_template(template_path, output_path, context):
    content = template_path.read_text()

    for key, value in context.items():
        content = content.replace(f"__{key}__", value)

    output_path.write_text(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    project_name = args.name
    root = Path(project_name)

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

    context = {
        "PROJECT_NAME": project_name
    }

    render_template(
        template_dir / "config.yaml",
        root / "config/config.yaml",
        context
    )
    render_template(
        template_dir / "Snakefile",
        root / "Snakefile",
        context
    )

    print(f"✅ Project created: {project_name}")

if __name__ == "__main__":
    main()