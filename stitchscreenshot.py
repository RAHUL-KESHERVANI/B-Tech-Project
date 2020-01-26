import datetime
import math
from pyvirtualdisplay import Display
import os
import tempfile
# third-party imports
from PIL import Image
from selenium import webdriver
 
 
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
        stiched.save(output_path)
    finally:
        # cleanup
        for path in tempfiles:
            if os.path.isfile(path):
                os.remove(path)
        pass
 
    return output_path
 
 
def main():
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
 
    url = 'https://www.facebook.com/'
 
    save_fullpage_screenshot(
        driver,
        url,
        filename
    )
 
    driver.quit()
 
    print( filename )
 
    return
 
 
if __name__ == '__main__':
    main()