import re
from bs4.element import Tag


def format_value(value: str) -> str:
    if "." in value:
        formatted_value = value.strip("0")
        formatted_value = formatted_value[:-1] if formatted_value.endswith(".") else formatted_value
    else:
        formatted_value = value.lstrip("0")

    return formatted_value if formatted_value else "0"


def get_spec_values(product_details: Tag, labels_to_find: list, unit: str = None) -> str | None:
    values_list = []
    for label in labels_to_find:
        label_tag = product_details.find("span", class_="label", string=label)
        value_tag = label_tag.find_next_sibling() if label_tag else None
        if value_tag:
            values_list.append(value_tag.get_text(strip=True))

    if not values_list:
        return None

    values = ";".join(values_list)
    if unit:
        pattern = rf'([\d.]+)\s{unit}'
        val_list = re.findall(pattern, values)
        values = "/".join([format_value(val) for val in val_list])

    return values if values else None


def convert_kw_to_hp(kw_values: str):
    if kw_values:
        hp_list = [round(float(kw) * 1.34102, 2) for kw in kw_values.split("/")]
        return "/".join([format_value(str(hp)) for hp in hp_list])
    return None
