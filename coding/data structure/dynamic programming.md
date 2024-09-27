#coding #dynamic_programming 
# 一般步骤
1. dp数组和下标的含义
2. 递推公式
3. 初始化
4. 遍历顺序
5. 举例推导

# 01背包问题
## 分类
|      |            |
| ---- | ---------- |
| 01背包 | 每种物品只有一个   |
| 完全背包 | 每种物品数量不限   |
| 多重背包 | 每种物品有数量限制` |
## 01背包

### 将其他问题转换为01背包问题
[代码随想录- 分割等和子集](https://programmercarl.com/0416.%E5%88%86%E5%89%B2%E7%AD%89%E5%92%8C%E5%AD%90%E9%9B%86.html#_416-%E5%88%86%E5%89%B2%E7%AD%89%E5%92%8C%E5%AD%90%E9%9B%86)
[对应力扣题目](https://leetcode.cn/problems/partition-equal-subset-sum/description/)

给你一个 **只包含正整数** 的 **非空** 数组 `nums` 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

**示例 1：**
```
输入: nums = [1,5,11,5]
输出: true
解释: 数组可以分割成 [1, 5, 5] 和 [11] 。
```

**示例 2：**
```
输入： nums = [1,2,3,5]
输出： false
```

关键代码：
采用滚动数组， 双重循环外层为物品序号，内层为背包容量，且背包容量反向遍历。
```cpp
vector<int> dp(sum +1,0);
for(int i=0; i<nums.size(); i++){
	for(int j = sum; j-nums[i]>=0; j--){
		dp[j] = max(dp[j], (dp[j - nums[i]] + nums[i]));
	}
}
```
注意循环中原本的`if(j>=nums[i]) dp[j] = max()`被写到了循环条件中。   

若不采用滚动数组，空间占用较大，二层循环无所谓先后，与dp的一、二维含义有关。
```cpp
vector<vector<int>> dp(weight.size(), vector<int>(bagweight + 1, 0));
for(int i = 1; i < weight.size(); i++) { // 遍历科研物品
	for(int j = 0; j <= bagweight; j++) { // 遍历行李箱容量
		if (j < weight[i]) dp[i][j] = dp[i - 1][j]; 
		// 如果装不下这个物品,那么就继承dp[i - 1][j]的值
		else {
			dp[i][j] = max(dp[i - 1][j], 
						   dp[i - 1][j - weight[i]] + value[i]);
		}
	}
}
```