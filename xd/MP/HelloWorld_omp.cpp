// Inclusión de la biblioteca estándar de entrada/salida
#include <stdio.h>

// Inclusión de la biblioteca OpenMP para programación paralela
#include <omp.h>

//void main(void)
//{
//	// Establece el número de hilos a utilizar (4 en este caso)
//	//omp_set_num_threads(4);
//
//	// Directiva para crear una región paralela 
//	#pragma omp parallel
//	{
//		int th_id = omp_get_thread_num();
//		printf("Hello world - Thread #: (%d) \n", th_id);
//	}
//
//}