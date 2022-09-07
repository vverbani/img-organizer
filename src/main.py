# import libraries
import os
from PIL import Image
from PIL.ExifTags import TAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import datetime
from datetime import date
from datetime import datetime

# method to add images/videos without dates to the last month or current month
def get_date(OUTPUT_FOLDER_PATH):
    latest_date= ""

    dir_list= os.listdir(OUTPUT_FOLDER_PATH)

    # if a year exists, get month but if a year doesn't exist, get todays date
    if dir_list:

        # filter out folders that are year only, i.e don't look into 'other_items' folder
        year_only_filter=[]
        for year in dir_list:
            if year.isnumeric():
                year_only_filter.append(year)

        latest_year= max(year_only_filter)
        dir_month_list= os.listdir(OUTPUT_FOLDER_PATH + latest_year)
        month_list= []

        # August -> 8
        for month in dir_month_list:
            month_list.append(datetime.strptime(month, '%B').month)

        # 2022:8:01
        latest_date= str(latest_year) + ":" + str(max(month_list)) + ":01"
    else:
        latest_date= date.today().strftime("%Y:%m:%d")

    return latest_date

# read jpg/jpeg data
def read_jpg_image(INPUT_FOLDER_PATH):
    date= ''

    # read the image data using PIL
    image = Image.open(INPUT_FOLDER_PATH)

    # extract EXIF data
    exifdata = image.getexif()

    image.close()

    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)

        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()

        # we only care about the date
        if tag == 'DateTime':
            date= data

    return date

# read movie data
def read_metadata(INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH):
    date= ''

    parser = createParser(INPUT_FOLDER_PATH)

    if not parser:
        print("Unable to parse file")
        return date

    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            return get_date(OUTPUT_FOLDER_PATH)

    if not metadata:
        print("Unable to extract metadata")
        return date

    for line in metadata.exportPlaintext():
        if line.split(':')[0] == '- Creation date':
            date= line.split(':')[1].split()[0]
            date= date.replace("-", ":")

    return date

# create folder structure then moves item into the folder
def move_item(file, image_date, INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH):
    print(" --- Moving file to folder --- ")

    date = datetime.strptime(image_date[0:10], "%Y:%m:%d")

    # src/output-images/2022
    dir_in_year= OUTPUT_FOLDER_PATH + str(date.year) + "/"
    dir_in_month= dir_in_year + date.strftime("%B")

    # if neither the year or month exist as directories
    if not os.path.isdir(OUTPUT_FOLDER_PATH + str(date.year) + "/"):
        os.mkdir(dir_in_year)
        if not os.path.isdir(OUTPUT_FOLDER_PATH + str(date.year) + "/" + date.strftime("%B")):
            os.mkdir(dir_in_month)
            # move image into month directory
            os.rename(INPUT_FOLDER_PATH + file, OUTPUT_FOLDER_PATH + str(date.year) + "/" + date.strftime("%B") + "/" + file)
    # if year exist as a directory but the month doesn't
    else:
        if not os.path.isdir(OUTPUT_FOLDER_PATH + str(date.year) + "/" + date.strftime("%B") + "/"):
            os.makedirs(dir_in_month, exist_ok=True)
            # move image into month directory
            os.rename(INPUT_FOLDER_PATH + file, OUTPUT_FOLDER_PATH + str(date.year) + "/" + date.strftime("%B") + "/" + file)

# delete .DS_store as it blocks the program looking for files/folders properly
def del_hidden_file(INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH):
    if os.path.exists(OUTPUT_FOLDER_PATH + '.DS_Store'):
        os.remove(OUTPUT_FOLDER_PATH + '.DS_Store')

    if os.path.exists(INPUT_FOLDER_PATH + '.DS_Store'):
        os.remove(INPUT_FOLDER_PATH + '.DS_Store')
    return

def main():

    # ADD THE INPUT AND OUPUT FOLDER PATHS FOR YOUR IMAGES
    INPUT_FOLDER_PATH= "src/images/"
    OUTPUT_FOLDER_PATH= "src/output-images/"
    OTHER_FOLDER_NAME= "src/output-images/other_items/"

    # date per image
    image_date= ""

    del_hidden_file(INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH)

    dir_list= os.listdir(INPUT_FOLDER_PATH)

    # exit out if there are no files to move
    if len(dir_list) == 0:
        print("No files to move, sorry but you'll have to try again when there's files.")
        return

    # create output folder
    os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

    print("Moving all files from '", INPUT_FOLDER_PATH, "' :")

    for file in dir_list:
        print(file)
        image_date= ''

        # ignore hidden files
        if file.lower().startswith(('.')):
            continue

        # file is either an image or a video
        if file.lower().endswith(('png','.jpg','.jpeg','m4v','mov','mp4')):
            if file.lower().endswith(('.jpg', '.jpeg')):
                image_date= read_jpg_image(INPUT_FOLDER_PATH + file)
                # Assuming jpeg image has no exifdata, check to see if date is stored in metadata
                if image_date == "":
                    image_date= read_metadata(INPUT_FOLDER_PATH + file, OUTPUT_FOLDER_PATH)
            else:
                image_date= read_metadata(INPUT_FOLDER_PATH + file, OUTPUT_FOLDER_PATH)

            # image or movie has no date, get latest dat
            if image_date == "":
                image_date= get_date(OUTPUT_FOLDER_PATH)

            move_item(file, image_date, INPUT_FOLDER_PATH, OUTPUT_FOLDER_PATH)
        # file is neither image nor video
        else:
            # move to /other_items folder
            os.makedirs(OTHER_FOLDER_NAME, exist_ok=True)
            os.rename(INPUT_FOLDER_PATH + file, OTHER_FOLDER_NAME + file)

if __name__ == "__main__":
    main()