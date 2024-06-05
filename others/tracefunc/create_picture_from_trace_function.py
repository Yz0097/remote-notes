import re
from graphviz import Digraph
from RegEx import edgeFuncCallsLine


def create_graph_from_trace_function(log_file_path, save_path):
    # 创建一个有向图，尝试不同的布局引擎如'sfdp'，'neato'，或者保留'dot'但改变排列方向
    dot = Digraph(comment='The Function Call Graph', engine='dot')
    dot.attr(rankdir='LR')  # 从左到右的布局

    # 读取日志文件
    i = 1
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.search(edgeFuncCallsLine, line)
            if match:
                # 提取信息
                pid, tid, caller_class, caller_func, callee_class, callee_func = match.groups()
                # 构造唯一的节点ID
                caller = f"{caller_class}.{caller_func}"
                callee = f"{callee_class}.{callee_func}"
                # 添加节点和边到图中
                dot.node(caller, f"{caller}")
                dot.node(callee, f"{callee}")
                dot.edge(caller, callee, f"call_id: {i}\nPID:{pid}, TID:{tid}")
                i += 1

    # 渲染图形到文件，保存为SVG格式，同时保留.gv源文件
    output_filename = save_path
    dot.render(output_filename, format='svg', view=True)


def create_graph_from_trace_function_default(log_file_path, save_path):
    # 创建一个有向图，尝试不同的布局引擎如'sfdp'，'neato'，或者保留'dot'但改变排列方向
    dot = Digraph(comment='The Function Call Graph', engine='dot')

    # 读取日志文件
    i = 1
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.search(edgeFuncCallsLine, line)
            if match:
                # 提取信息
                pid, tid, caller_class, caller_func, callee_class, callee_func = match.groups()
                # 构造唯一的节点ID
                caller = f"{caller_class}.{caller_func}"
                callee = f"{callee_class}.{callee_func}"
                # 添加节点和边到图中
                dot.node(caller, f"{caller}")
                dot.node(callee, f"{callee}")
                dot.edge(caller, callee, f"call_id: {i}\nPID:{pid}, TID:{tid}")
                i += 1

    # 渲染图形到文件（默认为PDF格式）
    output_filename = save_path
    dot.render(output_filename, format='svg', view=True)


if __name__ == '__main__':
    log_file_path = '0325fly/test_func_calls.log'
    save_path = '0325fly/test_func_calls_graph.gv'
    create_graph_from_trace_function(log_file_path, save_path)
