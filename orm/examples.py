from orm.controllers import get_regions, get_variants, get_sub_variants, get_variant_payload

variant_name = '❤МЕДИЦИНА'
region_name = 'Region1'
sub_variant_name = '💊ВТОРИНКА'

print(get_regions())
print(get_variants())
print(get_sub_variants(variant_name=region_name))
print(get_variant_payload(variant_name=variant_name, region_name=region_name, sub_variant_name=sub_variant_name))

variant_name_1 = '💆ПСИХОЛОГ'
sub_variant_name_1 = None

print(get_regions())
print(get_variants())
print(get_sub_variants(variant_name=variant_name_1))
print(get_variant_payload(variant_name=variant_name_1, region_name=region_name, sub_variant_name=sub_variant_name_1))
