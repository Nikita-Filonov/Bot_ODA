from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from orm.controllers import get_regions, get_variants, get_sub_variants
from orm.database import db_session
from orm.models import Region, Payload

variants = get_variants()
regions = get_regions()

medic_but = get_sub_variants("")

regions_markup = ReplyKeyboardMarkup(row_width=2).add(*[KeyboardButton(region["name"]) for region in regions])
variants_markup = ReplyKeyboardMarkup(row_width=2).add(*[KeyboardButton(variant["name"]) for variant in variants])
medic_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(sub_m) for sub_m in medic_but])

print(get_sub_variants(variant_name="🎓ОСВІТА"))
print(next(filter(lambda region: region['name'][1:] == "Агрономічна", get_regions())))
print(Region.get(db_session, name="👪Агрономічна").id)

Payload.create(db_session, phone="077", region_id=1, variant_id=1)
