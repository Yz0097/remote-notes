#reinforced_learning 
multiple agent double deep policy gradiant is used in [[zhanFreeMarketMultiLeader2020]] to do DRL.   
MADDPG为每个智能体维护critic network和actor network。智能体之间没有分工，也很难谈得上有合作关系。但是一般的，如果每个智能体之间使用相同的reward函数，可以称他们是相互合作的。   
MADDPG的问题在于为了维护2n个神经网络每一步迭代的开销都是很大的。