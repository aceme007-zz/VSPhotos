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
    return False


def parseFileNameForDate(name):
    # extract date
    m = re.match(r'(\d{4}[\d\-]*)-', name)
    if m:
        val = m.group(1)
        logger.debug('Date {a} is parsed from filename {b}'.format(a=val, b=name))
        return m.group(1)    
    else:
        logger.error('Unable to parse date from filename {0}'.format(name))
        skipped_files.append(os.path.join(FOLDER_LOCATION, eachFile))


def normalizeDate(date):
    # return 2015:10:24 20:00:00 format
    m1 = re.match(r'(\d{4})\-(\d{1,2})\-(\d{1,2})', date)
    if m1:
        val = m1.group(1) + ':' + m1.group(2).zfill(2) + ':' + m1.group(3).zfill(2) + ' 00:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val
    m2 = re.match(r'(\d{4})\-(\d{1,2})', date)
    if m2:
        val = m2.group(1) + ':' + m2.group(2).zfill(2) + ':01 00:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val
    m3 = re.match(r'(\d{4})\-', date)
    if m3:
        val = m3.group(1) + ':01:01 00:00:00'
        logger.debug('Normalized date {0}'.format(val))
        return val


def setDateMetaData(filename, date):
    if filename is None or date is None:
        logger.error('Filename {a} or Date {b} is empty'.format(a=filename, b=date))
        return False
    cmd = 'set Exif.Photo.DateTimeOriginal ' + str(normalizeDate(date))
    cmd_list = [LIB_CMD, "-M", cmd, filename]
    if not demo_mode:
        logger.debug('Command : {0}'.format(str(cmd_list)))
    try:
        if not demo_mode:
            result = subprocess.check_output(cmd_list)
        return True
    except Exception as w:
        skipped_files.append(os.path.join(FOLDER_LOCATION, eachFile))
        logger.error('Unable to set date {a} for filename {b} '.format(a=date, b=filename) + str(w))


if __name__ == "__main__":

    # set vars
    LIB_LOCATION = '/Users/kkaul/Documents/VSPhotos/dist'
    LIB_CMD = LIB_LOCATION + '/macosx/bin/exiv2'
    FOLDER_LOCATION = '/Users/kkaul/Documents/VSPhotos/src/2013-10'

    count = 0
    skipped_files = []

    # when True, it will skip metadata write operations on image (useful for dry run and log analysis)
    # when False, it will run the actual script (exiv2 lib call)
    demo_mode = True


    logging.basicConfig(level=logging.DEBUG,
                        filename="log.txt",
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logger = logging.getLogger(__name__)

    for eachFile in os.listdir(FOLDER_LOCATION):
        logger.debug('Start processing file {0}'.format(eachFile))
        if validFileName(eachFile):
            absolute_filename = os.path.join(FOLDER_LOCATION, eachFile)
            if not demo_mode:
                logger.debug('Absoulte Filename : {0}'.format(absolute_filename))
            if not demo_mode:
                logger.info(getMetaData(absolute_filename))
            parsed_date = parseFileNameForDate(eachFile)
            if setDateMetaData(absolute_filename, parsed_date):
                count += 1
                if not demo_mode:
                    logger.info(getMetaData(absolute_filename))
        else:
            skipped_files.append(os.path.join(FOLDER_LOCATION, eachFile))

logger.info('Total number of files processed : {0}'.format(count))
logger.info('Skipped Files {0} :'.format(len(skipped_files)))
logger.info('\n' + '\n'.join(skipped_files))
