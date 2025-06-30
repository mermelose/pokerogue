#include <iostream>
#include <omp.h>
//#define NUM_THREADS 2
//
//int main() {
//    int temperatura[] = { 20, 21, 19, 23, 22 };
//    int humedad[] = { 55, 60, 58, 57, 56 };
//    int presion[] = { 1012, 1013, 1011, 1014, 1012 };
//    const int n = 5;
//
//    // Variables para almacenar resultados
//    double promedio_temperatura = 0.0;
//    double promedio_humedad = 0.0;
//    int min_presion = presion[0];
//    int max_presion = presion[0];
//
//#pragma omp parallel sections num_threads(NUM_THREADS)
//    {
//        // Sección para temperatura
//#pragma omp section
//        {
//            int thread_id = omp_get_thread_num();
//            printf("Sección de temperatura ejecutándose en thread %d\n", thread_id);
//
//            double suma = 0;
//            for (int i = 0; i < n; ++i) suma += temperatura[i];
//            promedio_temperatura = suma / n;
//        }
//
//        // Sección para humedad
//#pragma omp section
//        {
//            int thread_id = omp_get_thread_num();
//            printf("Sección de humedad ejecutándose en thread %d\n", thread_id);
//
//            double suma = 0;
//            for (int i = 0; i < n; ++i) suma += humedad[i];
//            promedio_humedad = suma / n;
//        }
//
//        // Sección para presión
//#pragma omp section
//        {
//            int thread_id = omp_get_thread_num();
//            printf("Sección de presión ejecutándose en thread %d\n", thread_id);
//
//            for (int i = 1; i < n; ++i) {
//                if (presion[i] < min_presion) min_presion = presion[i];
//                if (presion[i] > max_presion) max_presion = presion[i];
//            }
//        }
//    }
//    // Imprimir resultados
//    std::cout << "\nResultados del procesamiento de sensores:\n";
//    std::cout << "Temperatura: Promedio = " << promedio_temperatura << " °C\n";
//    std::cout << "Humedad: Promedio = " << promedio_humedad << " %\n";
//    std::cout << "Presión: Rango = [" << min_presion << " - " << max_presion << "] hPa\n";
//
//    return 0;
//}