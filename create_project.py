from datetime import datetime
import os
from pathlib import Path
import shutil
import argparse
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import getpass
from pathlib import Path
import argparse
from jinja2 import Environment, FileSystemLoader


def render_template(env, template_name, output_path, context):
    try:
        template = env.get_template(template_name)
        output = template.render(context)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")

    except Exception as e:
        print(f"❌ Error rendering {template_name}: {e}")
        raise

def build_context(template_name, project_name):
    base = {
        "PROJECT_NAME": project_name,
        "DATE": datetime.now().strftime("%Y-%m-%d"),
    }

    if template_name == "geneformer":
        base.update({
            "USE_TOKENIZER": True,
            "MODEL_VERSION": "V1",
        })

    elif template_name == "scrna":
        base.update({
            "USE_HARMONY": True,
            "N_PCS": 50,
        })

    return base

def process_template_dir(env, template_dir, output_root, context):
    for path in template_dir.rglob("*"): #目录结构必须属于 template，通过此函数创建
        if path.is_file():
            rel_path = path.relative_to(template_dir)

            if path.suffix == ".j2":
                output_path = output_root / rel_path.with_suffix("")
                render_template(env, str(rel_path), output_path, context)

            else:   #rglob("*") 只遍历文件，空目录不会被复制，必须在模板里加：.gitkeep
                output_path = output_root / rel_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(path, output_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--template", default="basic")
    parser.add_argument("--output_dir", default="..")
    args = parser.parse_args()

    project_name = args.name
    template_name = args.template

    output_base = Path(args.output_dir).resolve()
    root = output_base / project_name
    root.mkdir(exist_ok=True)

    template_root = Path(__file__).parent / "templates"
    template_dir = template_root / template_name

    if not template_dir.exists():
        raise ValueError(f"Template not found: {template_name}")

    env = Environment(
        loader=FileSystemLoader(template_dir),
        auto_reload=True
    )

    context = build_context(template_name, project_name)

    process_template_dir(env, template_dir, root, context)

    print(f"✅ Project created: {project_name} ({template_name})")






if __name__ == "__main__":
    main()