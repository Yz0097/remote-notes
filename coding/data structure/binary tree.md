# 二叉树的存储方式
## 链式存储
## 顺序存储

parent node with num $i$, and its child nodes are $2i+1\quad and \quad   2i+2$
![[QQ20231020115316.png]]

如果二叉树并非满二叉树，会浪费存储空间

# 二叉树的性质

## 遍历一颗二叉树

### 前、中、后序遍历
#### 前序一般迭代

```cpp
vector<int> preorderTraversal(TreeNode* root) {
	stack<TreeNode*> st;
	vector<int> res;
	if(root) st.push(root);
	while(!st.empty()){
		TreeNode *cur = st.top();
		st.pop();
		res.push_back(cur->val);
		if(cur->right) st.push(cur->right);
		if(cur->left) st.push(cur->left);
	}
	return res;
}
```

#### 后序迭代

将前序迭代的中左右改为中右左，再将顺序反转得到后序迭代。     

#### 中序迭代的一般写法：

将访问与处理分开，利用一个指针进行访问

```cpp
vector<int> inorderTraversal(TreeNode* root) {
	TreeNode *cur = root;
	stack<TreeNode*> st;
	vector<int> res;

	while(nullptr != cur || !st.empty()){
		if(cur){//visit
			st.push(cur);
			cur = cur->left;
		}else{//deal
			cur = st.top();
			st.pop();
			res.push_back(cur->val);
			cur = cur->right;
		}
	}
	return res;
}
```
#### 统一迭代的写法

Node+NULL表示节点已经访问过待处理       
Node后没有NULL表示节点待访问

```cpp
//
vector<int> postorderTraversal(TreeNode* root) {
	vector<int> res;
	stack<TreeNode*> st;
	if(nullptr != root) st.push(root);
	TreeNode *tmp = root;
	while(!st.empty()){
		tmp = st.top();
		if(nullptr != tmp){
			//mid, right, left
			st.push(nullptr);
			if(nullptr != tmp->right) st.push(tmp->right);
			if(nullptr != tmp->left) st.push(tmp->left);
			tmp = st.top();
		}else{
			st.pop();
			tmp = st.top();
			st.pop();
			res.push_back(tmp->val);
		}
	}
	return res;
}
```

### 层序遍历

按层遍历二叉树，

## 完全二叉树 

深度为n的满二叉树，节点个数为$2^n -1$

### 求完全二叉树节点个数

以某一节点作为根节点，遍历其左右两条边，若深度相等，则无需遍历其内部的节点，可以判定为一个满二叉树。

- leetcode 222

## 二叉树的深度和高度

### depth

从根节点到当前节点的距离。    
使用前序遍历求得(回溯法)

```cpp
int get_depth(Node* cur, int depth){
	//mid
	cur->depth = depth;
	if(cur->left){//left
		depth++;
		get_depth(cur->left, depth);
		depth--;
	}
	if(cur->right){//right
		depth++;
		get_depth(cur->right, depth);
		depth--;
	}
	return depth;
}
```

### height

从当前节点到叶子节点的距离。      
使用后序遍历求得   

```cpp

```

------
二叉树的最大深度 = 根节点的最大高度

