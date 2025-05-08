import os
import re
from bs4.element import Tag
from requests import Session
from models import Assets, Materials, Specs, Product
from utils import get_spec_values, convert_kw_to_hp
from urllib.parse import quote


class ProductMapper:

    def __init__(self, product_id: str, product_category: str | None, product_details: Tag, session: Session):
        self.product_id = product_id
        self.details = product_details
        self.session = session
        self.product = Product(product_id, product_category)

    def get_description(self) -> str | None:
        desc_tag = self.details.find("div", class_="product-description")
        return desc_tag.get_text(strip=True) if desc_tag else None

    def get_specs(self) -> Specs:
        voltage = get_spec_values(self.details, ["Voltage @ Frequency", "Armature Voltage", "Field Voltage"], "V")
        rpm = get_spec_values(self.details, ["Speed", "Base Speed"], "rpm")
        frame = get_spec_values(self.details, ["Frame"])
        hp = get_spec_values(self.details, ["Output @ Frequency", "Output Power"], "HP")
        if not hp:
            kw = get_spec_values(self.details, ["Output @ Frequency", "Output Power"], "KW")
            hp = convert_kw_to_hp(kw)

        return Specs(hp, voltage, rpm, frame)

    def get_bom(self) -> list:
        bom = []
        parts_tag = self.details.find("div", attrs={"data-tab": "parts"})
        all_rows = parts_tag.find_all("tr") if parts_tag else None
        if all_rows:
            for part in all_rows[1:]:
                tds = part.find_all("td")
                part_number = tds[0].get_text(strip=True)
                description = re.sub(r"\s+", " ", tds[1].get_text(strip=True))
                quantity = int(tds[2].get_text(strip=True).split(".")[0])
                materials = Materials(part_number, description, quantity)
                bom.append(materials)
        return bom

    def get_assets(self) -> Assets:
        file_path = f"./output/assets/{self.product_id}"
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        manual_tag = self.details.find("a", attrs={"id": "infoPacket"})
        manual_url = f'https://www.baldor.com{manual_tag["href"]}' if manual_tag else None
        if manual_url:
            response = self.session.get(manual_url)
            with open(f"{file_path}/manual.pdf", "wb") as f:
                f.write(response.content)
            manual = f"assets/{self.product_id}/manual.pdf"
        else:
            manual = None

        cad_tag = self.details.find("div", attrs={"id": "drawings"})
        if ".DWG" in str(cad_tag):
            url = str(cad_tag).split(".DWG")[1].split("http")[1]
            url = f"http{url}.DWG".replace("&amp;", "&")
            comp_id = url.split("compId=")[1]
            dwg_url = f"https://www.baldor.com/api/products/download/?value={comp_id}&url={quote(url, safe='')}"
            response = self.session.get(dwg_url)
            with open(f"{file_path}/cad.dwg", "wb") as f:
                f.write(response.content)
            cad = f"assets/{self.product_id}/cad.dwg"
        else:
            cad = None

        image_tag = self.details.find("img", class_="product-image")
        image_src = image_tag["data-src"] if image_tag and image_tag["data-src"] != "/api/images/451" else None
        image_url = f'https://www.baldor.com{image_src}?bc=white&as=1&h=256&w=256' if image_src else None
        if image_url:
            response = self.session.get(image_url)
            with open(f"{file_path}/image.jpg", "wb") as f:
                f.write(response.content)
            image = f"assets/{self.product_id}/image.jpg"
        else:
            image = None

        return Assets(manual, cad, image)

    def get_product(self):
        self.product.description = self.get_description()
        self.product.specs = self.get_specs()
        self.product.bom = self.get_bom()
        self.product.assets = self.get_assets()
        return self.product.to_dict()
