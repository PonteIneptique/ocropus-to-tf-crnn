Ocropus data to TF-CRNN implementation
======================================

![Python 3](https://img.shields.io/badge/python-3-green.svg)
![Mozilla Public License V2.0](https://img.shields.io/badge/license-MPL2-blue.svg)

This small script is meant to be used if you have some manuscripts data and you want
to try out Sofia Ares Oliveira's implementation of TF-CRNN ( https://github.com/solivr/tf-crnn
for more details)

# Use

This script is a single file script at the moment and we hope to keep it this way.
Download or clone the directory beforehand. You can also simply copy the content of
[`cli.py`](cli.py) and save it where you need it.

To use it, you can do :

```bash
python3 cli.py my_ocropus_data_directory --output tf-crnn
```

**This will create a file "groundtruth.csv" in the directory
`./tf-crnn/my_ocropus_data_directory`.** The image file links are
absolute path, which allows to move your groundtruth
file to be moved along.

The command accepts also multiple directory and unix-selectors for
the input directories.

```bash
python3 cli.py ocropus/train  ocropus/test --output tf-crnn
# Same as
python3 cli.py ocropus/* --output tf-crnn
```

Both these commands will create files in `tf-crnn/train` and
`tf-crnn/test` named `groundtruth.csv`.

