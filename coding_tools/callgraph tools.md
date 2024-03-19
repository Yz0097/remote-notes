# code2flow
静态代码检查，根据代码绘制类、函数图像     
命令行调用：  
```
code2flow filename.py
```

# pycallgraph
动态绘制函数调用图。程序调用函数时记录，最后绘制一个图像。    
官方文档：命令行（调用失败）
```
pycallgraph graphviz -- ./filename.py
```

用moudle方法调用：
```Python
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from ttt import *

#ddd是你想绘制函数关系图的py文件
graphviz = GraphvizOutput(output_file=r'./ttt.png')
#这里直接输入ddd.py里面的函数就可以直接绘制出来了，打开trace_detail.png就能看到了
with PyCallGraph(output=graphviz):
    test()
```

