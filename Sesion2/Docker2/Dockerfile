# Imagen Base de python
FROM python:3.8-slim

# Establecer nuestro espacio de trabajo
WORKDIR /app

# Moiver mis archivos a el espacio de trabajo
COPY requeriments.txt ./

# instalar los paquetes
RUN pip install --no-cache-dir -r requeriments.txt

# Copian todos los archivos del local al espacio de trabajo
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
