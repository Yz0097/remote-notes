### Robust Communicative Multi-Agent Reinforcement Learning with Active Defense
主动防御
observation->classifer(estimate reliability) ->aggregation policy net

### Robust Deep Reinforcement Learning with Adversarial Attacks
在训练过程中加入敌对攻击, 提升算法对对应攻击的robustic
2018
三种类攻击模式

### Certifiably Robust Policy Learning against Adversarial Communication in Multi-agent Systems
理论分析证明, 利用恶意交流信息, message-ensemble policy, multiple randomly ablated message sets 2023

### Mis-spoke or mis-lead_ Achieving Robustness in Multi-Agent Communicative Reinforcement Learning against Adversarial Multi-Agent Communication with Adversarial Attacks
1. 用于生成恶意信息的模型
2. massage reconstruction 在攻击下使多智能体进行合作
3. 将恶意交流攻击建模为双方零和博弈, 提出基于博弈论的方法 R-MACRL, 改进最差情况下的防御表现
节点的策略包括行为策略和消息策略, 恶意节点包括第三个策略恶意策略, 是在消息空间中的一个行动.
恶意节点传出恶意消息, 恶意消息是原消息与恶意策略信息的组合, 恶意节点采取和原策略一样的行动来防止被发现.
一个时间步里所有消息的集合会被交流协议communication protocol处理为一个$m^{in}$,分发给每个节点



采用MACRL训练uav时, message space如何定义?


改进应该基于现有的baseline, 也就是无人机场景的rl算法需要有现有的实现, 否则应该做的就是实现前提条件

uav swarm 的尺度 10~100架  100架以上

与交流相关的强化学习算法一般恶意无人机的恶意策略只包括传输恶意的消息. 针对
恶意无人机可以作为stackberg博弈模型中的leader影响整体的策略

无人机集群 边缘计算 视频传输任务 
无人机集群拓扑结构的变化和空间中的信号干扰

在