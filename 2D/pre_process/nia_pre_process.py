import os
import shutil
import cv2
import pandas as pd

# Define paths
base_path = os.getcwd()
current_path = os.path.join(base_path, 'dataset')
join_path = os.path.join(base_path, 'nia_join')
resize_path = os.path.join(base_path, 'nia_resize')
split_path = os.path.join(base_path, 'nia_split')
class_folders = ['건축', '공예', '서예', '악기', '조각', '회화']
class_paths = [os.path.join(split_path, c) for c in class_folders]
class_split_path = os.path.join(base_path, 'nia_split_class')

# Create directories
paths_to_create = [join_path, resize_path, split_path, class_split_path] + class_paths
for path in paths_to_create:
    os.makedirs(path, exist_ok=True)

# Extract and move images
def move_images(src_path, join_path, conditions):
    for root, _, files in os.walk(src_path):
        files.sort()
        for file in files:
            if all(cond(file) for cond in conditions):
                shutil.move(os.path.join(root, file), join_path)
                
conditions1 = [
    lambda f: len(f.split('_')[-1]) == 5,
    lambda f: f.split('.')[-1] != 'xlsx',
    lambda f: f[0] != '.',
    lambda f: f[0] != 'C'
]

conditions2 = [
    lambda f: len(f.split('-')[-1]) in [5, 6],
    lambda f: f.split('.')[-1] not in ['xlsx', 'xlsb'],
    lambda f: f[0] != '.',
    lambda f: f[0] != 'C'
]

move_images(current_path, join_path, conditions1)
print('1 img done')
move_images(current_path, join_path, conditions2)
print('2 img done')

# Resize images
def resize_images(src_path, dst_path, size=(800, 600)):
    for root, _, files in os.walk(src_path):
        files.sort()
        for file in files:
            path = os.path.join(root, file)
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            if img is not None:
                resized_img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
                cv2.imwrite(os.path.join(dst_path, file), resized_img)

resize_images(join_path, resize_path)
print('Resize done')

# Extract labels from Excel
def extract_labels_from_excel(src_path, filename, skiprows=None):
    for root, _, files in os.walk(src_path):
        files.sort()
        if filename in files:
            csv = pd.read_excel(os.path.join(root, filename), skiprows=skiprows)
            return csv.to_dict()

goodgate_labels = extract_labels_from_excel(current_path, 'goodgate.xlsx')
wepco_labels = extract_labels_from_excel(current_path, 'wepco.xlsx', skiprows=[0])
image2d_labels = extract_labels_from_excel(current_path, '2dimg.xlsx', skiprows=[0])
print('Excel extraction done')

# Move images to class folders
def move_to_class_folders(src_path, dst_path, labels):
    for root, _, files in os.walk(src_path):
        files.sort()
        for file in files:
            filename, classname = labels['파일명'], labels['중분류(분야)']
            for f, c in zip(filename.values(), classname.values()):
                if f == file.split('_')[0] or f == file.split('-')[0]:
                    shutil.move(os.path.join(root, file), os.path.join(dst_path, c, file))

move_to_class_folders(resize_path, split_path, goodgate_labels)
move_to_class_folders(resize_path, split_path, wepco_labels)
move_to_class_folders(resize_path, split_path, image2d_labels)
print('Class split done')

# Split data into train, test, and validation sets
def split_data(src_path, dst_path, split_ratio=(0.8, 0.1, 0.1)):
    train_path = os.path.join(dst_path, 'train')
    test_path = os.path.join(dst_path, 'test')
    val_path = os.path.join(dst_path, 'val')
    for path in [train_path, test_path, val_path]:
        for c in class_folders:
            os.makedirs(os.path.join(path, c), exist_ok=True)
    
    for class_folder in class_folders:
        class_src_path = os.path.join(src_path, class_folder)
        files = sorted(os.listdir(class_src_path))
        mid = int(len(files) * split_ratio[0])
        last = int(len(files) * split_ratio[1])
        
        for i, file in enumerate(files):
            if i < mid:
                shutil.move(os.path.join(class_src_path, file), os.path.join(train_path, class_folder, file))
            elif i < mid + last:
                shutil.move(os.path.join(class_src_path, file), os.path.join(test_path, class_folder, file))
            else:
                shutil.move(os.path.join(class_src_path, file), os.path.join(val_path, class_folder, file))

split_data(split_path, class_split_path)
print('Data split done')
print('All done')

print('All done')
