# Referenciar una imagen (Python)
FROM ubuntu:20.04

#Evitar que el SO evite instalaciones manualas
ENV DEBIAN_FRONTEND=noninteractive

# Ejecutar algunas actualizaciones de sistemas y paquetes
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    wget && \
    apt-get clean

# Actualizar pip e instalar el JNotebook
RUN pip3 install --upgrade pip && \
    pip3 install notebook==6.5.6

# definir el directorio del trabajo
WORKDIR /workspace


# Donde se guardara las configuraciones de Jupyter
RUN mkdir -p /root/.jupyter

# Asignacion de variables de configuracion
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py

# Exponer el puerto de la imagen
EXPOSE 8888

# Comando por defente para inciar el contenedor
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]