配置miniconda
```
# conda create -p [PATH]
```
- creatre conda env at given PATH

``` bash
conda env list
conda info -e
```

conda problem:
couldn't activate conda environment in windows terminal.
WHY?
according to a webpage, do
```bash
conda init
```
but of no use

清华源
```
pip install torch==1.10.1 torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

setuptools降级
```
pip install --upgrade setuptools==57.5.0
```