#!/usr/bin/env python
# coding: utf-8

# In[47]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import selenium
from webdriver_manager.chrome import ChromeDriverManager


# In[48]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[49]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[50]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem = news_soup.select_one('div.list_text')


# In[51]:


slide_elem.find("div", {class_:="content_title"})


# In[52]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[53]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[61]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[62]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[63]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[64]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[65]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[66]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[67]:


df.to_html()


# In[68]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[69]:


# 1. Use browser to visit the URL 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://marshemispheres.com/'

browser.visit(url)


# In[39]:


browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[41]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[70]:


hemisphere_image_urls 
[{'img_url': 'https://marshemispheres.com/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png',
  'title': 'Cerberus Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png',
  'title': 'Schiaparelli Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png',
  'title': 'Syrtis Major Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png',
  'title': 'Valles Marineris Hemisphere Enhanced'},]


# In[71]:


html = browser.html

hemi_soup = soup(html, 'html.parser')
hemi_items = hemi_soup.find_all('div', class_='item')


# In[72]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in hemi_items:
    
    # Create empty dictionary to store values
    hemispheres = {}
    
    # Find image URL
    main_url = x.find('a', class_='itemLink')['href']
    browser.visit(url + '/' + main_url)
    main_url = browser.html
    image_soup = soup(main_url, 'html.parser')
    hemi_url = url + '/' + image_soup('img', class_='wide-image')[0]['src']

    # Find the titles
    hemi_title = x.find('h3').text

    # Store findings in dictionary
    hemispheres['image_url'] = hemi_url
    hemispheres['title'] = hemi_title

    # Add to list
    hemisphere_image_urls.append(hemispheres)


# In[73]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls
df.to_html()


# In[74]:


# 5. Quit the browser
browser.quit()


# In[ ]:




