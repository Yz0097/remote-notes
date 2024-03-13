#coding  
```cpp
class Solution {
public:
	vector<vector<int>> threeSum(vector<int>& nums) {    
		set<vector<int>> res;
		sort(nums.begin(),nums.end());//注意对原数组排序
		for(int i=0;i<nums.size()-2;i++){
			if(nums[i]>0){//去重，当三指针第一位超过0时，不可能和为0
				break;
			}
			
			int p1 = i+1,p2 = nums.size()-1;
			while(p1<p2){//双指针
				int sum = nums[i]+nums[p1]+nums[p2];
				if(sum == 0 ){
					res.insert(vector<int>{nums[i],nums[p1],nums[p2]});
					p1++;
					p2--;
				}else if(sum<0){
					p1++;
				}else if(sum>0){
					p2--;
				}
			}
		}
		
		vector<vector<int>> res1;
		for(auto i = res.begin();i!=res.end();i++){
			res1.push_back(*i);
		}
		return res1;
	}
};
```
使用了哈希方法，发现开销极大![[Pasted image 20230828012842.png]]
但是好像测试的问题并不在此。在添加了第二部分去重后，用时已经不是一个数量级了
```cpp
if(i>0&& nums[i]==nums[i-1]){//第二种去重，针对数列中的重复元素
	continue;
}
```
![[Pasted image 20230828013559.png]]
当然，对于这一题，最好还是节约使用哈希容器的额外空间开销，只使用双指针也可以完成该题，虽然时间复杂度保持$O(n^2)$，但是空间复杂度由$O(n)+hash\_set$变为了$O(1)$。  

当sum==0的情况下，应当采用这样的去重方式避免使用哈希容器：
```cpp
if(sum == 0 ){
	res.push_back(vector<int>{nums[i], nums[p1], nums[p2]});
	// 去重逻辑应该放在找到一个三元组之后，对b 和 c去重
	while (p2 > p1 && nums[p2] == nums[p2 - 1]) p2--;
	while (p2 > p1 && nums[p1] == nums[p1 + 1]) p1++;
	// 找到答案时，双指针同时收缩
	p2--;
	p1++;
}
```
运行结果：![[Pasted image 20230828014334.png]]
~~虽然leetcode的测试仅供参考~~

# 