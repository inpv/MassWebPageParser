import os  # listing directories etc.
import time  # waiting for the pages to be loaded
import unittest  # to organize testing process
import wget  # to download web hosted images
from selenium import webdriver  # web parser itself
from selenium.common.exceptions import NoSuchElementException  # custom exc, empty search workaround
from pathlib import Path  # to create files
from MassWebPageParser.file_util import FileUtil
from MassWebPageParser.text_util import TextUtil


class Parser(unittest.TestCase):

    # CLASS VARIABLES

    product_link_xpath = ''
    product_image_xpath = ''
    product_image_selector = ''

    urls_array = []
    product_links_list = []

    # ADDITIONAL METHODS

    @staticmethod
    def insert_urls():
        # reads multiple lines with URLs to later parse from

        print()
        print("Now enter the URLs of all directories you want to parse:")
        print("Separate them by spaces, they will be auto-removed eventually.")
        print("When you're done, press Enter on a blank line one more time to exit the adding cycle.")

        while True:
            line = input()
            if len(line) > 0:
                if line[-1] == " ":
                    line = line[:-1]
                    Parser.urls_array.append(line)
            else:
                break

        return Parser.urls_array

    @staticmethod
    def insert_products_xpath():
        print("Now enter the XPath of a group of links which point to product cards:")
        print("Hint: first find the XPath of two list elements, if only one tag param changes,")
        print("remove the param, but leave the tag.")

        Parser.product_link_xpath = input()

        return Parser.product_link_xpath

    @staticmethod
    def insert_images_xpath():
        print()
        print("Now enter the XPath of a group of links which point to product images:")
        print("Hint: first find the XPath of two list elements, if only one tag param changes,")
        print("remove the param, but leave the tag.")

        Parser.product_image_xpath = input()

        return Parser.product_image_xpath

    @staticmethod
    def insert_images_css_selector():
        print()
        print("In case the image can't be found by XPath, please enter a backup CSS selector:")

        Parser.product_image_selector = input()

        return Parser.product_image_selector

    @staticmethod
    def create_products_list(links):

        for link in links:
            link_href = link.get_attribute('href')  # getting the link to the product itself
            Parser.product_links_list.append(link_href)  # filling the list with links

        return Parser.product_links_list

    # IMAGES DOWNLOAD

    @staticmethod
    def download_and_check_pics_creation(local_img_url, local_img_name):
        wget.download(local_img_url,
                      FileUtil.pics_local_dir + local_img_name + ".png")  # download the pic

        full_pic_name = FileUtil.pics_local_dir + local_img_name + ".png"

        if os.path.isfile(full_pic_name):  # check if the image has been created
            print('The image named ' + local_img_name + ' is successfully downloaded.')
        else:
            print('Some problems with image creation occurred, please check.')

    # CREATING AND WRITING TO FILES

    @staticmethod
    def create_new_html_file(local_img_name):

        # creating a new html file for the desc

        new_desc_name = FileUtil.descs_local_dir + local_img_name + '.html'
        Path(new_desc_name).touch()

        if os.path.isfile(new_desc_name):  # check if the file has been created
            print('The file named ' + local_img_name + ' is successfully created.')
        else:
            print('Some problems with empty html file creation occurred, please check.')

        return new_desc_name

    @staticmethod
    def write_descs_to_new_html_file(new_desc_name, local_img_name, pretty_text):

        # writing the descs to a new html file

        html_file = open(new_desc_name, 'wb')  # opening the created file in write mode
        html_file.write(pretty_text)
        html_file.close()

        html_file = open(new_desc_name,
                         'rb')  # opening again in read mode, to determine if a file has been created

        if os.stat(new_desc_name).st_size != 0:  # check if the info has been written to file
            print('The info to the file ' + local_img_name + ' has been written successfully.')
        else:
            print('Something went wrong with the file ' + local_img_name + ', please check.')

        html_file.close()
        print()

    # MAIN PARSER CODE

    def setUp(self):
        self.driver = webdriver.Firefox()

    def parse_catalog(self):
        driver = self.driver

        print()
        print("Starting up Selenium driver...")

        # MAIN METHOD

        for url in Parser.urls_array:  # looping through all previously stated URLs

            driver.get(url)
            url_title = driver.find_element_by_tag_name("title").text  # sets the page title as the browser heading
            self.assertIn(url_title, driver.title)
            time.sleep(2)

            links = driver.find_elements_by_xpath(str(Parser.product_link_xpath))
            # finds all the elements according to Xpath

            Parser.product_links_list = Parser.create_products_list(links)  # get the eventual links list

            for product_link in Parser.product_links_list:
                driver.get(product_link)  # get the page
                time.sleep(2)  # wait until loaded

                # IMAGES DOWNLOAD

                img_name = driver.find_element_by_tag_name(FileUtil.img_name_search_tag).text

                try:
                    img_url = \
                        driver.find_element_by_xpath(
                            Parser.product_image_xpath).get_attribute(
                            'src')  # link to pic
                    if img_url:
                        Parser.download_and_check_pics_creation(img_url, img_name)

                except NoSuchElementException as exception:
                    # find pic element by CSS selector if not found by XPath

                    img_url = driver.find_element_by_css_selector(Parser.product_image_selector).get_attribute(
                        'src')  # link to pic
                    if img_url:
                        Parser.download_and_check_pics_creation(img_url, img_name)

                # CREATING DESCRIPTIONS

                raw_desc = TextUtil.create_raw_descs(product_link)
                final_desc = TextUtil.add_attrs(raw_desc)

                # CREATING AN EMPTY HTML FILE AND WRITING TO IT

                local_desc_name = Parser.create_new_html_file(img_name)
                Parser.write_descs_to_new_html_file(local_desc_name, img_name, final_desc)

                driver.execute_script("window.history.go(-1)")  # going back
                time.sleep(2)  # wait until the page loads

            Parser.product_links_list.clear()  # prevent from adding elements from previous cycle

    def tearDown(self):  # closing parser
        self.driver.close()
