from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from keyboards import platforma, menu
from funk import toifa_tugmalari, xizmat_tugmalari, get_xizmat_name_by_service, get_service_min_max, get_platforma_toifa_by_service


router = Router()
msg1="🖇Quyidagi xizmatlardan birini tanlang"
msg2 = "👋Assalomu aleykum botimizga hush kelibsiz. Kerakli menyuni tanlang!"

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(msg2, reply_markup=menu)



@router.message(F.text == "🗂 Xizmatlar")
async def xizmatlar_handler(message: Message):
    await message.answer('🖇Quyidagilardan tarmoqlardan birini tanlang!', reply_markup=platforma)


@router.callback_query(F.data.startswith("platforma:"))
async def xizmat_handler(callback: CallbackQuery):
    platforma = callback.data.split(":")[1]  # Masalan, "telegram"
    await callback.message.edit_text(msg1, reply_markup=toifa_tugmalari(platforma))
    await callback.answer()



@router.callback_query(F.data.regexp(r"^(telegram|instagram|youtube|tiktok):"))
async def toifa_handler(callback: CallbackQuery):
    platforma, toifa = callback.data.split(":", 1)  # faqat birinchi ":" bo'yicha bo'lish
    await callback.message.edit_text(
        f"🖇 {toifa} xizmatlari",
        reply_markup=xizmat_tugmalari(platforma, toifa)
    )
    await callback.answer()



@router.callback_query(F.data.startswith("service:"))
async def service_handler(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[1])
    service_name = get_xizmat_name_by_service(service_id)
    order = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Buyurtma berish", callback_data=f"order:{service_id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back:{service_id}")
        ]
    ]
    )
    await callback.message.edit_text(f"🆔Xizmat raqami: {service_id} \n⚡️Xizmat nomi: {service_name}\n\n{get_service_min_max(service_id)}", reply_markup=order)
    await callback.answer()


    
@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text('🖇Quyidagilardan tarmoqlardan birini tanlang!', reply_markup=platforma)
    await callback.answer()

@router.callback_query(F.data.startswith("back:"))
async def back_to_xizmatlar(callback: CallbackQuery):
    service_id = int(callback.data.split(":")[1])

    result = get_platforma_toifa_by_service(service_id)
    if result is None:
        await callback.answer("⚠️ Qaytish ma'lumotlari topilmadi", show_alert=True)
        return

    platforma, toifa = result

    await callback.message.edit_text(
        f"🖇 {toifa} xizmatlari",
        reply_markup=xizmat_tugmalari(platforma, toifa)
    )
    await callback.answer()
