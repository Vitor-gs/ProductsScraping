import re
from bs4.element import Tag


def format_value(value: str) -> str:
    """
    Formats a numeric string by removing unnecessary zeros and dealing with decimals.
    :param value: A string representing a numeric value.
    :return: The cleaned and formatted numeric string
    """
    if "." in value:
        formatted_value = value.strip("0")
        formatted_value = formatted_value[:-1] if formatted_value.endswith(".") else formatted_value
    else:
        formatted_value = value.lstrip("0")

    return formatted_value if formatted_value else "0"


def get_spec_values(product_details: Tag, labels_to_find: list, unit: str = None) -> str | None:
    """
    Extracts and formats specification values from a product details HTML block.
    :param product_details: A BeautifulSoup Tag containing the product specification section.
    :param labels_to_find: List of label names (as strings) to look for in the product details.
    :param unit: If provided, filters and formats values that match this unit.
    :return: A string of formatted values separated by "/", or None if no matching values are found.
    """
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


def convert_kw_to_hp(kw_values: str) -> str | None:
    """
    Some products list power in kilowatts, while others use horsepower. This function standardizes
    the data by converting kW values to HP using the conversion factor 1 kW = 1.34102 HP.
    :param kw_values: A string of numeric values separated by "/", representing power in kW.
    :return: A string of converted values in HP, or None if input is empty.
    """
    if kw_values:
        hp_list = [round(float(kw) * 1.34102, 2) for kw in kw_values.split("/")]
        return "/".join([format_value(str(hp)) for hp in hp_list])
    return None
