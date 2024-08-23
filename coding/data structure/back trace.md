# 回溯算法
## 回溯算法的一般格式
```cpp
vector</*datatype*/> res;
/*datatype*/ path;
void traceback(/*回溯参数*/){
	if(/*终止条件*/){
		res.push_back(path);
		return;
	}
	
	for(/*按层遍历*/){
		//插入
		traceback(/*更新回溯参数*/);
		//回退插入内容(回溯)
	}
}
```

需要注意在终止条件前后仍然操作path时, 在`res.push_back(path)`之后仍然需要维护path. 相当于回溯过程中的回退插入内容.
例子: https://leetcode.cn/problems/restore-ip-addresses/
```cpp
        if(s.size() != 1 && s[0]=='0')
            return false;
        int num = 0;
        for(int i =0;i<s.size();i++){
            if(s[i]<'0'||s[i]>'9')
                return false;
            num = num * 10 + (s[i]-'0');
            if(num > 255)
                return false;
        }
        return true;

    }
    void traceback(string &s, int idx, int num_dot/*回溯参数*/){
        if(num_dot == 3/*终止条件*/){
            string tmp = "";
            for(int i = idx; i < s.size();i++){
                tmp.push_back(s[i]);
            }

            if(is_valid(tmp)){
	            //插入
                path.append(tmp);
                //保存path
                res.push_back(path);
                //1.维护一个全局的path;
                //2.在终止之前仍然对path进行操作,且回溯返回后仍然使用path
                //回退插入内容(回溯)
                for(int i = 0;i<tmp.size();i++){
                    path.pop_back();
                }
                return;
            }else
                return;
        }
        string tmp = "";
        for(int i = idx; i < s.size() && i < idx+3; i++/*按层遍历*/){
            
            tmp.push_back(s[i]);
            if(is_valid(tmp)){
                //插入
                path.append(tmp+".");

                traceback(s, i+1, num_dot+1);

                //回退插入内容(回溯)
                for(int j = 0; j < tmp.size()+1;j++){
                    path.pop_back();
                }
            }
        }
    }
    vector<string> restoreIpAddresses(string s) {
        traceback(s, 0, 0);
        return res;
    }
};
```