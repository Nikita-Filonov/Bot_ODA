from orm.controllers import get_regions, get_variants
from bot.utils import build_keyboard

variants = get_variants()
regions = get_regions()

regions_markup = build_keyboard(mapping=regions, row_width=2)
variants_markup = build_keyboard(mapping=variants, row_width=2)
