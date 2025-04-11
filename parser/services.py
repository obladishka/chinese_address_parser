from parser.models import AddressObject, Province, SpecialWord


def init_settings(address: str) -> None:
    """Configures correct English translations for characters with several meanings."""

    village = AddressObject.objects.filter(cn_name="村").first()
    if "镇" in address:
        village = AddressObject.objects.create(cn_name="村", eng_name="Village", is_parent_item=False, hierarchy=2.2)
        village.save()
    elif "镇" not in address and village:
        village.delete()

    floor = AddressObject.objects.get(cn_name="楼")
    if "层" in address:
        floor.eng_name = "Building"
        floor.hierarchy = 4.2
    else:
        floor.eng_name = "Floor"
    floor.save()


def splitter(address: str, separator: str) -> tuple:
    """ "Cuts out" objects from address."""
    raw_data = address.split(separator, 1)
    obj = raw_data.pop(0) + separator
    return obj, "".join(raw_data)


def find_province(address: str) -> tuple:
    """Parses and translates province."""
    provinces = list(Province.objects.all())
    for province in provinces:
        if province.cn_name in address:
            region, address = splitter(address, province.cn_name)
            return region.replace(province.cn_name, f"{province.eng_name}"), address
    return None, address


def translate_words(address: str) -> str:
    """Translates special words."""
    words = list(SpecialWord.objects.all())
    for word in words:
        address = address.replace(word.cn_name, f" {word.eng_name} ")

    return address


def find_parent_objects(address: str) -> dict[str:str]:
    """Parses parent objects."""

    area = ""
    city = ""
    street = ""
    house_num = ""

    parent_objects = AddressObject.objects.filter(is_parent_item=True).order_by("hierarchy")

    if parent_objects.first().cn_name in address:
        area, address = splitter(address, parent_objects.first().cn_name)

    for parent_object in parent_objects.filter(hierarchy=2.0):
        if parent_object.cn_name in address:
            city, address = splitter(address, parent_object.cn_name)
            break

    for parent_object in parent_objects.filter(hierarchy=3.0):
        if parent_object.cn_name in address:
            street, address = splitter(address, parent_object.cn_name)
            break

    for parent_object in parent_objects.filter(hierarchy=4.0):
        if parent_object.cn_name in address:
            house_num, address = splitter(address, parent_object.cn_name)

    return {"area": area, "city": city, "street": street, "house_num": house_num, "unit_num": address}


def check_logic(address: str) -> dict[str:str]:
    """Checks parsing correctness."""
    raw_data = find_parent_objects(address)
    area = raw_data.get("area")
    city = raw_data.get("city")
    street = raw_data.get("street")
    house_num = raw_data.get("house_num")
    unit_num = raw_data.get("unit_num")
    house_ex = ""

    for obj in list(
        AddressObject.objects.order_by("hierarchy").filter(is_parent_item=False, hierarchy__gt=2, hierarchy__lt=3)
    ):
        if obj.cn_name in street:
            a, b = splitter(street, obj.cn_name)
            city += a
            street = b

    if " " in street:
        street = street.rsplit(maxsplit=1)
        city += street[0]
        street = street[-1]

    for obj in list(
        AddressObject.objects.order_by("hierarchy").filter(is_parent_item=False, hierarchy__gt=3, hierarchy__lt=4)
    ):
        if obj.cn_name in house_num:
            a, b = splitter(house_num, obj.cn_name)
            street += a
            house_num = b

    items = AddressObject.objects.order_by("hierarchy").filter(
        is_parent_item=False, hierarchy__gt=4, hierarchy__lt=4.5
    )
    items_list = [item.cn_name for item in list(items)]
    if unit_num and unit_num[0] in items_list:
        unit_num = house_num + unit_num
        house_num = None

    for obj in items:
        if obj.cn_name in unit_num:
            a, b = splitter(unit_num, obj.cn_name)
            house_ex += a
            unit_num = b

    if unit_num and not house_ex:
        house_ex = unit_num
        unit_num = None

    return {
        "area": area,
        "city": city,
        "street": street,
        "house_num": house_num,
        "house_ex": house_ex,
        "unit_num": unit_num,
    }


def parse_address(address: str) -> dict[str:str]:
    """Main algorithm function."""
    init_settings(address)
    region, address = find_province(address)
    address = translate_words(address)
    result = check_logic(address)
    area = result.get("area")
    city = result.get("city")
    street = result.get("street")
    house_num = result.get("house_num")
    house_ex = result.get("house_ex")
    unit_num = result.get("unit_num")
    return {
        "region": region,
        "area": area,
        "city": city,
        "street": street,
        "house_num": house_num,
        "house_ex": house_ex,
        "unit_num": unit_num,
    }
