import numpy as np

# https://stackoverflow.com/a/39270509/699934
def copy_image_to_np_array(image):
    return np.array(np.asarray(image, dtype='uint8')[..., :3][:, :, ::-1])