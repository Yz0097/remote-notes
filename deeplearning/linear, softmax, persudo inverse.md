#deep_learning #python #coding
# 1 线性回归
pytorch official toutrial
### 1 generate dataset
```Python
def synthetic_data(w, b, num_examples):  #@save
    """生成y=Xw+b+噪声"""
    X = torch.normal(0, 1, (num_examples, len(w)))
    y = torch.matmul(X, w) + b
    y += torch.normal(0, 0.01, y.shape)
    return X, y.reshape((-1, 1))

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 1000)
```

### 2 data iter
分批次读取batch_size个样本
```Python
w = torch.normal(0,0.01,size=(2,1),requires_grad=True)
b = torch.zeros(1,requires_grad=True)
def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    # 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        batch_indices = torch.tensor(
            indices[i: min(i + batch_size, num_examples)])
        yield features[batch_indices], labels[batch_indices]
```

使用torch中的data方法：
```Python
from torch.utils import data

def load_arrary(datainput, batch_size, is_train=True):
    data_set = data.TensorDataset(*datainput)
    return data.DataLoader(data_set, batch_size, shuffle=is_train)

data_iter = load_arrary((features2,labels2), batch_size)
```

调用：
```Python
for Features, Labels in data_iter:
	pass
```
or:
```Python
for X, y in data_iter:
	pass
```
### 3 线性回归
```Python
def linreg(X,w,b):
    return torch.matmul(X,w) + b

def squared_loss(y_hat, y):
    return (y_hat - y.reshape(y_hat.shape))**2/2

def sgd(params, learning_rate, batch_size):
    with torch.no_grad():
        for param in params:
            param -= learning_rate * param.grad / batch_size
            param.grad.zero_()

for epoch in range(num_epochs):
	for X, y in data_iter(batch_size, features, labels):
		l = squared_loss(linreg(X, w, b), y)
		l.sum().backward()
		sgd([w,b], learning_rate, batch_size)
		with torch.no_grad():
			tmp_l = squared_loss(linreg(features,w,b),labels)
			print(f'epoch {epoch}, loss {tmp_l.mean():f}')

```
使用torch封装
```Python
from torch import nn
from torch.utils import data

net = nn.Sequential(nn.Linear(features2.shape[1],1))
net[0].weight.data.normal_(0,0.01)
net[0].bias.data.fill_(0)

loss = nn.MSELoss()

trainer = torch.optim.SGD(net.parameters(), lr = learning_rate)

for epoch in range(num_epochs):
    for X,y in data_loaded:
        l = loss(net(X),y)
        trainer.zero_grad()
        l.backward()
        trainer.step()
    l=loss(net(features2),labels2)
    print(f'epoch {epoch}, loss {l:f}')
    print(net[0].weight,net[0].bias)
```
