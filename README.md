# FreePik photo archiver on yandex disk

### project for backing up photo from FreePik to Yandex Disk

## Installation

```
git clone https://github.com/sardor86/yandex_disk.git
pip install -r requirements.txt
```

## Compilation for windows
```
cd yandex_disk_archiver
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```
#### the executable is located in the dist folder

## Running a project on linux
```
cd yandex_disk_archiver
python main.py
```
