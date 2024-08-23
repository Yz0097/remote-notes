# 回溯算法
## 回溯算法的一般格式
```cpp
vector</*datatype*/> res;
/*datatype*/ path;
void traceback(/*回溯参数*/){
	if(/*中止条件*/){
		res.push_back(path);
		return;
	}
	
	for(/*按层遍历*/){
		//插入
		traceback(/*更新回溯参数*/);
		//回退插入内容
	}
}
```