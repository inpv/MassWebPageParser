from MassWebPageParser.parser import Parser
from MassWebPageParser.file_util import FileUtil


class Launcher:

    # contains general process and components

    @staticmethod
    def start_launcher():

        print()
        print("Welcome to the Mass WebPage Parser utility.")
        print("It uses selenium and Gecko webdriver to download descriptions and images from a website,")
        print("and then creates and/or fills an excel file with their data.")
        print()

        # creates class instances for a specific parser usage

        file_util_instance = FileUtil()
        parser_instance = Parser()

        # SET THE DIRECTORIES AND FILES
        file_util_instance.insert_dirs()
        file_util_instance.get_excel_file()

        # FIRE UP SELENIUM DRIVER
        parser_instance.insert_urls()
        parser_instance.insert_products_xpath()
        parser_instance.insert_images_xpath()
        parser_instance.insert_images_css_selector()
        file_util_instance.insert_search_params()

        parser_instance.setUp()
        parser_instance.parse_catalog()
        parser_instance.tearDown()

        # SENDING THE PICS AND DESCS TO AN EXCEL FILE
        file_util_instance.send_descs_to_excel()
        file_util_instance.send_pics_links_to_excel()
