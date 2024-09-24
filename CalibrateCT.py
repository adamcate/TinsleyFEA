import pydicom as dicom
import matplotlib.pyplot as plt
import os
# from ipywidgets import interact, interactive, fixed, interact_manual
# import ipywidgets as widgets
import numpy as np

# import the yaml libraries for configuration files
import yaml

with open('config.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

rootDir = data.get('root_path')

models = data["models"]

patient = models[0].get("data").get("name") # get the patient's name

parentDirectory = rootDir + patient + "/DICOMImages/CT/"
saveDirectory = rootDir + patient + "/FEA/"

identifier = "IM_"

# path = "C:/Users/jake/OneDrive/Documents/Jake/Academia/Graduate School/Research/T1D/ROI Data/2001_R/S88340/S70"
path = parentDirectory
dir_list = os.listdir(path)
dir_list = [i for i in dir_list if identifier in i]

# read the slice dimensions from the first DICOM image in the list
ds = dicom.dcmread(path + "/" + dir_list[0])
x = ds.Columns
y = ds.Rows

z = len(dir_list)
data = np.zeros((z, x, y))

for i in range(len(dir_list)):
    image_path = path + "/" + dir_list[i]
    ds = dicom.dcmread(image_path)
    j = ds.InstanceNumber - 1
    data[j,:,:] = ds.pixel_array

data = np.flip(data, axis=0)
# data = np.flip(data, axis=1)
# data = np.flip(data, axis=2)

"""
def plot_func(j, a, b, L):
    l = int(L/2)
    plt.figure(figsize = (10, 10))
    plt.imshow(data[j,:,:], cmap = "bone")
    plt.axhline(a+0.5)
    plt.axvline(b+0.5)
    rectangle = plt.Rectangle((b-l, a-l), L, L)
    plt.gca().add_patch(rectangle)
    print(np.median(data[j,a-l:a+l,b-l:b+l]))

interact(plot_func, 
         j = widgets.IntSlider(value = 100, min = 0, max = z-1, step = 1),
         a = widgets.IntSlider(value = 260, min = 1, max = x, step = 1),
         b = widgets.IntSlider(value = 139, min = 1, max = y, step = 1),
         L = widgets.IntSlider(value = 30, min = 1, max = 100, step = 1))

"""
air = -985
fat = -138
muscle = 49

pname = parentDirectory + patient + "_AFM_p.raw"
Ename = parentDirectory + patient + "_AFM_E.raw"

# for linear fit w/o bone
vals = [air, fat, muscle]
ref_vals = [-807, -85, 31]
fit = np.polyfit(vals, ref_vals, deg = 1)
p = np.poly1d(fit)
BMD = p(data)
p = 0.0012*BMD + 0.17
p[p <= 0.0] = 0

E = (6850*(np.power(p, 1.49)))*1.28
E[E <= 0.0] = 1
E[E > 8768] = 17000

p = p*10000
p.astype(np.ushort).tofile(pname)
E.astype(np.ushort).tofile(Ename)