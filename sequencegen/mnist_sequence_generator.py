import random
from functools import reduce

import numpy
import png
import argparse
import os

from sequencegen.image_source import ImagesByLabel
from sequencegen.image_downloader import ImageDownloader

pad_left_config = False


def generate_mnist_sequence(digits, spacing_range, image_width):
    """
    Generate a numpy array encoding an image of a sequence of digits with greyscale pixel values between 0 and 1.
    :param digits: A list of integers between 0 and 9 inclusive. The generated image image array will be of that
    sequence.
    :param spacing_range: The upper and lower bounds of the width of the spacers inserted between digits.
    :param image_width: The number of columns in the result.  The concatenation will be truncated or padded on the right
    to make that number of columns.
    :return: A numpy array encoding an image of a sequence of digits.
    """
    image_source = ImageDownloader()
    return _normalize_to_numpy(_generate_sequence_helper(digits, spacing_range, image_width, image_source))


def _generate_sequence_helper(digits, spacing_range, image_width, image_source, random_=random):
    """
    Generate a Python list encoding an image of a sequence of digits with greyscale pixel values between 0 and 255.
    :param digits: A list of integers between 0 and 9 inclusive. The generated image image array will be of that
    sequence.
    :param spacing_range: A tuple containing the upper and lower bounds of the width of the spacers inserted between
    digits.
    :param image_width: The number of columns in the result.  The concatenation will be truncated or padded on the right
    to make that number of columns.
    :return: A numpy array encoding an image of a sequence of digits.
    """
    if not reduce((lambda x, y: x and y), map((lambda z: isinstance(z, int) and 0 <= z < 10), digits)):
        raise ValueError("digits must be a list of integers between 0 and 9.")

    if not (isinstance(spacing_range, tuple) and spacing_range.__len__() == 2
            and 0 <= spacing_range[0] <= spacing_range[1]):
        raise ValueError("spacing_range must be a tuple or two integers, with the second not lower than the first.")

    if not isinstance(image_width, int) and image_width < 0:
        raise ValueError("image_width must be a non-negative integer")

    images = ImagesByLabel(image_source)

    chosen_images = []
    for digit in digits:
        chosen_image_index = random_.randrange(len(images[digit]))
        chosen_images.append(images[digit][chosen_image_index])
    num_rows = max(map(len, chosen_images))
    return _concatenate_lists(_add_separators(chosen_images, spacing_range, pad_left_config, random_),
                              num_rows, image_width)


def _normalize_to_numpy(image):
    """
    Convert a Python list encoding an image of a sequence of digits with greyscale pixel values between 0 and 255,
    to a numpy array of pizel values ranging from 0 to 1.
    :param image: The image as a Python list.
    :return: The image as a numpy array.
    """
    num_rows = len(image)
    num_cols = 0
    if num_rows > 0:
        num_cols = len(image[0])
    normalized_image = numpy.ones(shape=(num_rows, num_cols))
    for image_row in range(len(image)):
        for image_col in range(len(image[image_row])):
            normalized_image[image_row][image_col] = image[image_row][image_col] / 255
    return normalized_image


def _concatenate_lists(images, num_rows, num_cols):
    """
    Concatenate a list of image lists into a numpy arrays.
    :param images: A list of image arrays to concatenate.
    :param num_rows: The number of rows in the images.
    :param num_cols: The number of columns in the result.  The concatenation will be truncated or padded on the right to
    make that number of columns.
    :return: A numpy array containing the concatenated lists.
    """
    output_array = [[255 for _ in range(num_cols)] for _ in range(num_rows)]
    current_image_index = 0
    current_output_col = 0
    current_image_col = 0
    # skip past empty images
    while current_image_index < len(images) and len(images[current_image_index][0]) == 0:
        current_image_index += 1
    while current_output_col < num_cols and current_image_index < len(images):
        array_cols = len(images[current_image_index][0])
        for current_image_row in range(len(images[current_image_index])):
            output_array[current_image_row][current_output_col] \
                = 255 - images[current_image_index][current_image_row][current_image_col]

        current_output_col += 1
        current_image_col += 1
        if current_image_col == array_cols:
            current_image_col = 0
            current_image_index += 1
            # skip past empty images
            while current_image_index < len(images) and len(images[current_image_index][0]) == 0:
                current_image_index += 1

    return output_array


def _add_separators(images, spacing_range, pad_left, random_):
    """
    Insert random-width, single-row spacer lists between each lists in arrays.
    :param images: A list of digit image lists to place spacers between.
    :param spacing_range: A tuple of two integers, the inclusive upper and lower bounds of the random spacer width.
    :param pad_left: If true a spacer will be placed before the first digit.
    :return: A new list containing the values or arrays interspersed with spacers.
    """
    output = []
    for index in range(len(images)):
        if index != 0 or pad_left:
            spacing = random_.randrange(spacing_range[0], spacing_range[1] + 1)
            output.append([[0 for _ in range(spacing)]])
        output.append(images[index])
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sequence")
    parser.add_argument("min_spacing")
    parser.add_argument("max_spacing")
    parser.add_argument("image_width")
    args = parser.parse_args()

    sequence_string = args.sequence
    if not sequence_string.isdigit():
        raise ValueError("Argument sequence must be a sequence of digits.")

    sequence = [int(x) for x in list(sequence_string)]

    if not args.min_spacing.isdigit():
        raise ValueError("Argument min_spacing must be an integer.")
    if not args.max_spacing.isdigit():
        raise ValueError("Argument max_spacing must be an integer.")
    if not args.image_width.isdigit():
        raise ValueError("Argument image_width must be an integer.")

    min_spacing = int(args.min_spacing)
    max_spacing = int(args.max_spacing)
    width = int(args.image_width)

    image_list = _generate_sequence_helper(sequence, (min_spacing, max_spacing), width, ImageDownloader())
    cwd = os.getcwd()

    png.from_array(image_list, 'L').save(os.path.join(cwd, "{}.png".format(sequence_string)))
