#include <mpi.h>
#include <iostream>

int main(int argc, char** argv) {
    int rank, num_procs;
    
    MPI_Init(&argc, &argv);
    
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    std::cout << "Hello from process " << rank 
              << " of " << num_procs << std::endl;

    MPI_Finalize();
    
    return 0;
}