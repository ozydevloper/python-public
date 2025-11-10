from playwright.sync_api import sync_playwright

ID_DUMMY = "8325101400002"


class App:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(user_data_dir="./../ICRMAUTO", headless=False, channel="chrome")
        self.page = self.browser.new_page()
        self.page.on('response', self.handle_response)
        self.page.goto("https://icrmplus.iconpln.co.id/icrm/permohonan/corporate/disposition-to-partner", wait_until='networkidle')

        self.input_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[1]/div/div/div/div[2]/input")
        self.button_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[2]/button[1]")

        self.page.get_by_role('button', name="Nama Perusahaan", exact=True).click()
        self.page.get_by_role('menuitem', name="ID Permohonan", exact=True).click()

        self.data = None
        self.data_action = []

    def handle_response(self, response):
        if response.url == "https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/korporat/disposisi/detail/lihat":
            self.data = response.json()['data']['data']


    def step(self):
        self.input_search.clear()
        self.input_search.fill(ID_DUMMY)
        self.button_search.click()

        self.page.get_by_role('gridcell', name=ID_DUMMY, exact=True).click()
        while True:
            self.page.wait_for_timeout(100)
            if self.data != None:
                print("Data didapatkan")
                for i in self.data:
                    row = i
                    if row['disposisiStatus'] == '0':
                        self.data_action.append(row['idPermohonanProduk'])
                break
        
        for idPermohonan in self.data_action:
            self.page.get_by_role('gridcell', name=idPermohonan, exact=True).click()
            self.page.wait_for_timeout(60000)


    def run(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    app = App()
    app.step()