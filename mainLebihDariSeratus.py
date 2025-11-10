from playwright.sync_api import sync_playwright

ID_DUMMY = "8325101400002"
NAMA_WORKORDER = "Project Modem Robustel 2025"

class App:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(user_data_dir="./../ICRMAUTO", headless=False, channel="chrome")
        self.page = self.browser.new_page()

        self.page.route("*/**", self.handle_request_intercept)
        self.page.goto("https://icrmplus.iconpln.co.id/icrm/permohonan/corporate/disposition-to-partner", wait_until='networkidle')

        self.input_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[1]/div/div/div/div[2]/input")
        self.button_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[2]/button[1]")

        self.page.get_by_role('button', name="Nama Perusahaan", exact=True).click()
        self.page.get_by_role('menuitem', name="ID Permohonan", exact=True).click()

        self.data = None
        self.data_action = []
        self.id_permohonan = None
        self.id_permohonan_produk = None
        self.on_input = False

    def handle_request_intercept(self, route, request):
        if self.on_input and request.url == "https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/korporat/disposisi/lihat":
            print(self.id_permohonan)
            print(self.id_permohonan_produk)
            payload = {"listBulk":[{"idMitra":"ZZZZ","idPermohonan":self.id_permohonan,"idPermohonanProduk":self.id_permohonan_produk,"teriminating":"0","statusOriginating":"0"}],"listAsset":"","namaWorkOrder":"Project Modem Robustel 2025","tanggalMulaiAktivasi":"2025-11-10","tanggalSelesaiAktivasi":"2025-11-30","estimasiTanggalAmbil":"2025-11-10 09:00"}
            route.continue_(post_data=payload, url="https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/disposisi/bulk/simpan/v3")
        elif request.url == "https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/korporat/disposisi/detail/lihat":
            print(self.id_permohonan)
            print(self.id_permohonan_produk)
            payload = {"idPermohonan":"8325101400002","limit":500,"pageIn":1}
            route.continue_(post_data=payload)
        else:
            route.continue_()


    def step(self):
        self.input_search.clear()
        self.input_search.fill(ID_DUMMY)
        self.button_search.click()

        with self.page.expect_response("https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/korporat/disposisi/detail/lihat") as response_info:
            self.page.get_by_role('gridcell', name=ID_DUMMY, exact=True).click()
        
        self.data = response_info.value.json()['data']['data']

        for i in self.data:
            row = i
            if row['disposisiStatus'] == '0':
                self.data_action.append(row['idPermohonanProduk'])

        self.on_input = True
        self.page.get_by_role('button', name="Back", exact=True).click()

        for idPermohonanProduk in self.data_action:
            self.id_permohonan = ID_DUMMY
            self.id_permohonan_produk = idPermohonanProduk


            with self.page.expect_response("https://rcrm.iconpln.co.id/icrm-be-backoffice-production/permohonan/disposisi/bulk/simpan/v3") as response_info_2:
                self.button_search.click()

            print(response_info_2.value.json())
            print("response lewat")
            
            # self.page.get_by_role('textbox', name="Pilih Mitra", exact=True).click()
            # self.page.get_by_role('option', name='PT PLN ICON PLUS ').click()
            # self.page.get_by_role('textbox', name="Ketikan Nama Work Order", exact=True).fill(NAMA_WORKORDER)

            # self.page.get_by_role('button', name="Tanggal Mulai", exact=True).click()
            # self.page.get_by_role('cell', name='10', exact=True).click()

            # self.page.get_by_role('button', name="Tanggal Selesai", exact=True).click()
            # self.page.get_by_role('cell', name='30', exact=True).click()
            
            # self.page.get_by_role('button', name="Tgl Estimasi Pick Up Material", exact=True).click()
            # self.page.get_by_role('cell', name='10', exact=True).click()
            # self.page.wait_for_timeout(60000)
            


    def run(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    app = App()
    app.step()