#!/usr/bin/env python
# coding: utf-8

# In[265]:


import rasterio as rio
import numpy as np


# In[266]:


R10 = '/Users/shivashis.ext/felicette-data/LC81390462020136'
b4 = rio.open(R10+'/LC81390462020136-b4.tiff')
b3 = rio.open(R10+'/LC81390462020136-b3.tiff')
b2 = rio.open(R10+'/LC81390462020136-b2.tiff')


# In[267]:


out_tiff = R10 + '/stack_prog.tiff'
with rio.open(out_tiff,'w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0], photometric="RGB") as rgb:
    rgb.write(b4.read(1),1) 
    rgb.write(b3.read(1),2) 
    rgb.write(b2.read(1),3) 
    rgb.close()


# In[268]:


r = b4.read(1)
g = b3.read(1)
b = b2.read(1)
norm_r = np.linalg.norm(r)
norm_g = np.linalg.norm(g)
norm_b = np.linalg.norm(b)
r = r / norm_r
g = g / norm_g
b = b / norm_b


# In[ ]:





# In[269]:


img = np.array([r,g,b])


# In[270]:


# img


# In[271]:


from rio_color import operations


# In[272]:


# ops = "gamma g 1.7 gamma r 1.4 sigmoidal rgb 10 0.4"
# ops = "sigmoidal 123 20 0.2"

# assert img.shape[0] == 3
# assert img.min() >= 0
# assert img.max() <= 1

# for func in operations.parse_operations(ops):
#     img = func(img)


# In[273]:


# img = img * 255


# In[ ]:





# In[274]:


from matplotlib import pyplot as plt
norm_r = img[0]*norm_r
r = norm_r * (255/np.amax(norm_r))
r = r.astype(np.uint8)
norm_g = img[1]* norm_g
g = norm_g * (255/np.amax(norm_g))
g = g.astype(np.uint8)
norm_b = img[2]* norm_b
b = norm_b * (255/np.amax(norm_b))
b = b.astype(np.uint8)


# In[281]:


rbg_v = np.stack([r,g,b], axis=-1).astype(np.uint8)
out_tiff = R10 + '/stack_prog_color.tiff'
with rio.open(out_tiff,'w',driver='Gtiff', width=b4.width, height=b4.height, 
              count=3,crs=b4.crs,transform=b4.transform, dtype=np.uint8, photometric="RGB") as rgb:
    rgb.write(r.astype(np.uint8),1) 
    rgb.write(g.astype(np.uint8),2) 
    rgb.write(b.astype(np.uint8),3) 
    rgb.close()
plt.imshow(rbg_v)
plt.show()


# In[276]:



# with rio.open(out_tiff,'w',driver='Gtiff', width=b4.width, height=b4.height, 
#               count=3,crs=b4.crs,transform=b4.transform, dtype=np.uint16) as rgb:
#     rgb.write(norm_b.astype(np.uint16),1) 
#     rgb.write(norm_g.astype(np.uint16),2) 
#     rgb.write(norm_r.astype(np.uint16),3) 
#     rgb.close()


# In[277]:


array = np.zeros([5, 4, 3], dtype=np.uint8)


# In[278]:


np.amax(norm_r)


# In[279]:


r


# In[ ]:





# In[ ]:






