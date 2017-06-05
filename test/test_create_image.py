import unittest


from sequencegen import mnist_sequence_generator


class TestImageArrayGen(unittest.TestCase):
    def test_make_image(self):
        rand = random_mock()
        image_list = mnist_sequence_generator._generate_sequence_helper([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], (10, 25), 200,
                                                                        image_dowloader_mock(), rand)
        for row in range(len(image_list)):
            for col in range(len(image_list[row])):
                in_range = inside_expected_range(row, col)
                if in_range >= 0:
                    assert image_list[row][col] == in_range * 10
                else:
                    assert image_list[row][col] == 255


def inside_expected_range(row, col):
    for digit in range(10):
        if row <= digit and (10 * digit + sum(range(digit + 1))) <= col \
                < (10 * digit + sum(range(digit + 1)) + digit + 1):
            return digit
    return -1


class image_dowloader_mock:
    def get_image_bytes(self, index):
        rows = (index + 1)
        cols = (index + 1)
        return bytes([255 - index * 10 for _ in range(rows * cols)]), rows, cols

    def get_labels(self):
        return 10, bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


class random_mock:
    def randrange(self, start, stop=None):
        if stop is not None:
            return start
        else:
            return start - 1
