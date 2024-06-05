from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
 
from ttt import *
#ddd是你想绘制函数关系图的py文件
graphviz = GraphvizOutput(output_file='xxx.gv', output_type='dot')
#这里直接输入ddd.py里面的函数就可以直接绘制出来了，打开trace_detail.png就能看到了
with PyCallGraph(output=graphviz):
    test()
