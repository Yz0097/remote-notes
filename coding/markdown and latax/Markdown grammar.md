#md 
# 格式 
## 空格

| 空格（1个字符位置）   | \\quad  |
| ------------ | ------- |
| 2个空格（2个字符位置） | \\qquad |
| 1/3          | a\\ b   |
| 2/7          | \\;     |
| 1/6          | \\,     |
| 挨近1/6        | \\!     |
换行：\\\

## 表格格式
```
| title1 | title2 |
|--------|--------|
| context|context|

/** 
in line 2: 
|:-----| 左对齐
|:-----:| 居中
|----:|
```


# 公式
## 正上方正下方的标注
$\arg\max\limits_j y_j = argmax\limits_j o_j$
$$\arg\max_n$$
$$\mathop{argmax}_n$$


`$\argmax\limits_j y_j = \argmax\limits_j o_j$`在vscode的juypter notebook里有效
$$\begin{displaymath}
\argmax_j y_j
\end{displaymath}$$

obsidian中的`$$ ... $$`环境相当于latex中的展示模式