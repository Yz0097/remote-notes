

# 1、在intel devCloud 平台上，测试MPI不同通信模式代码并解释其效果；
## 点对点通信
阻塞：MPI_Send MPI_Recv
```cpp
int MPI_Send(void *buffer, int count, MPI_Datatype, int dest, int tag, MPI_Comm);

int MPI_Recv(void *buffer, int count, MPI_Datatype, int source, int tag, MPI_Comm, MPI_Status);
```
非阻塞：MPI_Isend MPI_Irecv
```cpp
int MPI_Isend(void *buffer, int count, MPI_Datatype, int dset, int tag, MPI_Comm, MPI_Request *);

int MPI_Irecv(void *buffer, int count, MPI_Datatype, int dset, int tag, MPI_Comm, MPI_Status, MPI_Request *);

```

## 聚合通信
一对多 MPI_Bcast
多对一 MPI_Gather
多对多 MPI_Alltoall

```cpp
int MPI_Bcast(void *buffer, int count, MPI_Datatype, int root, MPI_Comm);
```


# 2、对比Pthread、OpenMP和MPI三种并行编程语言。

# 3、在intel devCloud 平台上，参考视频学习并完成OpenCL完成矩阵乘法，并测试不同大小矩阵的加速比。