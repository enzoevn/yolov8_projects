# If not working, first do: sudo rm -rf /tmp/.docker.xauth
# It still not working, try running the script as root.
## Build the image first
### docker build -t r2_path_planning .
## then run this script

# Para dar permisos al fichero: "sudo chmod +x Nombre_archivo.bash"
# Para lanzarlo ./Nombre_archivo.bash

docker build -t yolov8_projects . 

docker run -it \
    --name yolov8_projects \
    --gpus all \
    --volume /mnt/docker/yolov8_projects:/home/enzo \
    --ipc=host \
    --user $(id -u):$(id -g) \
    yolov8_projects \
    bash

