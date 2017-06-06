# MnistSequenceGenerator

A simple script to generate images of handwritten numbers by concatenating digit images from the [MNIST database](http://yann.lecun.com/exdb/mnist/).

Provides the following function
```python
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
```

as well as a command line script which saves a .png image of the produced digit sequence.

Installing on a fresh Ubuntu VM.
```
sudo apt-get update
sudo apt-get -y install python3-pip
git clone https://github.com/Evan-Sparks/MnistSequenceGenerator.git
sudo python3 setup.py install
```

Executing from the command line.
```
# example with sequence = 0123456789, min spacing = 1, max spacing = 10, image_width = 400
# outputs a file named 0123456789.png in the current working directory
python3 sequencegen/mnist_sequence_generator.py 0123456789 1 10 400
```

Implementation Details:
The implementation is made up of three components. A data source in image_source.py, a parser and data interface in
image_source.py, and an image generator in mnist_sequence_generator.py.

The data source downloads and reads the MNIST image and label files to a temporary file if they are not already present.
It exposes functions which return, as an array of bytes, the list of labels and the pixels of an image at a given index
within a file, as well as the dimensions of the image and the number of labels.  The data source reads images into
memory individually by index.  This results in reduced performance in the form of more separate reads from disk but
gains in reduced startup time and more importantly allows for extension to data sets too large to fit in memory.
Unlike the images, the labels are fully ingested.  This is because the random selection of image by label requires the
full inventory of labels.

The parser is a dict-like data structure wrapping the data source.  It maps labels to list-like objects proxying all
images with that label.  When the list's get item function is called for index i it reads the bytes of the ith image
which has the given label, parses it into a list of lists of ints and returns it in the form of
list[row][col] = pixel_val.

The image generator takes the digit images provided by the parser and concatenates them into image sequences before
outputting them in numpy or png formats.  Random spacing is inserted between the digit images by inserting single-row
"images" of white background pixels between the digit images prior to concatenation.  This is slightly less efficient
as it results in copying the spacer pixels into the output rather than simply skipping columns, but keeping the
concatenation function general by avoiding building the spacing into it significantly improves it's extensibility.
