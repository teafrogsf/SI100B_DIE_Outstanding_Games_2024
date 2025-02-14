from PIL import Image
import sys

def fix_image_srgb_profile(file_path):
    img = Image.open(file_path)
    img.save(file_path, icc_profile=None)

if __name__ == '__main__':
    pic = sys.argv[1]
    fix_image_srgb_profile(pic)