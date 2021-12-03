# LoLVODWatcher

Used for watching League of Legends VODs to complete missions. The script can watch multiple videos simulatenously via multiple tabs. The script can also do the following:
* Mute the sound
* Lower video quality to save bandwidth
* Allows user to input desired VOD URL.

## Getting Started
These instructions will help you get started with using the application.

### Prerequisites
The following must be installed:
* Google Chrome

### Usage
1. Launch the application using LoLVODWatcher.exe
2. Enter the number of minutes to watch each video.
3. Enter the number of videos/tabs to watch simulatenously.
4. Log in with User and Password.
5. Leave the application and browser to run in background.

Note: Releases are packaged using Pyinstaller. The executable will only work on Microsoft Windows platform.

## Development
These instructions will get you a copy of the project up and running on your local machine for development.

### Built With
* [Python 3.6](https://docs.python.org/3/) - The scripting language used.
* [Selenium](https://selenium-python.readthedocs.io/) - Web crawling automation framework.
* [Webdriver-Manager](https://github.com/SergeyPirogov/webdriver_manager) - Manager for webdriver version.
* [Chrome Webdriver](http://chromedriver.chromium.org/downloads) - Webdriver for Chrome browser. Use to control automation with Selenium.
* [PyInstaller](https://www.pyinstaller.org/) - Used to create executable for release.

### Running the Script
Run the following command to installer all the required Python modules:
```
pip install -r requirements.txt
```
To run the application:
```
python .\LoLVODWatcher.py
```

### Compiling using PyInstaller

The project files includes a batch file (Windows platform only) with commands to run to compile into an executable. 

Other development platforms can run the following command in Terminal:

```
pyinstaller -F --onefile .\LoLVODWatcher.py
```
You may need to modify the file paths if not in same current working directory.

## Screenshot
![lolvodwatcher](https://user-images.githubusercontent.com/41496510/50428181-ed758100-0869-11e9-95f2-d65ed64fedd5.png)

## Authors
* **Patrick Yu** - *Initial work* - [patrickgod1](https://github.com/patrickgod1)
