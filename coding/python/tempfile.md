1. 创建tmpfile
```python
file = tempfile.NamedTemporaryFile()
```


2. 清空文件内容
```python
file.seek(0)
file.truncate()
```