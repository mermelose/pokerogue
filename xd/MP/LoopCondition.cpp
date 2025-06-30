/**
 * Programa que compara el rendimiento de dos implementaciones diferentes
 * para procesar una matriz unidimensional con operaciones condicionales.
 */
#include <stdio.h>  // Librer�a para operaciones de entrada/salida
#include <stdlib.h> // Librer�a est�ndar para funciones como malloc, free, etc.
#include <ctime>    // Librer�a para medir tiempo con clock()
#include <omp.h>    // Librer�a OpenMP para medici�n de tiempo de alta precisi�n

int main(void) {
    // Declaraci�n e inicializaci�n de variables
    int N = 5;             // Tama�o de la matriz N�N
    int idx = 0;           // �ndice para acceder a elementos de la matriz unidimensional
    int x[5 * 5];          // Arreglo unidimensional que representa una matriz de 5�5
    double t0, t1;         // Variables para almacenar tiempos de inicio y fin
    double time, time_s;   // Variables para almacenar la duraci�n de ejecuci�n

    // Inicializaci�n del arreglo y mostrar valores iniciales
    for (int i = 0; i < N * N; i++) {
        x[i] = i;
        printf("x[%d] = %d\n", i, x[i]);
    }

    // PRIMERA IMPLEMENTACI�N: Bucle con condicional dentro del bucle anidado
    printf("Bucle con condicional\n");
    t0 = clock();  // Marca de tiempo inicial usando clock()

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            idx = i * N + j;  // Calcular �ndice en arreglo unidimensional para simular matriz 2D

            // Operaci�n condicional: multiplica por 2 si j < i, sino asigna 0
            if (j < i) {
                x[idx] = x[idx] * 2;
            }
            else {
                x[idx] = 0;
            }

            // Mostrar estado despu�s de la operaci�n
            printf("i:%d - j:%d - idx:%d - x[%d] = %d\n", i, j, idx, idx, x[idx]);
        }
    }

    t1 = clock();  // Marca de tiempo final
    time = (t1 - t0) / CLOCKS_PER_SEC;  // C�lculo del tiempo transcurrido en segundos
    printf("Tiempo de ejecuci�n (ctime): %f\n", time);

    // SEGUNDA IMPLEMENTACI�N: Separaci�n del bucle para evitar condicionales
    printf("Bucle sin condicional\n");

    // Reiniciar el arreglo a sus valores originales
    for (int i = 0; i < N * N; i++)
        x[i] = i;

    t0 = omp_get_wtime();  // Marca de tiempo inicial usando OpenMP para mayor precisi�n

    for (int i = 0; i < N; i++) {
        printf("***********************\n");

        // Primer bucle: procesa elementos donde j < i (multiplicaci�n por 2)
        int j = 0;
        for (; j < i; j++) {
            idx = i * N + j;
            x[idx] = x[idx] * 2;
            printf("i:%d - j:%d - idx:%d - X[%d] = %d\n", i, j, idx, idx, x[idx]);
        }

        printf("--------------------\n");

        // Segundo bucle: procesa elementos donde j >= i (asignaci�n de 0)
        // Reutiliza la variable j del bucle anterior
        for (; j < N; j++) {
            printf("Valor de j: %d\n", j);
            idx = i * N + j;
            x[idx] = 0;
            printf("i:%d - j:%d - idx:%d - X[%d] = %d\n", i, j, idx, idx, x[idx]);
        }
    }

    t1 = omp_get_wtime();  // Marca de tiempo final
    time_s = t1 - t0;      // C�lculo del tiempo transcurrido
    printf("Tiempo de ejecuci�n (omp): %f\n", time_s);

    return 0;  // Terminar programa con �xito
}

//N = 500
//Bucle con condicional
//Tiempo de ejecuci�n(ctime) : 0.001000
//Bucle sin condicional
//Tiempo de ejecuci�n(omp) : 0.000562