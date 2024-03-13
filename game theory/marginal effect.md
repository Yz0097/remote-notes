#crowdsensing    #game_theory  

在[[zhanFreeMarketMultiLeader2020]] 中设定payoff函数时，注意到两项：
$$\begin{align}
\phi_m(\sigma_m)&=\mu_mlog(1+\sigma_m)\\
C_m^n(t_m^n)&=a_m^n{t_m^n}^2+b_m^nt_m^n
\end{align}$$   
设计TI的收益函数的正项，即数据总价值时，使用了函数$f(x)= log(1+x)$ 。正是由于其数据总价值的边际递减效应。对应到函数的设计上，体现在：    
1. $f'(x)>0$ 函数递增
2. $f''(x)<0$ 函数的二阶导数小于0，即一阶导$f'(x)$单调递减，函数$f(x)$的增量不断减小
同样的，对于边际效应递增的函数，就对应的设计为一个二次函数。   
值得思考的是，同时满足$f'(x)<0,f''(x)>0$ 的函数远不止$log(1+x)$这样一个例子，具体该如何选取呢