# Heptabase-Export
This repo contains a simple pythron script which can imporve the performance of the outcome of exporting from Heptabase data.

There are two part you should change before using this script.
1. Change line 4 'All-Data.json path here' to your 'All-Data.json' file path.
2. Change line 33 'export path here' to your export folder path.

The script will read your 'All-Data.json' file and create all untrashed cards to markdown file in the folder you want. In addition, it will also change all the Heptabase bi-dirctional link to normal [[]] link in order to match the format of other application such as obsidian logseq etc.
