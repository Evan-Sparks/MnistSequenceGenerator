import urllib.request
import os.path
import gzip
import tempfile


def _download_file(url, path):
    if os.path.isfile(path):
        print("File {} already present, not downloading.".format(path))
    else:
        print("Downloading file from {} to {}".format(url, path))
        urllib.request.urlretrieve(url, path)


def get_label_file_path():
    return os.path.join(tempfile.gettempdir(), "train-labels-idx1-ubyte.gz")


def get_image_file_path():
    return os.path.join(tempfile.gettempdir(), "train-images-idx3-ubyte.gz")


def get_label_url():
    return "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"


def get_image_url():
    return "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"


class ImageDownloader:
    def __init__(self):
        _download_file(get_image_url(), get_image_file_path())
        _download_file(get_label_url(), get_label_file_path())
        image_bytes = self._get_bytes_from_file(4, 12)
        self.num_images = int.from_bytes(image_bytes[0:4], byteorder='big', signed=False)
        self.num_rows = int.from_bytes(image_bytes[4:8], byteorder='big', signed=False)
        self.num_columns = int.from_bytes(image_bytes[8:12], byteorder='big', signed=False)

    @staticmethod
    def _get_bytes_from_file(start_offset, length):
        """
        Get a block of bytes from the digit image file.
        :param start_offset: The offset in the digit image file to start reading from.
        :param length: The length of the block of bytes to return.
        :return: A contiguous block of bytes.
        """
        image_file = gzip.open(get_image_file_path())
        image_file.seek(start_offset)
        image_bytes = image_file.read(length)
        image_file.close()
        return image_bytes

    def get_image_bytes(self, index):
        """
        Get the bytes associated with the image in position index in the file.
        :param index: The index of the image in the file, note the index is global not just among images of a given
        label.
        :return: A tuple conatinaing a contiguous block of bytes representing the image, an the number of rows as an int
        and the number of columns as an int.
        """
        length = self.num_rows * self.num_columns
        offset = 16 + length * index
        return self._get_bytes_from_file(offset, length), self.num_rows, self.num_columns

    @staticmethod
    def get_labels():
        """
        Get the number of labels and label bytes from the labels file.
        :return: The number of labels in the file and a list of bytes of that length containing labels.
        """
        label_file = gzip.open(get_label_file_path())
        label_file.seek(4)
        num_labels = int.from_bytes(label_file.read(4), byteorder='big', signed=False)
        label_bytes = label_file.read(num_labels)
        label_file.close()
        return num_labels, label_bytes
