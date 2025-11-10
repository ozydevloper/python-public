from playwright.sync_api import sync_playwright

ID_DUMMY = "8325101400002"


class App:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(user_data_dir="./../ICRMAUTO", headless=False, channel="chrome")
        self.page = self.browser.new_page()
        self.page.goto("https://icrmplus.iconpln.co.id/icrm/permohonan/corporate/disposition-to-partner", wait_until='networkidle')

        self.input_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[1]/div/div/div/div[2]/input")
        self.button_search = self.page.locator("//html/body/div/div[1]/div[1]/div/main/div/div[2]/div[3]/div/form/div/div/div[2]/button[1]")

        self.page.get_by_role('button', name="Nama Perusahaan", exact=True).click()
        self.page.get_by_role('menuitem', name="ID Permohonan", exact=True).click()

    def step(self):
        self.input_search.clear()
        self.input_search.fill(ID_DUMMY)
        self.button_search.click()
        self.page.wait_for_timeout(60000)


    def run(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    app = App()
    app.step()