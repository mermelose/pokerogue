#include <stdio.h>   // Biblioteca est�ndar para operaciones de entrada/salida
#include <omp.h>     // Biblioteca de OpenMP para programaci�n paralela
//#define NUM_THREADS 4

// Version 0
//int main(void) {
//    int i = 0;
//    int n = 2;
//#pragma omp parallel
//    {
//        for (i = 0; i < n; i++)
//            printf("Thread %d executes loop iteration % d\n", omp_get_thread_num(), i);
//    }
//    /*-- End of parallel region --*/
//}

// Version 1
//int main(void) {
//    int i = 0;       // variable de control para el bucle
//    int n = 13;      // n�mero de iteraciones del bucle
//
//    // directiva que crea una regi�n paralela donde m�ltiples hilos ejecutar�n el c�digo
//    // shared(n): la variable n es compartida entre todos los hilos (todos ven el mismo valor)
//#pragma omp parallel num_threads(NUM_THREADS) shared(n)
//    {
//        // directiva que distribuye las iteraciones del bucle entre los hilos disponibles
//        // cada hilo ejecutar� un subconjunto de las iteraciones de forma independiente
//        // por defecto, el trabajo se distribuye de manera equilibrada (schedule(static))
//#pragma omp for
//        for (i = 0; i < n; i++)
//            printf("thread %d executes loop iteration %d\n", omp_get_thread_num(), i);
//        // omp_get_thread_num() devuelve el id del hilo que est� ejecutando ese c�digo
//    }
//    /*-- end of parallel region --*/
//    // al salir de la regi�n paralela, solo contin�a el hilo maestro (thread 0)
//
//}
