class ImagesByLabel:
    """
    A map from label, in the form of an integer, to the list of all digit images with that label.
    """
    def __init__(self, image_provider_):
        self.image_provider = image_provider_

        self._parse_labels()

    def _parse_labels(self):
        self.labels = {label: [] for label in range(10)}

        self.num_labels, label_bytes = self.image_provider.get_labels()
        for label_index in range(self.num_labels):
            label = label_bytes[label_index]
            self.labels[label].append(label_index)

    def __getitem__(self, key):
        return ImageList(self.image_provider, self.labels[key])

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
    def __init__(self, image_provider_, images_with_label_):
        self.image_provider = image_provider_
        self.images_with_label_ = images_with_label_

    def __getitem__(self, key):
        if key >= len(self.images_with_label_) or 0 > key:
            raise IndexError("Image number {} out of range, must be between 0 and {}"
                             .format(key, len(self.images_with_label_) - 1))

        image_bytes, num_rows, num_cols = self.image_provider.get_image_bytes(self.images_with_label_[key])
        output = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

        for row in range(num_rows):
            for col in range(num_cols):
                output[row][col] = image_bytes[row * num_cols + col]
        return output

    def __len__(self):
        return len(self.images_with_label_)

    def __setitem__(self, key, value):
        raise NotImplementedError
