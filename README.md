# Cinnamon Dynamic Wallpaper
<img src="cinnamon-dynamic-wallpaper@TobiZog/5.4/icons/icon.svg" alt="drawing" width="200" style="margin-left:auto; margin-right:auto; width:50%; display:block"/>

![](res/wallpaper_merged.jpg)

## About the project
This extension switches the background image of your Cinnamon desktop multiple times in a day, based on a location or custom time periods. You can choose between included image-sets, your own HEIC-file or a source folder with single images. Configuration through a user-friendly configuration window.

### Features
- 8 included image sets
- 10 day periods
- HEIF converter
- Image configuration assistent with simple one-click setup for image choices
- Online location estimation or offline with manual latitude and longitude input
- Time periods individual configured by user
- Offline sun angles estimation
- Image stretching over multiple displays or repeat image for every display
- Show image on lock screen

### Tested Cinnamon versions
- 5.4 (Mint 21)
- 5.6 (Mint 21.1)
- 5.8 (Mint 21.2)
- 6.0 (Mint 21.3)

#### Only supported with version 1.x
- 4.8 (Mint 20.1)
- 5.0 (Mint 20.2)
- 5.2 (Mint 20.3)

### Technology
- Using `JavaScript` for
	- Location estimation
	- Change of the desktop wallpapers
- `Python` displays the preference window
- Image Configurator UI was written with `Glade`

## Installation
### From Built-in Extension Manager
![](res/download-manager.png)

1. Open "Extensions" in Linux Mint or any other distribution with Cinnamon as Desktop Environment
2. Click on "Download"
3. Search and download it

### From the repo
1. Download the Repository
2. Extract the files
3. Copy the folder `cinnamon-dynamic-wallpaper@TobiZog` to `~/.local/share/cinnamon/extensions/`

## How to use it
1. Active the Extension via Cinnamon Extension Manager
2. Open the settings
3. Keep `Estimate coordinates via network` active or disable it and insert latitude and longitude in the fields
4. Choose a set of images or disable it and select for every daytime an image manually

## Image Configurator
The Cinnamon Dynamic Wallpaper extension offers an integrated image configuration assistant. Here, you can choose an included image set or import a HEIC-file from your system. You have to choose the images for the time periods after the import.

![](res/image_configurator.png)


## Included image sets
The image sets are from https://github.com/adi1090x/dynamic-wallpaper

| Aurora | Beach | Bitday |
| ------ | ----- | ------ |
| ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/aurora/5.jpg) | ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/beach/4.jpg) | ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/bitday/4.jpg) |

| Cliffs | Gradient | Lakeside | 
| -------- | --------- | ------ |
| ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/cliffs/4.jpg) | ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/gradient/4.jpg) | ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/lakeside/4.jpg) |

| Mountains | Sahara |
| --------- | ------ |
| ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/mountains/4.jpg) | ![](cinnamon-dynamic-wallpaper@TobiZog/5.4/images/included_image_sets/sahara/4.jpg) |