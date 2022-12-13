# Heptabase-Export
This repo contains two simple python scripts which can imporve the performance of exporting from Heptabase data.

There are two parts you should change before using this script.
1. Change line 4 `All-Data.json path here` to your `All-Data.json` file path.
2. Change line 33 `export path here` to your export folder path.

`Heptabase_clean` will read your `All-Data.json` file and create all untrashed cards to markdown file in the folder you want. In addition, it will also change all the Heptabase bi-directional link to normal '[[]]' link in order to match the format of other note-taking applications such as obsidian logseq etc.

if you want to keep your Heptabase whiteboard layout, `Hepta2obcanvas.py` can help you using Heptabase data to create obsidian canvas file.
There is only one part you shoule change before using this script.
1. Change line 6 `your All-Data.json path here` to your `All-Data.json` file path.

This script will automatically create each of whiteboards you have in Heptabase to a single obsidian canvas file. This script can not create the connections in whiteboard due to the limitation of Heptabase exporting data. 


---
这个 repo 只有一个简单的 python 脚本，可以提高从 Heptabase 数据导出的表现。

在使用这个脚本之前，有两个部分你应该改变。
1. 将第4行 `All-Data.json path here `改为你的 `All-Data.json`文件路径。
2. 将第33行`export path here`改为你的导出文件夹路径。

脚本将读取你的`All-Data.json`文件，并在你想要的文件夹中创建所有未删减的卡片为 `markdown` 文件。此外，它还会把所有Heptabase的双向链接改为正常的"[[]]"链接，以便与其他笔记软件的格式相匹配，如 obsidian logseq 等等。

如果你想保留你的Heptabase白板布局，`Hepta2obcanvas.py`可以帮助你使用Heptabase数据来创建 Obsidian Canvas 文件。
在使用这个脚本之前，你只需要改变一个部分。
1. 将第6行`你的All-Data.json路径在这里`改为你的`All-Data.json`文件路径。

这个脚本将自动创建你在 Heptabase 中的每个白板成一个 obsidian canvas 文件。由于Heptabase导出数据的限制，这个脚本不能在 Canvas 中创建连接。


