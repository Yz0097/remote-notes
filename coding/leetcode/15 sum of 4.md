#coding
15 四数之和

```cpp
class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> res;
        sort(nums.begin(), nums.end());
        for(int i = 0; i < nums.size() - 3; i++){
            if(i >= 0 && target >= 0 && nums[i] >=target){
                break;
            }
            if(i > 0 && nums[i] == nums[i - 1]){
                break;
            }
  
            for(int j = i + 1;j < nums.size() - 2; j++){
                if(j >= 0 && target >= 0 && nums[j] >= target - nums[i]){
                    break;
                }
                if(j > i + 1 && nums[j] == nums[j - 1]){
                    break;
                }
                int p1 = j + 1, p2 = nums.size()-1;
  
                while(p1 < p2){
                    int sum = nums[i] + nums[j] + nums[p1] + nums[p2];
                    if(sum == target){
                        res.push_back(vector{nums[i], nums[j], nums[p1], nums[p2]});
                        while(p1 < p2 && nums[p1] == nums[p1 + 1]){
                            p1++;
                        }
                        while(p1 < p2 && nums[p2] == nums[p2 - 1]){
                            p2--;
                        }
                        p1++;
                        p2--;
                    }else if(sum < target){
                        p1++;
                    }else if(sum > target){
                        p2--;
                    }
                }
            }
        }
        return res;
    }
};

```


#### 1. 对i,j去重时的错误，应当采用continue
```cpp
if(i > 0 && nums[i] == nums[i - 1]){
	continue;//越过当前重复的数据直接进入下一组
}
```
#### 2. 剪枝条件错误
会导致无法通过测试[0,0,0,0]
![[Pasted image 20230828182741.png]]
```cpp
if(target >= 0 && nums[i] >target){
	break;
}
```
#### 3. 无法通过[0,0,0]
使用循环条件
```cpp
for(int i = 0; i < nums.size() - 3; i++)
```
当输入的nums数组长度小于3时，仍然会运行循环体，并且无法跳出循环。必须将条件中的`nums.size()`修改为一个int变量才行。不知道是不是力扣oj特有的问题：
```cpp
int len = nums.size();
for(int i = 0; i < len - 3; i++)
```

## 注意
三数之和、四数之和都不要忘记：首先对输入进行排序