from pathlib import Path
import shutil
import argparse

# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--name", required=True)
#     args = parser.parse_args()

#     root = Path(args.name)

#     folders = [
#         "config",
#         "docs",
#         "notebooks",
#         "workflow/rules",
#         "data/raw",
#         "data/interim",
#         "data/tokenized",
#         "results",
#         "logs"
#     ]

#     for f in folders:
#         (root / f).mkdir(parents=True, exist_ok=True)

#     template_dir = Path(__file__).parent / "templates/basic"
#     shutil.copy(template_dir / "Snakefile", root / "Snakefile")
#     shutil.copy(template_dir / "config.yaml", root / "config/config.yaml")

#     print(f"✅ Project created: {args.name}")

# if __name__ == "__main__":
#     main()





def render_template(template_path, output_path, context):
    content = template_path.read_text()

    # 替换变量
    for key, value in context.items():
        content = content.replace(f"__{key}__", value)

    output_path.write_text(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    project_name = args.name
    root = Path(project_name)

    # 1️⃣ 创建目录
    folders = [
        "config",
        "workflow/rules",
        "data/raw",
        "data/interim",
        "data/tokenized",
        "results",
        "logs"
    ]

    for f in folders:
        (root / f).mkdir(parents=True, exist_ok=True)

    # 2️⃣ 模板路径
    template_dir = Path(__file__).parent / "templates/basic"

    # 3️⃣ context（变量）
    context = {
        "PROJECT_NAME": project_name
    }

    # 4️⃣ 渲染文件（重点）
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