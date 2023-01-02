import os
import pandas as pd
import numpy as np
import cv2
import csv
import shutil



# Unzip all files


#! Creating a folder
current_path = os.path.join(os.getcwd(),'dataset') # Orisinal datasets locaion
join_path = os.path.join(os.getcwd(),'nia_join') # Extract jpg files only
resize_path =  os.path.join(os.getcwd(),'nia_resize') # join_path files -> resize

split_path = os.path.join(os.getcwd(),'nia_split') # Class separation
clas_a = os.path.join(os.getcwd(),'nia_split/건축')
clas_b = os.path.join(os.getcwd(),'nia_split/공예')
clas_c = os.path.join(os.getcwd(),'nia_split/서예')
clas_d = os.path.join(os.getcwd(),'nia_split/악기')
clas_e = os.path.join(os.getcwd(),'nia_split/조각')
clas_f = os.path.join(os.getcwd(),'nia_split/회화')
 
class_path = os.path.join(os.getcwd(), 'nia_split_class') # Dataset split (8:1:1)

pass_list = [join_path, resize_path, split_path, 
             clas_a, clas_b, clas_c, clas_d, clas_e, clas_f, class_path]

for path in pass_list:
    os.makedirs(path, exist_ok=True)


#! Extract GOODGATE, WEPCO images 
for root, dirs, files in os.walk(current_path):
    dirs.sort()
    files.sort()
    for file in files:
        if len(file.split('_')[-1])== 5 and file.split('.')[-1] != 'xlsx' and file[0] != '.' and file[0] != 'C':  
            path = os.path.join(root, file) 
            shutil.move(path, join_path)
            
print('1 img done')
    
    
#! Extract 2DIMAGE images 
for root, dirs, files in os.walk(current_path):
    dirs.sort()
    files.sort()
    for file in files:
        if len(file.split('-')[-1])== 5 and file.split('.')[-1] != 'xlsx' and file.split('.')[-1] != 'xlsb' and file[0] != '.' and file[0] != 'C': 
            path = os.path.join(root, file)
            shutil.move(path, join_path)
        
        elif len(file.split('-')[-1])== 6 and file.split('.')[-1] != 'xlsx' and file.split('.')[-1] != 'xlsb' and file[0] != '.' and file[0] != 'C': 
            path = os.path.join(root, file)
            shutil.move(path, join_path)
           
print('2 img done')


#! Images resize
for root, dirs, files in os.walk(join_path):
    files.sort()
    for file in files:   
        if len(file.split('_')[-1])== 5 and file.split('.')[-1] != 'xlsx' and file[0] != '.' and len(file.split('-')[-1]) != 6:   
            path = os.path.join(root, file)
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            try:
                imgfile = cv2.resize(img, (800,600), interpolation=cv2.INTER_AREA)
                name = os.path.basename(path)
                paths = os.path.join(resize_path, name)
                cv2.imwrite(paths, imgfile)
            except:
                pass
            
        if len(file.split('-')[-1])== 5 and file.split('.')[-1] != 'xlsx' and file[0] != '.' and len(file.split('-')[-1]) != 6:   
            path_ = os.path.join(root, file)
            img_ = cv2.imread(path_, cv2.IMREAD_COLOR)
            try:
                imgfile_ = cv2.resize(img_, (800,600), interpolation=cv2.INTER_AREA)
                name_ = os.path.basename(path_)
                paths_ = os.path.join(resize_path, name_)
                cv2.imwrite(paths_, imgfile_)
            except:
                pass
            
        
        elif len(file.split('-')[-1])== 6 and file.split('.')[-1] != 'xlsx' and file[0] != '.':   
            path_ = os.path.join(root, file)
            img_ = cv2.imread(path_, cv2.IMREAD_COLOR)
            try:
                imgfile_ = cv2.resize(img_, (800,600), interpolation=cv2.INTER_AREA)
                name_ = os.path.basename(path_)
                paths_ = os.path.join(resize_path, name_)
                cv2.imwrite(paths_, imgfile_)
            except:
                break
print('Resize done')


#! Extract GOODGATE label information from Excel
for root, dirs, files in os.walk(current_path):
    files.sort()
    for file in files: 
        if file.split('.')[-1] == 'xlsx' and file == 'goodgate.xlsx': 
            csv = pd.read_excel(os.path.join(root,file))
            csv_dict = csv.to_dict()
            
            try:
                filename = csv_dict['파일명']
                classname = csv_dict['중분류(분야)']

                filename_list = list(filename.values())[1:]
                classname_list = list(classname.values())[1:]
                
            except:
                pass

print('gg excel done')

#! Extract WEPCO label information from Excel
for root, dirs, files in os.walk(current_path):
    files.sort()
    for file in files: 
        if file.split('.')[-1] == 'xlsx' and file == 'wepco.xlsx': 
            csv = pd.read_excel(os.path.join(root,file), skiprows=[0])
            csv_dict = csv.to_dict()
            
            try:
                filename_b = csv_dict['파일명']
                classname_b = csv_dict['중분류(분야)']

                filename_list_b = list(filename_b.values())[1:]
                classname_list_b = list(classname_b.values())[1:]
                
            except:
                pass

print('we excel done')


#! Divide GOODGATE Class
for root, dirs, files in os.walk(resize_path):
    files.sort()   
    for file in files:
        for (clas,file_) in zip(classname_list,filename_list):
            if file_ == file[:-6] :
                temp = len(file)
                path = os.path.join(root, file[:temp-4]+file[-4:])
                spl_path = os.path.join(split_path,clas,file)                    
                shutil.move(path, spl_path)
print('gg split done')


#! Divide WEPCO Class
for root, dirs, files in os.walk(resize_path):
    files.sort()   
    for file in files:
        for (clas,file_) in zip(classname_list_b,filename_list_b):
            if file_ == file[:-6] :
                temp = len(file)
                path = os.path.join(root, file[:temp-4]+file[-4:])
                spl_path = os.path.join(split_path,clas,file)                    
                shutil.move(path, spl_path)
print('we split done')


#! Extract 2DIMAGE label information from Excel
for root, dirs, files in os.walk(current_path):
    files.sort()
    for file in files:     
        if file.split('.')[-1] == 'xlsx' and file == '2dimg.xlsx':
            csv = pd.read_excel(os.path.join(root,file), skiprows=[0])
            csv_dict = csv.to_dict()
            
            try: 
                filename_3 = csv_dict['신) 이미지 파일명']
                classname_3 = csv_dict['중분류']

                filename_lists = list(filename_3.values())[0:]
                classname_lists = list(classname_3.values())[0:]  
                
            except :
                pass
print('2d excel done')
                

#! Divide 2DIMAGE Class
for root, dirs, files in os.walk(resize_path):
    files.sort()   
    for file in files:
        for (clas2,file_2) in zip(classname_lists, filename_lists): 
            if file_2 == file[:-4] :
                temp = len(file)
                path = os.path.join(root, file[:temp-6]+file[-6:])
                spl_path = os.path.join(split_path,clas2,file)                    
                shutil.move(path, spl_path)

print('2d split done')


#! Class split 8:1:1
train_a = os.path.join(os.getcwd(), 'nia_split_class/train/건축')
train_b = os.path.join(os.getcwd(), 'nia_split_class/train/공예')
train_c = os.path.join(os.getcwd(), 'nia_split_class/train/서예')
train_d = os.path.join(os.getcwd(), 'nia_split_class/train/악기')
train_e = os.path.join(os.getcwd(), 'nia_split_class/train/조각')
train_f = os.path.join(os.getcwd(), 'nia_split_class/train/회화')

test_a = os.path.join(os.getcwd(), 'nia_split_class/test/건축')
test_b = os.path.join(os.getcwd(), 'nia_split_class/test/공예')
test_c = os.path.join(os.getcwd(), 'nia_split_class/test/서예')
test_d = os.path.join(os.getcwd(), 'nia_split_class/test/악기')
test_e = os.path.join(os.getcwd(), 'nia_split_class/test/조각')
test_f = os.path.join(os.getcwd(), 'nia_split_class/test/회화')

val_a = os.path.join(os.getcwd(), 'nia_split_class/val/건축')
val_b = os.path.join(os.getcwd(), 'nia_split_class/val/공예')
val_c = os.path.join(os.getcwd(), 'nia_split_class/val/서예')
val_d = os.path.join(os.getcwd(), 'nia_split_class/val/악기')
val_e = os.path.join(os.getcwd(), 'nia_split_class/val/조각')
val_f = os.path.join(os.getcwd(), 'nia_split_class/val/회화')

path_list = [train_a, train_b, train_c, train_d, train_e, train_f, 
             test_a, test_b, test_c, test_d, test_e, test_f, 
             val_a, val_b, val_c, val_d, val_e, val_f]


for path_af in path_list:
    os.makedirs(path_af, exist_ok=True)
    
print('2_Folder done')


for root, dirs, files in os.walk(clas_a):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        a_spl_path = os.path.join(clas_a, file)
        a_new_pa = os.path.join(train_a, file)
        shutil.move(a_spl_path, a_new_pa)
    
    for file in files[mid:-last]:
        a_spl_path = os.path.join(clas_a, file)
        a_new_pa2 = os.path.join(test_a, file)
        shutil.move(a_spl_path, a_new_pa2)
        
    for file in files[-last:]:
        a_spl_path3 = os.path.join(clas_a, file)
        a_new_pa3 = os.path.join(val_a, file)
        shutil.move(a_spl_path3, a_new_pa3)


    
for root, dirs, files in os.walk(clas_b):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        b_spl_path = os.path.join(clas_b, file)
        b_new_pa = os.path.join(train_b, file)
        shutil.move(b_spl_path, b_new_pa)
    
    for file in files[mid:-last]:
        b_spl_path2 = os.path.join(clas_b, file)
        b_new_pa2 = os.path.join(test_b, file)
        shutil.move(b_spl_path2, b_new_pa2)
        
    for file in files[-last:]:
        b_spl_path3 = os.path.join(clas_b, file)
        b_new_pa3 = os.path.join(val_b, file)
        shutil.move(b_spl_path3, b_new_pa3)

        

for root, dirs, files in os.walk(clas_c):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        c_spl_path = os.path.join(clas_c, file)
        c_new_pa = os.path.join(train_c, file)
        shutil.move(c_spl_path, c_new_pa)
    
    for file in files[mid:-last]:
        c_spl_path2 = os.path.join(clas_c, file)
        c_new_pa2 = os.path.join(test_c, file)
        shutil.move(c_spl_path2, c_new_pa2)
        
    for file in files[-last:]:
        c_spl_path3 = os.path.join(clas_c, file)
        c_new_pa3 = os.path.join(val_c, file)
        shutil.move(c_spl_path3, c_new_pa3)
        
        
for root, dirs, files in os.walk(clas_d):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        d_spl_path = os.path.join(clas_d, file)
        d_new_pa = os.path.join(train_d, file)
        shutil.move(d_spl_path, d_new_pa)
    
    for file in files[mid:-last]:
        d_spl_path2 = os.path.join(clas_d, file)
        d_new_pa2 = os.path.join(test_d, file)
        shutil.move(d_spl_path2, d_new_pa2)
        
    for file in files[-last:]:
        d_spl_path3 = os.path.join(clas_d, file)
        d_new_pa3 = os.path.join(val_d, file)
        shutil.move(d_spl_path3, d_new_pa3)
        
        
for root, dirs, files in os.walk(clas_e):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        e_spl_path = os.path.join(clas_e, file)
        e_new_pa = os.path.join(train_e, file)
        shutil.move(e_spl_path, e_new_pa)
    
    for file in files[mid:-last]:
        e_spl_path2 = os.path.join(clas_e, file)
        e_new_pa2 = os.path.join(test_e, file)
        shutil.move(e_spl_path2, e_new_pa2)
        
    for file in files[-last:]:
        e_spl_path3 = os.path.join(clas_e, file)
        e_new_pa3 = os.path.join(val_e, file)
        shutil.move(e_spl_path3, e_new_pa3)
        
        
for root, dirs, files in os.walk(clas_f):
    files.sort()
    
    mid = int(len(files)*0.8)
    last = int(len(files)*0.1)
    
    for file in files[:mid]:
        f_spl_path = os.path.join(clas_f, file)
        f_new_pa = os.path.join(train_f, file)
        shutil.move(f_spl_path, f_new_pa)
    
    for file in files[mid:-last]:
        f_spl_path2 = os.path.join(clas_f, file)
        f_new_pa2 = os.path.join(test_f, file)
        shutil.move(f_spl_path2, f_new_pa2)
        
    for file in files[-last:]:
        f_spl_path3 = os.path.join(clas_f, file)
        f_new_pa3 = os.path.join(val_f, file)
        shutil.move(f_spl_path3, f_new_pa3)

print('Class split done')
print('All done')