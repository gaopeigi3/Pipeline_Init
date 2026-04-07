把“项目初始化”和“数据流程执行”解耦

我直接用最直白的话讲：

🧩 这两行在干嘛？
shutil.copy(template_dir / "Snakefile", root / "Snakefile")
shutil.copy(template_dir / "config.yaml", root / "config/config.yaml")

👉 本质只有一句话：

把“模板文件”复制到新项目里

🧠 拆开讲（逐字理解）
第一行
shutil.copy(template_dir / "Snakefile", root / "Snakefile")

意思是：

👉 从这里复制：

templates/basic/Snakefile

👉 到这里：

你的新项目/Snakefile
第二行
shutil.copy(template_dir / "config.yaml", root / "config/config.yaml")

意思是：

👉 从：

templates/basic/config.yaml

👉 复制到：

你的新项目/config/config.yaml
📦 用现实类比（很重要）

你可以把 templates/basic/ 想成：

📁 一个“项目模板仓库”

里面放着：

标准 Snakefile
标准 config.yaml

当你运行：

python create_project.py --name test

其实发生的是：

👉 复制一套“空白模板项目”给你

就像：

cp -r template_project new_project

但你是程序化地复制（更灵活）

🔥 为什么要这样做（核心思想）

如果不用 copy，你会：

❌ 每次手写 Snakefile
❌ 每次写 config.yaml
❌ 很容易写错

用了模板：

✔ 每个项目结构一致
✔ 不用重复写
✔ 可以不断升级模板

⚠️ 一个你必须理解的关键点

你现在做的是：

❌ 不是在“写 pipeline”
✅ 而是在“造 pipeline 的模板”

🧠 再往深一层（你已经快到这一步了）

以后你可以做：

Snakefile_template.replace("__PROJECT_NAME__", args.name)

👉 自动改内容

甚至：

project: AML

👉 自动写进去

🧠 一句话总结

这两行代码的本质是：

用模板复制，代替手动创建文件

🔥 如果你再往前走一步（我建议）

你可以试试这个改动：

👉 不复制，而是“生成文件”

(root / "Snakefile").write_text("...")
那什么时候用 copy，什么时候 write？
场景	用什么
文件很简单	write_text
文件复杂（Snakemake）	copy ✅