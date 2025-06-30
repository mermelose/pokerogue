#include <stdio.h>
#include <stdlib.h>
#include <ctime> 
#include <omp.h>
#include <iostream>
using namespace std;

//int cuadrado(int n) {
//	return n * n;
//}
//
//int main(void) {
//	double t0, t1, time_i, time_o;
//	int n = 10000, sum = 0, i = 0;
//	printf("Llamada a la función dentro del for\n");
//	t0 = omp_get_wtime();
//	for (i = 0; i < cuadrado(n); i++) {
//		sum += i;
//		//cout << sum << endl;
//	}
//	t1 = omp_get_wtime();
//	time_i = t1 - t0;
//	cout << "Execution Time: " << time_i << endl;
//
//	printf("Llamada a la función fuera del for\n");
//	t0 = omp_get_wtime();
//	int z = cuadrado(n);
//	sum = 0;
//	for (i = 0; i < z; i++) {
//		sum += i;
//		//cout << sum << endl;
//	}
//	t1 = omp_get_wtime();
//	time_o = t1 - t0;
//	cout << "Execution Time: " << time_o << endl;
//	cout << "Speed: " << time_i/time_o << endl;
//
//}
