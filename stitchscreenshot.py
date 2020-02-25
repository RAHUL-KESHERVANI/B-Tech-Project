import datetime
import math
from pyvirtualdisplay import Display
import os
import tempfile
# third-party imports
from PIL import Image
from selenium import webdriver
import random
import string



def get_chrome_drive(driver_path=None):
    base_dir = os.path.dirname( os.path.abspath(__file__) )
    log_path = os.path.join( base_dir, 'chromedriver.log' )

    if driver_path is None:
        driver_path = os.path.join( base_dir, 'bin', 'chromedriver' )
        pass

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--hide-scrollbars')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=options,
        service_args=[
            '--log-path={}'.format(log_path)
        ]
    )

    return driver

def get_firefox_drive(driver_path=None):
    base_dir = os.path.dirname( os.path.abspath(__file__) )
    log_path = os.path.join( base_dir, 'geckodriver.log' )

    if driver_path is None:
        driver_path = os.path.join( base_dir, 'bin', 'geckodriver' )
        pass

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    driver = webdriver.Firefox(
        executable_path=driver_path,
        firefox_options=options
    )

    return driver


def crop(img, output_path):
    im = Image.open(r"/home/rahul/BtechProj/adsf.png")

    # Size of the image in pixels (size of orginal image)
    # (This is not mandatory)
    width, height = im.size
    print(width)
    print(height)
    # Setting the points for cropped image
    left = 5
    top = height / 4
    right = 164
    bottom = 3 * height / 4

    # Cropped image of above dimension
    # (It will not change orginal image)
    im1 = im.crop((left, top, right, bottom))

    # Shows the image in image viewer
    im1.save('ifhaui.png')
def save_fullpage_screenshot(driver, url, output_path, tmp_prefix='selenium_screenshot', tmp_suffix='.png'):
    """
    Creates a full page screenshot using a selenium driver by scrolling and taking multiple screenshots,
    and stitching them into a single image.
    """

    # get the page
    driver.get(url)

    # get dimensions
    window_height = driver.execute_script('return window.innerHeight')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    num = int( math.ceil( float(scroll_height) / float(window_height) ) )

    # get temp files
    tempfiles = []
    for i in range( num ):
        fd,path = tempfile.mkstemp(prefix='{0}-{1:02}-'.format(tmp_prefix, i+1), suffix=tmp_suffix)
        os.close(fd)
        tempfiles.append(path)
        pass
    tempfiles_len = len(tempfiles)

    try:
        # take screenshots
        for i,path in enumerate(tempfiles):
            if i > 0:
                driver.execute_script( 'window.scrollBy(%d,%d)' % (0, window_height) )

            driver.save_screenshot(path)
            pass

        # stitch images together
        stiched = None
        for i,path in enumerate(tempfiles):
            img = Image.open(path)

            w, h = img.size
            y = i * window_height

            if i == ( tempfiles_len - 1 ) and num > 1:
                img = img.crop((
                    0,
                    h-(scroll_height % h),
                    w,
                    h
                ))

                w, h = img.size
                pass

            if stiched is None:
                stiched = Image.new('RGB', (w, scroll_height))

            stiched.paste(img, (
                0, # x0
                y, # y0
                w, # x1
                y + h # y1
            ))
            pass
        crop(stiched, output_path)
        stiched.save(output_path)
    finally:
        # cleanup
        for path in tempfiles:
            if os.path.isfile(path):
                os.remove(path)
        pass

    return output_path

def generate(width, height):
    f = open('/home/rahul/AwesomeProject/App.js', 'w+')
    # c = open('/home/rahul/AwesomeProject/App.js', 'r')
    f.write("import React from 'react';\nimport { Text, View, TextInput, TouchableOpacity, StyleSheet} from 'react-native';\nimport {CheckBox} from 'native-base';\nexport default function App() {\n\treturn (")
    # l = c.readline()
    f.write("\n\t\t<View style={styles.container}>")
    # for y in range(10):
    f.write("\n\t\t\t<View style={styles.item}>")
    for i in range(10):
        digits = "".join( [random.choice(string.digits) for i in xrange(8)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(15)] )
        f.write("\n\t\t\t\t<Text style= {{marginTop:15}}>"+digits+chars+"</Text>")
    f.write("\n\t\t\t</View>")
    f.write("\n</View>\n)}\nconst styles = StyleSheet.create({\n\tcontainer: {\n\tflex: 1,\n\tflexDirection: 'row',\n\tflexWrap: 'wrap',\n\talignItems: 'flex-start'\n\t},\n\titem: {\n\twidth: '6.67%'\n\t}\n})")


def main(url):
    for x in range(10):
        #generate random width height for each component
        #width, height = random
        generate(width, height)
        now = datetime.datetime.now()

        filename = 'screenshot-{}-{}.png'.format(
            now.strftime('%Y%m%d'),
            now.strftime('%H%M%S')
        )

        # driver = get_chrome_drive() if True else get_firefox_drive()
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome()
        driver.set_window_size(1280,800)

        # url = 'https://ahfarmer.github.io/calculator/'

        save_fullpage_screenshot(
            driver,
            url,
            filename
        )
        crop(filename, widht, height)
        driver.quit()

    # print( filename )

    return


if __name__ == '__main__':
    f = open('webpages.txt', 'r+')
    content = f.read()
    content = list(filter(None, content.split("\n")))
    for c in content:
        main(c)
    # generate()
