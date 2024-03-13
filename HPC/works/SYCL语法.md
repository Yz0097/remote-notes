### buffer与host内存中开辟的空间绑定 
这样做可以便于输入输出
```cpp
float(*A) = new float[mA * nA];
float(*B)[mB * nB] = new float[round_size][mB * nB];

buffer a_buffer(reinterpret_cast<float *>(A), range(mA, nA));
buffer b_buffer(reinterpret_cast<float *>(B[round]), range(mB,nB));

// A[i][j] = A[j + nA * i]
// matrix row and col, store by row
```

### 创建accessor来访问buffer
```cpp
host_accessor b2(b_buffer, read_only);

for (int k = 0; k < 10; k++){
	cout<<"---------------number:"<<k+1<<"-----------------\n";
	for(int i = 0 ; i<mB;i++){
		for(int j =0;j<nB;j++){
			cout<<B[k][i*nB+j]<<'\n';
			cout<<b2[k][i][j]<<'\n';
		}
	}
}
```


### 创建队列
```cpp
queue q(default_selector_v);

cout << "Device: " << q.get_device().get_info<info::device::name>() << "\n";
```


### 通过队列提交任务 并行核函数
这是一个矩阵乘法的例子
```cpp
q.submit([&](auto &h)

{
	// Read from a and b, write to c
	accessor a(a_buffer, h, read_only);
	accessor b(b_buffer, h, read_only);
	accessor c(c_buffer, h, write_only);
	
	// Execute kernel.
	h.parallel_for(range(mC, nC), [=](auto index)
	{
		// Get global position in Y direction.
		int row = index[0];
		// Get global position in X direction.
		int col = index[1];
		float sum = 0.0f;
		
		// Compute the result of one element of c
		for (int i = 0; i < nA; i++) {
		sum += a[row][i] * b[i][col];
		}
		c[index] = sum;
	});
});
q.wait();
```