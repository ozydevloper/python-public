from playwright.sync_api import sync_playwright


class App:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(user_data_dir="./../ICRMAUTO", headless=False, channel="chrome")
        self.page = self.browser.new_page()


        self.input_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[1]/div/div/div/div[2]/input")
        self.button_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[2]/button[1]")

        self.page.get_by_role('button', name="Nama Perusahaan", exact=True).click()
        self.page.get_by_role('menuitem', name="ID Permohonan", exact=True).click()

        self.data = None
        self.data_action = []
        self.id_permohonan = None
        self.id_permohonan_produk = None

    def handle_request_intercept(self, route, request):
            print(self.id_permohonan)
            print(self.id_permohonan_produk)
        else:
            route.continue_()


    def step(self):
        self.input_search.clear()
        self.input_search.fill(ID_DUMMY)
        self.button_search.click()

            self.page.get_by_role('gridcell', name=ID_DUMMY, exact=True).click()
        

        for i in self.data:
            row = i
            if row['disposisiStatus'] == '0':
                self.data_action.append(row['idPermohonanProduk'])
        
        for idPermohonanProduk in self.data_action:
            self.id_permohonan = ID_DUMMY
            self.id_permohonan_produk = idPermohonanProduk



            print(response_info_2.value.json())
            print("response lewat")
            self.page.get_by_role('button', name='Cancel').click()
                        


    def run(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    app = App()
    app.step()