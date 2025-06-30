#include <iostream>
#include <cmath>
#include <chrono>
#include <mpi.h>

using namespace std;

// Función matemática que vamos a sumar (ejemplo: 1/sqrt(i+1))
double funcion(int i) {
    return 1.0 / sqrt(i + 1);
}

int main(int argc, char** argv) {
    // Inicializar MPI
    MPI_Init(&argc, &argv);

    // Obtener el rango del proceso y el tamaño total de los procesos
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Tamaño total de la serie
    const int N = 100000;  // Número de términos en la serie
    const int work_per_process = N / size;  // Trabajo por proceso

    // Dividir el trabajo entre los procesos
    int start = rank * work_per_process;
    int end = (rank + 1) * work_per_process - 1;

    // Ajustar el último proceso en caso de que no se divida perfectamente
    if (rank == size - 1) {
        end = N - 1;
    }

    // Medir el tiempo de ejecución
    auto start_time = chrono::high_resolution_clock::now();

    // Calcular la suma parcial para el rango de este proceso
    double local_sum = 0.0;
    for (int i = start; i <= end; ++i) {
        local_sum += funcion(i);
    }

    // Medir el tiempo de ejecución del proceso
    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end_time - start_time;

    // Imprimir el tiempo de ejecución y el rango de cálculo para cada proceso
    cout << "Proceso " << rank << " calculó desde el índice " << start << " hasta " << end
         << " en " << duration.count() << " segundos." << endl;

    // Reducir la suma local a la suma global usando MPI_Reduce
    double global_sum = 0.0;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    // El proceso 0 imprime el resultado final
    if (rank == 0) {
        cout << "La suma total es: " << global_sum << endl;
    }

    // Finalizar MPI
    MPI_Finalize();
    return 0;
}
