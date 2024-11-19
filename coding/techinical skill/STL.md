#coding #hash #cpp
## 哈希容器
[[hash]]
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
map中是否包含了某个数字,例：
```cpp
unordered_map <int,int> exp{pair(0,1), pair(1,2)};
exp.count(0) //输出
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

| 容器适配器 |                        functions                        |     |
| :---: | :-----------------------------------------------------: | --- |
| stack | empty,size,push,pop,top,emplace,swap(stack<T>,stack<T>) |     |
queue  |  empty, size,front,back,push,emplace,push,pop,swap
priority_queue  | 





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


# vector
## vector初始化
```cpp
vector<bool> used(size/*int size*/, false/*datatype initial_val*/);
```


### 清空vector
```cpp
vector<int> test(5);

//1 占用内存不变
test.clear();

//2 内存不变
for(auto i = test.begin(); i!= test.end(); i++){
	test.erase(i);
}

//3 释放内存
vector<int> ().swap(test);
```


# string
string一样适用大量的stl相关操作，例如：
```cpp
sting s = "abc";
s.push_back('d');//此时s = "abcd"
s.pop_back();//s = "abc", 返回值应为'd'
```
特别的有取子串操作：
```cpp
sting s = "abc";
int start = 0;
int end = 1;
string tmp = s.substr(start, end - start + 1);
tmp = "a";
```
`substr`方法，第一个参数开始下标，第二个参数为子串长度
				
cpp中, 字符串可以使用运算符`+`进行操作, 使用`append`方法与运算符`+=`相同
```cpp
string a = "aaa";
string b = "bbb";

string ab = a + b;//ab = "aaabbb"
a += b; //a = "aaabbb"
a.append(b); // a = "aaabbbbbb";
```
- `+`方式本质是 `s = new StringBuilder(s).append("a") .toString();`