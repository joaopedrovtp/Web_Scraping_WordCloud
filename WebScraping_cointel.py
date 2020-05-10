## Make a WorldCloud of 10 recent articles content from Coin Telegraph site.

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
from itertools import chain
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator

# First collect the html content from the homepage website cointelegraph.com
url = "https://cointelegraph.com"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

# Collecting all the posts links from main page
links = [i['href'] for i in soup.find_all(class_="post-card__figure-link", href=True)]

# Let's catch the content from the recent ten posts
content = []
for post in links[0:10]:
  
    url = "https://cointelegraph.com" + post
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    content.append([i.text for i in soup.find_all(class_='post-content')])

# Join all lists of content into one text
flat_content =  list(chain.from_iterable(content)) # Flatten list of lists
text = ' '.join(map(str, flat_content)) # join the list to string

# Cleaning text - removing punctuation, digits and to lowercase text
text2 = text.translate(str.maketrans('', '', string.punctuation)).lower() #Punctuation / lower
clean_text = ''.join([i for i in text2 if not i.isdigit()])  #digits

# Word tokenization using NLTK - Natural Language processing
tokenizer = RegexpTokenizer('\s+', gaps = True)
words = tokenizer.tokenize(clean_text)

# Removing stopwords and extra whitespaces
english_stops = set(stopwords.words('english'))
clean_words = [word.strip() for word in words if word not in english_stops]

# Rejoin word to make the wordcloud 
final_text = ' '.join([w for w in clean_words])

## Wordcloud 
# Creates a mask (bitcoin format image)
bitcoin_mask = np.array(Image.open("bitcoin.png"))

# Transform array values 0 to 255 (255 are pure white, needed that to get the shape of the coin) 
bitcoin_mask[bitcoin_mask == 0] = 255

# Build and plot wordcloud
wordcloud = WordCloud(max_words=500, background_color="white", mask = bitcoin_mask).generate(final_text)
image_colors = ImageColorGenerator(bitcoin_mask)
plt.figure(figsize=[7,7])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.show()

# Saving wordcloud image
wordcloud.to_file("bitcoin_wordcloud.png")


