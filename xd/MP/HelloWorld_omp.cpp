// Inclusi�n de la biblioteca est�ndar de entrada/salida
#include <stdio.h>

// Inclusi�n de la biblioteca OpenMP para programaci�n paralela
#include <omp.h>

//void main(void)
//{
//	// Establece el n�mero de hilos a utilizar (4 en este caso)
//	//omp_set_num_threads(4);
//
//	// Directiva para crear una regi�n paralela 
//	#pragma omp parallel
//	{
//		int th_id = omp_get_thread_num();
//		printf("Hello world - Thread #: (%d) \n", th_id);
//	}
//
//}