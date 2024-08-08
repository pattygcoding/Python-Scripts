# Python Scripts by Patrick Goodwin

## Table of Contents
- [Compare Diff](#compare-diff)
- [Count Files](#count-files)

## Compare Diff

This script compares two files line by line and highlights the differences. It also has an optional feature to ignore timestamps during the comparison.

### Arguments
- `file1`: The first file to compare. Defaults to `TestFile1.txt`.
- `file2`: The second file to compare. Defaults to `TestFile2.txt`.
- `--notime`: Optional flag to remove timestamps before comparing.

### Example Usage
```
python compare_diff.py file1.txt file2.txt
```

## Count Files

This script counts the number of files in the current directory and its subdirectories. It can optionally exclude the `node_modules` directory.

### Arguments

- `--includenode`: Include files in the `node_modules` directory.

### Example Usage
```
python count_files.py
```
