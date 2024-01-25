from PIL import Image, ImageEnhance, ImageFilter, ImageStat
import os
import shutil

def is_high_quality(image_path, resolution_threshold=100000, clarity_threshold=100):
    with Image.open(image_path) as img:
        # Check resolution
        width, height = img.size
        if width * height < resolution_threshold:
            return False

        # Check clarity
        img_gray = img.convert('L')
        sharpness = ImageEnhance.Sharpness(img_gray).enhance(3.0).filter(ImageFilter.FIND_EDGES)
        image_clarity = sharpness.convert('L')
        image_var = ImageStat.Stat(image_clarity).stddev[0]
        if image_var < clarity_threshold:
            return False

        return True

def save_grayscale_image(image_path, output_folder, quality=95):
    with Image.open(image_path) as img:
        grayscale_image = img.convert('L')
        filename = os.path.basename(image_path)
        save_path = os.path.join(output_folder, filename)
        save_path = os.path.splitext(save_path)[0] + ".jpg"
        grayscale_image.save(save_path, format='JPEG', quality=quality)

def select_high_quality_images(input_folder, output_folder, max_images=200):
    high_quality_images = []
    count = 0
    for filename in os.listdir(input_folder):
        if count >= max_images:
            break
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            if is_high_quality(image_path):
                high_quality_images.append(image_path)
                save_grayscale_image(image_path, output_folder)
                count += 1
    return high_quality_images

# Example usage
input_folder = 'SEM_Custom_Dataset'
output_folder = 'high_quality'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


high_quality_images = select_high_quality_images(input_folder, output_folder, max_images=200)

print("High-quality grayscale images saved in the output folder:")
for image in high_quality_images:
    print(image)

