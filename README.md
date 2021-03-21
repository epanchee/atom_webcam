### Установка

`./install.sh [user] [interval] [--debug|''] [workdir] [save_path]`

###Пример установки:

./install.sh dietpi 300 --debug

--debug пишем, если нужно логирование

###Полезное

Забиндить папку с фотками на другой диск (пример)  
`mount --bind /mnt/toshiba/Media/atom /opt/atom_webcam/data/`

/mnt/toshiba/Media/atom - точка монтирования
/opt/atom_webcam/data/ - папка, куда сохраняются картинки
