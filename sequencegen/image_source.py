class ImagesByLabel:
    """
    A map from label, in the form of an integer, to the list of all digit images with that label.
    """
    def __init__(self, image_provider_):
        self.image_provider = image_provider_

        image_bytes = image_provider_.get_image_bytes(4, 12)
        self.num_images = int.from_bytes(image_bytes[0:4], byteorder='big', signed=False)
        self.num_rows = int.from_bytes(image_bytes[4:8], byteorder='big', signed=False)
        self.num_columns = int.from_bytes(image_bytes[8:12], byteorder='big', signed=False)

        self._parse_labels()

    def _parse_labels(self):
        self.labels = {label: [] for label in range(10)}

        self.num_labels, label_bytes = self.image_provider.get_labels()
        for label_index in range(self.num_labels):
            label = label_bytes[label_index]
            self.labels[label].append(label_index)

    def __getitem__(self, key):
        return ImageList(self.image_provider, self.labels[key], self.num_rows, self.num_columns)

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __iter__(self):
        return iter(self.labels.keys())

    def __len__(self):
        return len(self.labels)


class ImageList:
    """
    A proxy object which exposes the digit images of a given label as a list, backed by the digit image file.
    """
    def __init__(self, binary_provider_, indicies_, num_rows_, num_columns_):
        self.binary_provider = binary_provider_
        self.indicies = indicies_
        self.num_rows = num_rows_
        self.num_columns = num_columns_

    def _get_image_bytes(self, index):
        length = self.num_rows * self.num_columns
        offset = 16 + length * index
        return self.binary_provider.get_image_bytes(offset, length)

    def __getitem__(self, key):
        if key >= len(self.indicies) or 0 > key:
            raise IndexError("Image number {} out of range, must be between 0 and {}"
                             .format(key, len(self.indicies) - 1))

        output = [[0 for _ in range(self.num_columns)] for _ in range(self.num_rows)]

        image_bytes = self._get_image_bytes(self.indicies[key])
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                output[row][col] = image_bytes[row * self.num_columns + col]
        return output

    def __len__(self):
        return len(self.indicies)

    def __setitem__(self, key, value):
        raise NotImplementedError
