import requests  # to load web pages into an object
from bs4 import BeautifulSoup  # creating and filtering descriptions


class TextUtil:

    @staticmethod
    def create_raw_descs(link_inside):

        def _remove_all_attrs(text):  # removing tag attributes
            for tag in text.find_all(True):
                tag.attrs = {}
            return text

        # FORMING THE DESCRIPTIONS

        page = requests.get(link_inside)  # getting the object from url
        soup = BeautifulSoup(page.content, 'html.parser')  # loading it into the soup
        desc_divs = []  # a list for all descs' divs

        # the code below is a sample, do NOT paste it in your project as is
        """
        main_heading = soup.find("h1")
        main_heading.name = "div"  # change the name for uniformity
        if main_heading:
            desc_divs.append(main_heading)
        else:
            pass

        main_desc = soup.find("div", class_="product-main-text")  # main desc
        if main_desc:
            desc_divs.append(main_desc)
        else:
            pass

        features_table_desc = soup.find("div", class_="title")  # features (table heading)
        if features_table_desc:
            desc_divs.append(features_table_desc)
        else:
            pass

        features_table = soup.find("table", class_="table-striped")  # features table
        if features_table:
            desc_divs.append(features_table)
        else:
            pass

        catalog_detail_block = soup.find("div", class_="catalog_detail_info")  # text after features table
        if catalog_detail_block:
            desc_divs.append(catalog_detail_block)
        else:
            pass
        """

        soup.clear()  # clearing the old soup

        for desc_div in desc_divs:  # loading the new soup with objects from the list
            soup.append(desc_div)

        soup_without_attrs = _remove_all_attrs(soup)  # removing all unnecessary attrs

        return soup_without_attrs

    @staticmethod
    def add_attrs(soup):

        # ADDING NEEDED ATTRIBUTES

        def create_new_breakline_tag():
            breakline_tag = soup.new_tag('br')
            return breakline_tag

        def create_new_bold_tag():
            bold_tag = soup.new_tag('b')
            return bold_tag

        # the code below is a sample, do NOT paste it in your project as is
        """
        # elements with unique properties
        
        features_table = soup.find("table")
        features_table.attrs["border"] = "1"
        features_table.attrs["cellpadding"] = "5"
        features_table.insert_after(create_new_breakline_tag())

        main_product_heading = soup.find("div")
        main_product_heading.string.wrap(create_new_bold_tag())
        main_product_heading.insert_after(create_new_breakline_tag())

        # elements with the same properties

        help_headings = soup.find_all("div", string=re.compile("Our mission"))
        quality_heading = soup.find("div", string="Quality")
        specs_heading = soup.find("div", string="FEATURES")

        bold_br_headings = []  # a list for elements with the same properties

        if help_headings:  # adding elements to list, but only if they have been found
            bold_br_headings.extend(help_headings)
        else:
            pass

        if quality_heading:
            bold_br_headings.append(quality_heading)
        else:
            pass

        if specs_heading:
            bold_br_headings.append(specs_heading)
        else:
            pass

        for heading in bold_br_headings:
            heading.insert_before(create_new_breakline_tag())
            heading.insert_after(create_new_breakline_tag())
            heading.string.wrap(create_new_bold_tag())
        """

        pretty_text = soup.prettify().encode('utf-8')  # final pretty version

        return pretty_text
