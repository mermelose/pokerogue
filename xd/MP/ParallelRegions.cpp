#include <stdio.h>
#include <omp.h>
//# define N 10
//# define NUM_THREADS 3

//void Square(int id, double a[]) {
//	int i;
//	printf("thread id: %d\n", id);
//	for (i = id; i < N; i += NUM_THREADS)
//	{
//		a[i] *= a[i];
//		printf("thread id: %d - a[%d] = %f\n", id, i, a[i]);
//	}
//}
//
//void main(void) {
//	double a[N], t0, t1, time;
//	for (int i = 0; i < N; i++)
//		a[i] = i;
//	
//	t0 = omp_get_wtime();
//#pragma omp parallel num_threads(NUM_THREADS)
//	{
//		int id = omp_get_thread_num();
//		Square(id, a);
//	}
//	t1 = omp_get_wtime();
//	time = t1 - t0;
//	printf("Tiempo de ejecución: %f\n", time);
//
//	for (int i = 0; i < 10; i++)
//	{
//		printf("a[%d] = %f\n", i, a[i]);
//	}
//
//	printf("all done\n");
//}
