from playwright.sync_api import sync_playwright
from minio import Minio


def main():
    conn_dict = {"endpoint": "****", "access_key": "****",
                 "secret_key": "****", "region": "****"}

    bucket_name = "****"
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page(accept_downloads=True)
        page.goto("https://rpwdl.ezdrowie.gov.pl/Registry/DownloadRegistries")

        file_type_dict = {'Rpm': 'odmioty_lecznicze',
                          'Rpz': 'praktyki_lekarskie_indywidualne',
                          'Rpzg': 'praktyki_lekarskie_grupowe',
                          'Rpzp': 'praktyki_pielęgniarskie_indywidualne',
                          'Rpzpg': 'praktyki_pielęgniarskie_grupowe',
                          'Rpf': 'praktyki_fizjoterapeutyczne_indywidualne',
                          'Rpfg': 'praktyki_fizjoterapeutyczne_grupowe'}

        for file_type, name in file_type_dict.items():
            page.select_option("select#EntryType", file_type)
            page.select_option("select#FileType", "Csv")
            page.select_option("select#Range", "OnlyActive")

            with page.expect_download() as download_info:
                download_button = page.query_selector("button[class*='btn-success']")
                download_button.click()

            download = download_info.value
            path = download.path()
            print(path)
            file_name = file_type + '_' + name
            download.save_as(path=f"./{file_name}.zip")
            conn = Minio(**conn_dict)
            conn.fput_object(bucket_name=bucket_name, object_name=file_name, content_type="application/octet-stream",
                             file_path=path, metadata=None)

        browser.close()


if __name__ == '__main__':
    main()
