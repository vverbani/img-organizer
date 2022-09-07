# AUTOMATED IMAGE ORGANIZER

Tired of trying to organize a thousand pictures that are crammed into one singular folder? Yeah, me too.

This idea came from having a couple of external hard drives that had a large number of images in single folders. It was annoying to not know when the image was taken, and got boring after skimming through a 100 of them.

I wanted a way to organize these images, location and/or time. Since most images nowadays might not have their location the next best choice was by time. This script combs through a folder full of images and organizes them by their respective Year and date.

Any non image gets moved to the `/other-items` folder.


## Prerequisites

1. [Docker](https://www.docker.com/)
2. Make sure to add the folder path where your images exist in the following variable: `INPUT_FOLDER_PATH`
3. Make sure to add the folder path to where you want your automated images to end up in with the following variable: `OUTPUT_FOLDER_PATH`

## Usage

```bash
    docker-compose up
```

**** PLEASE USE THIS AT YOUR OWN RISK ****
