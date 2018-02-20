import os
import subprocess
import re
import logging


def getMetaData(filename):
    try:
        logger.debug('Fetching metadata for file {0}'.format(filename))
        result = subprocess.check_output([LIB_CMD, filename])
        return result
    except Exception as e:
        logger.error('Error fetching metadata for file {0} '.format(filename) + str(e))


def validFileName(name):
    # file does not have a date then skip
    if re.match(r'\d{4}', name):
        logger.debug('{0} is a valid filename. Date is present'.format(name))
        return True
    logger.debug('{0} is not a valid filename. Date is absent'.format(name))
    # filenames not adhering to format
    return True


def parseFileNameForDate(name):
    # extract date based on filename format
    m = re.match(r'(\d{4}[\d\-]*)-', name)
    # case where there is some year in filename
    n = re.search(r'((1|2)\d{3})', name)
    if m:
        val = m.group(1)
        logger.info('Date >>>{a}<<< is parsed from filename {b}'.format(a=val, b=name))
        return m.group(1)    
    elif n and 'IMG_' not in name:
        val = n.group(1)
        logger.info('Date >>>{a}<<< is parsed from filename {b}'.format(a=val, b=name))
    else:
        logger.error('Unable to parse date from filename {0}'.format(name))
        date_skipped_files.append(os.path.join(absolute_filename))


def normalizeDate(date):
    # return 2015:10:24 20:00:00 format
    m1 = re.match(r'(\d{4})\-(\d{1,2})\-(\d{1,2})', date)
    if m1:
        val = m1.group(1) + ':' + m1.group(2).zfill(2) + ':' + m1.group(3).zfill(2) + '09:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val
    m2 = re.match(r'(\d{4})\-(\d{1,2})', date)
    if m2:
        val = m2.group(1) + ':' + m2.group(2).zfill(2) + ':01 09:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val
    m3 = re.match(r'(\d{4})\-', date)
    if m3:
        val = m3.group(1) + ':01:01 09:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val


def setDateMetaData(filename, date):
    if filename is None or date is None:
        logger.error('Filename {a} or Date {b} is empty'.format(a=filename, b=date))
        return False
    cmd = '-alldates=' + str(normalizeDate(date))
    cmd_list = [LIB_CMD, cmd, filename]
    if not demo_mode:
        logger.debug('Command : {0}'.format(str(cmd_list)))
    try:
        if not demo_mode:
            result = subprocess.check_output(cmd_list)
        return True
    except Exception as w:
        date_skipped_files.append(os.path.join(absolute_filename))
        logger.error('Unable to set date {a} for filename {b} '.format(a=date, b=filename) + str(w))


def parseFileNameForTitle(filename):
    filename = filename.replace(' ', '-').replace(',','')
    # https://regex101.com/r/rLOK5f/4
    m1 = re.search(r'([A-Z][a-zA-Z\-\d\.\_\'\(\)]+)\.((jpg)|(pdf))', filename)
    if m1 and 'IMG_' not in filename:
        title_and_description = m1.group(1)
        title_and_description_list = re.split('-|_', title_and_description)
        for (index, word) in enumerate(title_and_description_list):
            if word == 'Sac':
                title_and_description_list[index] = 'Sacramento'
            elif 'Sw' in word:
                # split word into own list
                # ['Sw', 'Bhashya', 'Sw', 'Shraddha', 'Sw', 'Asesha']
                expanded_list = re.sub('(?!^)([A-Z][a-z]+)', r' \1', word).split()
                for (i, item) in enumerate(expanded_list):
                    if item == 'Sw' or item == 'Sw.':
                        expanded_list[i] = 'Swami'
                    elif expanded_list[i-1] == 'Swami':
                            if 'nanda' not in item:
                                expanded_list[i] = item + 'nanda'

                expanded = ' '.join(expanded_list)
                title_and_description_list[index] = expanded
            elif 'album' in word.lower() or 'abum' in word.lower():
                description_word_index = index - 1
                title_and_description_list.pop(index)
            else:
                # split camel case
                word = ' '.join(re.sub('(?!^)([A-Z][a-z]+)', r' \1', word).split())
                title_and_description_list[index] = word

        title_and_description = ' '.join(title_and_description_list)
        logger.info('Title and Description >>>{a}<<< parsed from filename {b}'.format(a=title_and_description, b=filename))
        return title_and_description
    else:
        logger.error(('Unable to parse title from filename {0}'.format(filename)))
        title_skipped_files.append(os.path.join(absolute_filename))


def setTitleMetaData(filename, title):
    if filename is None or title is None:
        logger.error('Filename {a} or Title {b} is empty'.format(a=filename, b=title))
        return False
    cmd = '-Title=' + title
    cmd_list = [LIB_CMD, cmd, filename]
    if not demo_mode:
        logger.debug('Command : {0}'.format(str(cmd_list)))
    try:
        if not demo_mode:
            result = subprocess.check_output(cmd_list)
        return True
    except Exception as w:
        title_skipped_files.append(os.path.join(absolute_filename))
        logger.error('Unable to set title {a} for filename {b} '.format(a=title, b=filename) + str(w))


def setCopyrightMetaData(filename):
    # cmd = 'set Exif.Photo.Copyright' + 'Vedanta Society Sacramento, CA'
    cmd = '-copyright=' + 'Vedanta Society Sacramento, CA'
    cmd_list = [LIB_CMD, cmd, filename]
    if not demo_mode:
        logger.debug('Command : {0}'.format(str(cmd_list)))
    try:
        if not demo_mode:
            result = subprocess.check_output(cmd_list)
        return True
    except Exception as e:
        logger.error('Unable to set copyright for filename {0} '.format(filename) + str(e))


if __name__ == "__main__":

    # set vars
    LIB_LOCATION = '/usr/local/bin'
    LIB_CMD = LIB_LOCATION + '/exiftool'

    FOLDER_ROOT = '/Users/kkaul/Documents/VSPhotos/src/'
    FOLDER_LOCATION_LIST = [
                            '2013-10',
                            '2013-11',
                            '2013-12',
                            '2014-01-And-2014-02',
                            '2014-03-To-2014-12',
                            '2015-01-And-2015-02',
                            '2015-03-And-2015-04',
                            '2015-05',
                            '2015-06',
                            '2015-07'
                            ]

    global_count = 0
    date_count = 0
    date_skipped_files = []
    title_count = 0
    title_skipped_files = []

    # control flag
    # when True, it will skip metadata write operations on image (useful for dry run and log analysis)
    # when False, it will run the actual script (exiv2 lib call)
    demo_mode = True

    logging.basicConfig(level=logging.INFO,
                        filename="log.txt",
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logger = logging.getLogger(__name__)

    for folder_location in FOLDER_LOCATION_LIST:
        folder_location = FOLDER_ROOT + folder_location
        logger.debug('\nStart processing folder {0}'.format(folder_location))
        for eachFile in os.listdir(folder_location):
            global_count += 1
            absolute_filename = os.path.join(folder_location, eachFile)
            if not demo_mode:
                logger.debug('Absoulte Filename : {0}'.format(absolute_filename))
            logger.debug('Start processing file {0}'.format(eachFile))

            # getMetaData before making any changes
            if not demo_mode:
                logger.info(getMetaData(absolute_filename))

            # set copyright
            setCopyrightMetaData(absolute_filename)

            # title and description logic
            parsed_title = parseFileNameForTitle(eachFile)
            if setTitleMetaData(absolute_filename, parsed_title):
                title_count += 1

            # date logic
            if validFileName(eachFile):
                parsed_date = parseFileNameForDate(eachFile)
                if setDateMetaData(absolute_filename, parsed_date):
                    date_count += 1
            else:
                date_skipped_files.append(os.path.join(absolute_filename))

            # getMetaData after all changes
            if not demo_mode:
                logger.info(getMetaData(absolute_filename))

            # break
        # break

logger.info('Total number of files processed : {0}'.format(global_count))
logger.info('Files processed for date : {0}'.format(date_count))
logger.info('Files skipped for date : {0}'.format(len(date_skipped_files)))
if date_skipped_files:
    logger.info('\n' + '\n'.join(date_skipped_files))
logger.info('Files processed for Title : {0}'.format(title_count))
logger.info(('Files skipped for title : {0}'.format(len(title_skipped_files))))
if title_skipped_files:
    logger.info('\n' + '\n'.join(title_skipped_files))
