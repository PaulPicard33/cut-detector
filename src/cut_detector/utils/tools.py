import sys
import numpy as np


def display_progress(
    message,
    current,
    total,
    precision=1,
    additional_message="",
) -> None:
    """
    Nice display of progress.
    """
    percentage = round(current / total * 100, precision)
    padded_percentage = str(percentage).ljust(precision + 3, "0")
    display_message = f"\r{message}: {padded_percentage}%"
    # Display additional message
    if additional_message:
        display_message += " | " + additional_message
    sys.stdout.write(display_message)
    sys.stdout.flush()


def re_organize_channels(image: np.ndarray) -> np.ndarray:
    """
    Expect a 4 dimensions image.
    Re-organize channels to get TXYC order.
    """
    if image.ndim != 4:
        raise ValueError("Expect a 4 dimensions image.")

    # Get dimension index of smallest dimension, i.e. channels
    channels_dimension_index = np.argmin(image.shape)
    channels_dimension = image.shape[channels_dimension_index]
    if channels_dimension != 3:
        raise ValueError("Expect 3 channels: SiR-tubulin/MKLP1/Phase contrast, in that order.")
    # Put channels at the back
    image = np.moveaxis(image, channels_dimension_index, 3)

    # Get dimension index of second smallest dimension, i.e. time
    second_dimension_index = np.argsort(image.shape)[1]
    # Put time at the front
    image = np.moveaxis(image, second_dimension_index, 0)

    return image
