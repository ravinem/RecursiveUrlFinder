import os.path
import re
import urllib     
from urllib import request
from urllib.error import URLError


# Root path of the project. Files created for HTML pages will be stored here.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))+"/Files"

def PlotLinks(url,curDirectory,parent,count):   
    """
    It is a recursive function.
    It gets the full HTML from URL and extract all links inside that page.
    Then recurse through all extracted URL to and perform above step on each URL.
    Parameters:
        url - URL of web page whose content is to be downloaded and links are to be found.
        curDirectory - Path where URL's content will be saved
        parent - Keeps track of URL's till visited and helps in avoiding self/cycling loops
        count - Incremented with each recursive call and new directories and created with this variable
    """
    try:         
        urls = []
        isError = False
        fullHTML = ''
        # make url filename friendly, file would be saved with this name
        urlAsFilename = re.sub(r'[/\\:*?<>|]','',url)
        try:
            fullHTML = str(urllib.request.urlopen(url).read())
            urls = re.findall(r'href="[\'"]?([^\'" >]+)', fullHTML)
            urls = list(filter(lambda s : s.startswith('http'),urls))
        except URLError:
            isError = True
        if isError:
            return None
        # Recursive function's base case. If there are no links in the HTML then just write HTML to file.
        elif len(urls) == 0:
            if not os.path.exists(curDirectory):
                os.makedirs(curDirectory)
            with open(curDirectory+"\\"+urlAsFilename+".txt", 'w+') as file:
                file.writelines(fullHTML)
            return None
        else:
            if not os.path.exists(curDirectory):
                os.makedirs(curDirectory)
            with open(curDirectory+"\\"+urlAsFilename+".txt", 'w+') as file:
                file.writelines(fullHTML)
            for link in urls:
                linkAsFilename = re.sub(r'[/\\:*?<>|]','',link)
                if linkAsFilename in parent or urlAsFilename == linkAsFilename:  # checking for infinite loop caused by cycling/self links
                    continue
                else:
                    PlotLinks(link,curDirectory+"\\"+str(count+1),parent + urlAsFilename,count+1)  # recurse by incremeting count and concatinating visited URL
    except FileNotFoundError as e:
        print('Windows file path max limit reached :  '+str(e))
    except Exception as genericException:
        print(str(genericException))

def PrintUrlImages(url):
    '''
    From the given URL, distinct absolute images urls from HTML are taken and printed on Standard Console.
    Parameters:
        url : URL of web page from which image urls are to be found.
    '''
        
    UrlDomain = ''      #URL Domain , so that absolute image URL can be formed from relative URL
    if url.startswith('https'):
        UrlDomain = 'https://'+url[8:].split('/')[0]
    else:
        UrlDomain = 'http://'+url[7:].split('/')[0]

    try:
        fullHTML = str(urllib.request.urlopen(url).read())
        urls = list(set(re.findall(r'img [^>]*src="[\'"]?([^\'" >]+)', fullHTML)))  # find all distinct <src> attribute value of <img> tag
        imgCount = 1  # to keep count of urls while printing
        if len(urls)==0:
            print('')
            print('No images are linked with the provided url.')
        for imageUrl in urls:
            print(str(imgCount),end=') ')
            if imageUrl.startswith('http'):    # it is an absolute url, directly print it
                print(imageUrl)                    
            else:                              # it is a relative url
                if imageUrl.startswith('//'):
                    print(imageUrl)
                elif imageUrl.startswith('/'):  
                    print(UrlDomain+imageUrl)
                elif imageUrl.startswith('..'):
                    imageUrl = imageUrl.replace('../','')  
                    print(UrlDomain+'/'+imageUrl)                      
                else:
                    print(UrlDomain+'/'+imageUrl)

            imgCount = imgCount + 1
            print(' ')

    except URLError:
       print('Failed to get content from url : ' + url)    

# program enters in if it is run as stand alone program
if __name__=='__main__':
    url = input('Enter a full valid URL: ')
    print('')
    if re.match('^http://',url) is None or re.match('^https://',url) is None:
        print('Invalid URL')
    else:
        print('Starting 1st part of problem i.e. saving HTML as file for given Url...')
        if os.path.exists(PROJECT_ROOT):
            os.removedirs(PROJECT_ROOT)
        PlotLinks(url,PROJECT_ROOT,'',0)  # First Part of Problem
        print('Finished First part of Problem.')
        print('Check for created files at %s.'%PROJECT_ROOT)
        print('')
        print('****----------------------------------------------****')
        print('')
        print('Starting 2nd part of problem i.e. getting absolute image URLs linked with '+url+' ...')
        PrintUrlImages(url)             # Second part of problem
    
         
        




        
