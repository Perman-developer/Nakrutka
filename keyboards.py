from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from xizmatlar import xizmatlar

keyboard=[
    [KeyboardButton(text="🗂 Xizmatlar"), KeyboardButton(text="🔍 Buyurtmalarim")],
    [KeyboardButton(text="💰Hisob toʻldirish"), KeyboardButton(text="👤Mening hisobim")],
    [KeyboardButton(text="👥Referral"), KeyboardButton(text="☎️ Qo'llab-quvvatlash")],
]

menu = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
platforma = InlineKeyboardMarkup(
    inline_keyboard=[
        [
          InlineKeyboardButton(text="🔵Telegram" , callback_data="platforma:telegram")
        ],
        [
          InlineKeyboardButton(text="🔴Instagram", callback_data="platforma:instagram"),
          InlineKeyboardButton(text="⚫️Tik Tok", callback_data="platforma:tiktok")
        ],
        [
          InlineKeyboardButton(text="🟡You Tube", callback_data="platforma:youtube"),
          InlineKeyboardButton(text="🎁 Tekin xizmat", callback_data="platforma:free")
        ]
    ]
)

