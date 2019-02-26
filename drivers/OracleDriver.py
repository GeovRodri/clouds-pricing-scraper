from commons.BaseDriver import BaseDriver


class OracleDriver(BaseDriver):

    def __init__(self):
        self.url = "https://cloud.oracle.com/iaas/pricing"
        super().__init__()

    def get_price(self):
        titles, data = [], {}

        text_element = self.driver.find_element_by_xpath("//h4[contains(text(), 'Bare Metal Instances')]/parent::div"
                                                         "/parent::div/parent::div/parent::div/parent::div")

        data["default"] = []
        trs = text_element.find_elements_by_tag_name("tr")

        is_title = True
        for tr in trs:
            columns, index = {}, 0
            tds = tr.find_elements_by_tag_name("td")

            for td in tds:
                if is_title is True:
                    titles.append(td.text)
                else:
                    text_th = titles[index]
                    columns[text_th] = td.text
                    index += 1

            if is_title is True:
                is_title = False
            else:
                data["default"].append(columns)

        self.save_json('oracle', data)
