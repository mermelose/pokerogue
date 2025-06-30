
#include <iostream>
#include <omp.h>
#include <limits.h>  // Para el valor máximo y mínimo de int

using namespace std;

int main() {
    const int N = 100;  // Tamaño de la matriz 100x100
    int matriz[N][N];   // Declaración de la matriz
    int suma_diagonal_principal = 0;
    int suma_diagonal_secundaria = 0;
    int suma_total = 0;
    int max_val = INT_MIN;  // Iniciar con el valor mínimo posible
    int min_val = INT_MAX;  // Iniciar con el valor máximo posible

    // Inicialización de la matriz
    #pragma omp parallel for collapse(2) num_threads(6)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            matriz[i][j] = (i + j) * 3;  // Asignar valor a cada elemento
        }
    }

    // Procesamiento de la matriz en paralelo
    #pragma omp parallel for reduction(+:suma_diagonal_principal, suma_diagonal_secundaria, suma_total) reduction(min:min_val) reduction(max:max_val) num_threads(6)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            // Sumar los elementos de la diagonal principal
            if (i == j) {
                suma_diagonal_principal += matriz[i][j];
            }
            // Sumar los elementos de la diagonal secundaria
            if (i + j == N - 1) {
                suma_diagonal_secundaria += matriz[i][j];
            }
            // Sumar el total de todos los elementos de la matriz
            suma_total += matriz[i][j];

            // Encontrar el valor máximo en la matriz
            if (matriz[i][j] > max_val) {
                max_val = matriz[i][j];
            }
            // Encontrar el valor mínimo en la matriz
            if (matriz[i][j] < min_val) {
                min_val = matriz[i][j];
            }
        }
    }

    // Mostrar los resultados
    cout << "Suma de la diagonal principal: " << suma_diagonal_principal << endl;
    cout << "Suma de la diagonal secundaria: " << suma_diagonal_secundaria << endl;
    cout << "Valor máximo en la matriz: " << max_val << endl;
    cout << "Valor mínimo en la matriz: " << min_val << endl;
    cout << "Suma total de todos los elementos de la matriz: " << suma_total << endl;

    return 0;
}
