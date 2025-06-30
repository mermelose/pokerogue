#include <mpi.h>
#include <iostream>
#include <random>
#include <chrono>

void round_robin(int rank, int procs)
{
  int rand_mine, rand_prev;
  int rank_next = (rank +1)%procs;
  int rank_prev = rank == 0 ? procs - 1 : rank - 1;
  MPI_Status status;

  srand(time(nullptr) + rank); 
  rand_mine = rand() % 100; 
  printf("%d: random is %d\n", rank, rand_mine);

  if (rank % 2 == 0) {
      // Even-ranked processes: send first, then receive
      std::cout << rank << ": sending " << rand_mine << " to " << rank_next << std::endl;
      MPI_Send(&rand_mine, 1, MPI_INT, rank_next, 1, MPI_COMM_WORLD);

      std::cout << rank << ": receiving from " << rank_prev << std::endl;
      MPI_Recv(&rand_prev, 1, MPI_INT, rank_prev, 1, MPI_COMM_WORLD, &status);
  } else {
      // Odd-ranked processes: receive first, then send
      std::cout << rank << ": receiving from " << rank_prev << std::endl;
      MPI_Recv(&rand_prev, 1, MPI_INT, rank_prev, 1, MPI_COMM_WORLD, &status);

      std::cout << rank << ": sending " << rand_mine << " to " << rank_next << std::endl;
      MPI_Send(&rand_mine, 1, MPI_INT, rank_next, 1, MPI_COMM_WORLD);
  }

  printf("%d: I had %d, %d had %d\n", rank, rand_mine, rank_prev, rand_prev);
}

int main(int argc, char** argv) {
    int rank, num_procs;
    
    MPI_Init(&argc, &argv);
    
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    printf("%d: Hello (p=%d)\n", rank, num_procs);
    round_robin(rank, num_procs);
    printf("%d: goodbye\n", rank);
    MPI_Finalize();
    
    return 0;
}