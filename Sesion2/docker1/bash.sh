# Crear imagen docker
docker build -t image-test .

# listar imagenes
docker images

# ejecutar un contenedor
docker run -d -p 8080:8888 --name jupyter image-test

#log de ejecucion del contenedor
docker logs -f jupyter

# Eliminar una imagen
docker rmi -f a58859673f21

# Eliminar un contenedor
docker rm -f 3e47d957070b