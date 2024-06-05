import os
import sys
import threading


# 功能：用于函数跟踪，结果存放在call_relations列表
# 参数：
# 返回值：
# 2024.03.24
# 使用示例：
#     ignored_modules = {'re', 'subprocess', 'sre_compile', 'sre_parse', 'sre_constants'}  # 忽略标准库和第三方库
#     call_relations = []
#     sys.settrace(
#         lambda frame, event, arg: enhanced_trace_calls_with_modules(frame, event, arg, call_relations, ignored_modules))
#
#     # 此处放被跟踪的业务逻辑
#
#     sys.settrace(None)
#     with open('自定义跟踪文件名.log', 'w') as file:
#         for relation in call_relations:
#             print(relation, file=file)
def enhanced_trace_calls_with_modules(frame, event, arg, call_relations, ignored_modules):
    if event != 'call':
        return
    pid = os.getpid()  # Get current process id
    tid = threading.get_native_id()  # Get current thread id

    caller_frame = frame.f_back
    caller_module = caller_frame.f_globals['__name__'] if caller_frame else 'main'
    callee_module = frame.f_globals['__name__']

    # Skip calls from ignored modules
    if caller_module in ignored_modules or callee_module in ignored_modules:
        return

    caller_name = caller_frame.f_code.co_name if caller_frame else 'main'

    if 'self' in caller_frame.f_locals:
        caller_class = caller_frame.f_locals['self'].__class__.__name__
        caller_name = f"{caller_class}.{caller_name}"

    callee_name = frame.f_code.co_name
    if 'self' in frame.f_locals:
        callee_class = frame.f_locals['self'].__class__.__name__
        callee_name = f"{callee_class}.{callee_name}"

    relationship = f"{pid}-{tid}: {caller_module}.{caller_name} -> {callee_module}.{callee_name}"
    call_relations.append(relationship)
    return lambda f, e, a: enhanced_trace_calls_with_modules(f, e, a, call_relations, ignored_modules)


def enhanced_trace_calls(frame, event, arg, call_relations, ignored_modules):
    if event != 'call':
        return
    pid = os.getpid()  # Get current process id
    tid = threading.get_native_id()  # Get current thread id

    caller_frame = frame.f_back
    caller_module = caller_frame.f_globals['__name__'] if caller_frame else 'main'
    callee_module = frame.f_globals['__name__']

    # Skip calls from ignored modules
    if caller_module in ignored_modules or callee_module in ignored_modules:
        return

    caller_name = caller_frame.f_code.co_name if caller_frame else 'main'

    if 'self' in caller_frame.f_locals:
        caller_class = caller_frame.f_locals['self'].__class__.__name__
        caller_name = f"{caller_class}.{caller_name}"

    callee_name = frame.f_code.co_name
    if 'self' in frame.f_locals:
        callee_class = frame.f_locals['self'].__class__.__name__
        callee_name = f"{callee_class}.{callee_name}"

    relationship = f"{pid}-{tid}: {caller_name} -> {callee_name}"
    call_relations.append(relationship)
    return lambda f, e, a: enhanced_trace_calls(f, e, a, call_relations, ignored_modules)


def filter_call_relations(call_relations):
    filtered_relations = []
    prev_relation = None
    repeat_count = 0

    for relation in call_relations:
        if relation == prev_relation:
            if repeat_count < 1:  # Allow one repetition
                filtered_relations.append(relation)
                repeat_count += 1
        else:
            repeat_count = 0
            prev_relation = relation
            filtered_relations.append(relation)

    return filtered_relations


