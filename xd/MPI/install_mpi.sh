#!/bin/bash

echo "=== Iniciando instalación de OpenMPI ==="

# 0. Instalar herramientas de desarrollo necesarias
echo "Instalando herramientas de desarrollo..."
sudo apt update
sudo apt install -y build-essential gcc g++ gfortran make wget curl

# Verificar que gcc está instalado
if ! command -v gcc &> /dev/null; then
    echo "Error: gcc no se instaló correctamente"
    exit 1
fi

echo "Compilador gcc instalado correctamente: $(gcc --version | head -n1)"

# 1. Crear directorio para instalar OpenMPI
echo "Creando directorio de instalación..."
mkdir -p $HOME/openmpi
cd $HOME/openmpi

# 2. Descargar OpenMPI
echo "Descargando OpenMPI 5.0.7..."
wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.7.tar.gz

# Verificar que la descarga fue exitosa
if [ ! -f "openmpi-5.0.7.tar.gz" ]; then
    echo "Error: No se pudo descargar el archivo"
    exit 1
fi

# 3. Extraer el paquete
echo "Extrayendo el paquete..."
tar -xzvf openmpi-5.0.7.tar.gz
cd openmpi-5.0.7/

# 4. Configurar y compilar
echo "Configurando OpenMPI (esto puede tomar 5-10 minutos)..."
./configure --prefix=$HOME/openmpi

echo "Compilando OpenMPI..."
make all

# 5. Instalar
echo "Instalando OpenMPI..."
make install

# 6. Agregar OpenMPI al PATH y LD_LIBRARY_PATH
echo "Configurando variables de entorno..."
echo 'export PATH=$HOME/openmpi/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$HOME/openmpi/lib:$LD_LIBRARY_PATH' >> ~/.bashrc

# Cargar las nuevas variables de entorno
source ~/.bashrc

echo "=== Instalación completada ==="
echo "OpenMPI ha sido instalado en $HOME/openmpi"
echo "Las variables de entorno han sido configuradas en ~/.bashrc"
#echo "Ejecuta 'source ~/.bashrc' o reinicia la terminal para usar OpenMPI"