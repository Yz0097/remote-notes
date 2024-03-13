#coding
## 哈希容器
### 1.set; unordered_set
只能使用迭代器进行访问
### 2.map; unordered_map
```cpp
//注意 pair first second 的用法
map <int,int> exp{pair(0,1)};
auto i = exp.begin();
cout<<i->first;    //0
cout<<i->second;   //1
```

## 数组
### 队列
- deque 
```cpp
//deque options
deque <int> q;
q.push(int);
q.pop();
q.front();
```

# 容器适配器
可以理解为基础类型的派生类

  容器适配器   | functions
:------- :| :-----:
stack  | empty,size,push,pop,top,emplace,swap(stack<T>,stack<T>)
queue  |  empty, size,front,back,push,emplace,push,pop,swap
priority_queue  | $1




table example    

| Column 1 | Column 2  |	Column 3 |
|:--------| :---------:|--------:|
| centered 文本居左 | right-aligned 文本居中 |right-aligned 文本居右|

# 排序队列

priority_queue   
```cpp
class mycomparison {
public:
    bool operator()(const pair<int, int>& lhs, const pair<int, int>& rhs) {
        return lhs.second > rhs.second;
    }
};
priority_queue<pair<int,int>, vector<pair<int,int>>, mycomparison> q;

```

这里的比较函数选用了大于，维护了一个小顶堆，pop时会弹出最小的元素。

