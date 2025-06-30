#include <mpi.h>
#include <iostream>

int main(int argc, char** argv) {
    int rank, num_procs;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    double mi_valor = rank * 3.14;  // 0.0, 3.14, 6.28, 9.42...
    double maximo = 0.0;

    MPI_Reduce(&mi_valor,      // mi valor
           &maximo,        // máximo resultado
           1,              // 1 elemento
           MPI_DOUBLE,     // tipo double
           MPI_MAX,        // encontrar máximo
           0,              // proceso 0 recibe
           MPI_COMM_WORLD);

    if (rank == 0) {
        std::cout << "Máximo: " << maximo << std::endl;
    }   

    MPI_Finalize();
    return 0;
}

/*
MPI_Reduce - Sintaxis completa:

int MPI_Reduce(
    const void* sendbuf,     // Dato a enviar (de cada proceso)
    void* recvbuf,           // Donde guardar resultado
    int count,               // Número de elementos
    MPI_Datatype datatype,   // Tipo de dato
    MPI_Op op,               // Operación a realizar
    int root,                // Proceso que recibe resultado
    MPI_Comm comm            // Comunicador (normalmente MPI_COMM_WORLD)
);

¿Qué hace MPI_Reduce?

Recolecta las sumas parciales de todos los procesos
Las suma (MPI_SUM)
Envía el resultado al proceso 0

¿Qué hace MPI_Finalize?
Es la función que cierra y limpia el entorno MPI.

¿Qué hace exactamente?
1. Limpieza de recursos:

Libera memoria usada por MPI.
Cierra conexiones de red entre procesos.
Libera buffers de comunicación.
Desactiva el sistema de mensajería.

2. Sincronización final:

Espera a que todos los procesos terminen sus operaciones MPI.
Asegura que no hay comunicaciones pendientes.
*/