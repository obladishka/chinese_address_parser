from parser.models import AddressObject, Province, SpecialWord

from django.db.models.functions import Length


def init_settings(address: str) -> None:
    """Configures correct English translations for characters with several meanings."""

    village = AddressObject.objects.filter(cn_name="村").first()
    if "镇" in address and not village:
        village = AddressObject.objects.create(cn_name="村", eng_name="Village", is_parent_item=False, hierarchy=2.2)
        village.save()
    elif "镇" not in address and village:
        village.delete()

    floor = AddressObject.objects.get(cn_name="楼")
    if "层" in address:
        floor.eng_name = "Building"
        floor.hierarchy = 5.2
    else:
        floor.eng_name = "Floor"
        floor.hierarchy = 6.1
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
            region = region.replace(province.cn_name, f"{province.eng_name}")
            if "中国" in region:
                region = region.replace("中国", "China, ")
            return region, address
    return None, address


def translate_words(address: str) -> str:
    """Translates special words."""
    words = list(SpecialWord.objects.all())
    for word in words:
        address = address.replace(word.cn_name, f" {word.eng_name}, ")

    return address


def find_parent_objects(address: str) -> dict[str: str | None]:
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


def check_logic(address: str) -> dict[str: str | None]:
    """Checks parsing correctness."""
    raw_data = find_parent_objects(address)
    area = raw_data.get("area")
    city = raw_data.get("city")
    street = raw_data.get("street")
    house_num = raw_data.get("house_num")
    unit_num = raw_data.get("unit_num")
    house_ex = ""

    if unit_num and not house_num:
        house_num = unit_num
        unit_num = ""

    for obj in list(
        AddressObject.objects.order_by("hierarchy").filter(is_parent_item=False, hierarchy__gt=2, hierarchy__lt=3)
    ):
        if obj.cn_name in street:
            a, b = splitter(street, obj.cn_name)
            city += a
            street = b
        elif obj.cn_name in house_num and not street:
            a, b = splitter(house_num, obj.cn_name)
            city += a
            house_num = b

    if ", " in street:
        street = street.rsplit(", ", maxsplit=1)
        city += street[0]
        street = street[-1]
    elif ", " in house_num and not street:
        check_house_num = house_num.rsplit(", ", maxsplit=1)
        if "Building" not in check_house_num[0]:
            city += check_house_num[0]
            house_num = check_house_num[-1]

    for obj in list(
        AddressObject.objects.order_by("hierarchy").filter(is_parent_item=False, hierarchy__gt=3, hierarchy__lt=4)
    ):
        if obj.cn_name in house_num:
            a, b = splitter(house_num, obj.cn_name)
            street += a
            house_num = b

    if unit_num:
        items = AddressObject.objects.order_by("hierarchy").filter(
            is_parent_item=False, hierarchy__gt=5, hierarchy__lt=6
        )
        items_list = [item.cn_name for item in list(items)]
        if unit_num and unit_num[0] in items_list:
            unit_num = house_num + unit_num
            house_num = ""

        for obj in items:
            if obj.cn_name in unit_num:
                a, b = splitter(unit_num, obj.cn_name)
                house_ex += a
                unit_num = b

        units = list(AddressObject.objects.order_by("hierarchy").filter(is_parent_item=False, hierarchy__gt=6))
        if unit_num and not any([unit.cn_name in unit_num for unit in units]):
            house_ex = unit_num
            unit_num = ""

    return {
        "area": area,
        "city": city,
        "street": street,
        "house_num": house_num,
        "house_ex": house_ex,
        "unit_num": unit_num,
    }


def make_translations(
    area: str | None,
    city: str | None,
    street: str | None,
    house_num: str | None,
    house_ex: str | None,
    unit_num: str | None,
) -> dict[str: str | None]:
    """Translates address objects."""

    raw_list = [area, city, street, house_num, house_ex, unit_num]
    processed_list = []
    obj_list = ["area", "city", "street", "house_num", "house_ex", "unit_num"]

    for i, obj in enumerate(raw_list):
        if obj:
            words = list(
                AddressObject.objects.order_by("hierarchy")
                .filter(hierarchy__gte=i + 1, hierarchy__lt=i + 2)
                .order_by(Length("cn_name").desc())
            )
            for word in words:
                if word.cn_name in obj:
                    obj = obj.replace(word.cn_name, f" {word.eng_name}, ")
                obj = obj.rstrip(", ")
        processed_list.append(obj)

    return dict(zip(obj_list, processed_list))


def parse_address(address: str) -> dict[str: str | None]:
    """Main algorithm function."""
    init_settings(address)
    region, address = find_province(address)
    address = translate_words(address)
    result = check_logic(address)
    result = make_translations(**result)

    house_ex = result.get("house_ex")
    unit_num = result.get("unit_num")

    if house_ex and "号" in house_ex:
        result["house_ex"] = house_ex.replace("号", "")
    elif unit_num and "号" in unit_num:
        result["unit_num"] = unit_num.replace("号", "")

    raw_dict = {"region": region if region else ""}
    new_dict = raw_dict.update(result)
    return raw_dict
