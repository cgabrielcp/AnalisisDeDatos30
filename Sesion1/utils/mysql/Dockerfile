# Utiliza la última imagen oficial de MySQL como base
FROM mysql:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /mysql/data

# Define la contraseña del usuario root de MySQL (no recomendable para producción)
ENV MYSQL_ROOT_PASSWORD=root

# Copia los archivos SQL al directorio especial de inicialización de MySQL.
# Cualquier archivo `.sql` en /docker-entrypoint-initdb.d/ será ejecutado automáticamente
# al iniciar el contenedor por primera vez si no hay una base de datos previa.
COPY data_warehouse_netflix.sql /docker-entrypoint-initdb.d/
COPY db_movies_neflix_transact.sql /docker-entrypoint-initdb.d/
COPY retail_db.sql /docker-entrypoint-initdb.d/
