#!/bin/bash

echo "=== EJEMPLOS DE OVERSUBSCRIBE ==="
echo ""

# 1. Verificar recursos del sistema
echo "🔍 INFORMACIÓN DEL SISTEMA:"
echo "Núcleos de CPU disponibles: $(nproc)"
echo "Threads de hardware: $(nproc --all)"
echo "Memoria total: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo ""

# 2. Pruebas sin oversubscribe
echo "🚫 PRUEBAS SIN OVERSUBSCRIBE (comportamiento normal):"
echo ""

echo "✅ Ejecutando con 1 proceso (debería funcionar):"
time mpirun -np 1 ./hello_mpi
echo ""

echo "✅ Ejecutando con $(nproc) procesos (máximo normal):"
time mpirun -np $(nproc) ./hello_mpi
echo ""

echo "❌ Intentando con más procesos que núcleos (debería fallar):"
echo "Comando: mpirun -np $(($(nproc) + 1)) ./hello_mpi"
mpirun -np $(($(nproc) + 1)) ./hello_mpi 2>&1 | head -5
echo "... (error truncado)"
echo ""

# 3. Pruebas con oversubscribe
echo "✅ PRUEBAS CON OVERSUBSCRIBE:"
echo ""

echo "Ejecutando con 4 procesos (oversubscribe):"
time mpirun --oversubscribe -np 4 ./hello_mpi
echo ""

echo "Ejecutando con 8 procesos (oversubscribe):"
time mpirun --oversubscribe -np 8 ./hello_mpi
echo ""

echo "Ejecutando con 16 procesos (oversubscribe):"
time mpirun --oversubscribe -np 16 ./hello_mpi
echo ""

# 4. Comparación de rendimiento
echo "⏱️  COMPARACIÓN DE RENDIMIENTO:"
echo ""

echo "Midiendo tiempo con diferentes números de procesos..."
echo ""

echo "Con 1 proceso:"
time (mpirun -np 1 ./hello_mpi > /dev/null)
echo ""

echo "Con $(nproc) procesos (óptimo):"
time (mpirun -np $(nproc) ./hello_mpi > /dev/null)
echo ""

echo "Con 8 procesos (oversubscribe):"
time (mpirun --oversubscribe -np 8 ./hello_mpi > /dev/null)
echo ""

echo "Con 16 procesos (mucho oversubscribe):"
time (mpirun --oversubscribe -np 16 ./hello_mpi > /dev/null)
echo ""

# 5. Ejemplo visual del comportamiento
echo "📊 VISUALIZACIÓN DEL COMPORTAMIENTO:"
echo ""

echo "Normal (sin oversubscribe):"
echo "Núcleo 1: [Proceso 0]"
if [ $(nproc) -gt 1 ]; then
    echo "Núcleo 2: [Proceso 1]"
fi
echo ""

echo "Con oversubscribe (4 procesos en $(nproc) núcleo(s)):"
if [ $(nproc) -eq 1 ]; then
    echo "Núcleo 1: [P0] ↔ [P1] ↔ [P2] ↔ [P3] (se alternan)"
else
    echo "Núcleo 1: [P0] ↔ [P2] (se alternan)"
    echo "Núcleo 2: [P1] ↔ [P3] (se alternan)"
fi
echo ""

echo "=== CONCLUSIONES ==="
echo "- Sin oversubscribe: Mejor rendimiento, limitado por núcleos"
echo "- Con oversubscribe: Más flexibilidad, menor rendimiento por proceso"
echo "- Ideal para aprendizaje: --oversubscribe"
echo "- Ideal para producción: sin --oversubscribe"