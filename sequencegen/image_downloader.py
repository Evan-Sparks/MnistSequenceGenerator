import urllib.request
import os.path
import gzip
import configparser


def _download_file(url, path):
    if os.path.isfile(path):
        print("File {} already present, not downloading.".format(path))
    else:
        print("Downloading file from {} to {}".format(url, path))
        urllib.request.urlretrieve(url, path)


class ImageDownloader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
        _download_file(self.get_image_url(), self.get_image_file_path())
        _download_file(self.get_label_url(), self.get_label_file_path())

    def get_image_url(self):
        return self.config.get("ImageDownloader", "ImagesUrl")

    def get_label_url(self):
        return self.config.get("ImageDownloader", "LabelsUrl")

    def get_image_file_path(self):
        return self.config.get("ImageDownloader", "ImagesFilePath")

    def get_label_file_path(self):
        return self.config.get("ImageDownloader", "LabelsFilePath")

    def get_image_bytes(self, start_offset, length):
        """
        Get a block of bytes from the digit image file.
        :param start_offset: The offset in the digit image file to start reading from.
        :param length: The length of the block of bytes to return.
        :return: A contiguous block of bytes.
        """
        image_file = gzip.open(self.get_image_file_path())
        image_file.seek(start_offset)
        image_bytes = image_file.read(length)
        image_file.close()
        return image_bytes

    def get_labels(self):
        """
        Get the number of labels and label bytes from the labels file.
        :return: The number of labels in the file and a list of bytes of that length containing labels.
        """
        label_file = gzip.open(self.get_label_file_path())
        label_file.seek(4)
        num_labels = int.from_bytes(label_file.read(4), byteorder='big', signed=False)
        label_bytes = label_file.read(num_labels)
        label_file.close()
        return num_labels, label_bytes
