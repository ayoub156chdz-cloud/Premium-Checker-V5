#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✨ TELEGRAM PREMIUM CHECKER BOT v3.2.1
✨ نظام متكامل للاشتراكات والتحقق من البطاقات
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pytz
from enum import Enum
import json
import random
import string
from dataclasses import dataclass, asdict
import aiohttp
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    CallbackQuery, Message
)
import redis
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
import hashlib

# ---------- CONFIGURATION ----------
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [8073880253]  # أدمن IDs
CHANNEL_USERNAME = "https://t.me/ayoubd18"  # القناة الإجبارية
DATABASE_URL = "mongodb://localhost:27017"
REDIS_URL = "redis://localhost:6379"

# ---------- DATABASE MODELS ----------
class UserStatus(Enum):
    BLOCKED = "blocked"
    TRIAL = "trial"
    SUBSCRIBED = "subscribed"
    ADMIN = "@xwaoi1"

class SubscriptionPlan(Enum):
    WEEK = {"stars": 15, "days": 7}
    HALF_MONTH = {"stars": 25, "days": 15}
    MONTH = {"stars": 50, "days": 30}

class PromoCode(BaseModel):
    code: str
    duration_hours: int
    created_by: int  # Admin ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used_by: List[int] = Field(default_factory=list)
    max_uses: int = 1

class User(BaseModel):
    user_id: int
    username: Optional[str]
    first_name: str
    status: UserStatus = UserStatus.TRIAL
    subscription_until: Optional[datetime]
    trial_used: bool = False
    last_trial_date: Optional[datetime]
    cards_today: int = 0
    balance: int = 0  # عدد النجوم
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_banned: bool = False
    
    class Config:
        use_enum_values = True

# ---------- BOT INITIALIZATION ----------
bot = AsyncTeleBot(BOT_TOKEN)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)
mongo_client = AsyncIOMotorClient(DATABASE_URL)
db = mongo_client.premium_checker
users_collection = db.users
promo_collection = db.promos
logs_collection = db.logs

# ---------- UTILITY FUNCTIONS ----------
def get_user_key(user_id: int) -> str:
    return f"user:{user_id}"

async def get_user(user_id: int) -> Optional[User]:
    cached = redis_client.get(get_user_key(user_id))
    if cached:
        return User.parse_raw(cached)
    
    user_data = await users_collection.find_one({"user_id": user_id})
    if user_data:
        user = User(**user_data)
        redis_client.setex(get_user_key(user_id), 300, user.json())
        return user
    return None

async def save_user(user: User):
    await users_collection.update_one(
        {"user_id": user.user_id},
        {"$set": asdict(user)},
        upsert=True
    )
    redis_client.setex(get_user_key(user.user_id), 300, user.json())

async def is_member(user_id: int) -> bool:
    """التحقق من اشتراك المستخدم في القناة"""
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ---------- MAIN MENUS ----------
def get_main_menu(user: User) -> InlineKeyboardMarkup:
    """القائمة الرئيسية بعد التحقق"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    if user.status == UserStatus.ADMIN:
        keyboard.add(
            InlineKeyboardButton("🛠 لوحة الأدمن", callback_data="admin_panel"),
            InlineKeyboardButton("📊 إحصائيات", callback_data="stats")
        )
    
    keyboard.add(
        InlineKeyboardButton("💳 فحص بطاقة", callback_data="check_card"),
        InlineKeyboardButton("🔑 إدخال رمز تجريبي", callback_data="enter_promo")
    )
    
    if user.status != UserStatus.SUBSCRIBED:
        keyboard.add(
            InlineKeyboardButton("⭐ شراء اشتراك", callback_data="buy_subscription"),
            InlineKeyboardButton("🆓 تجربة اليوم", callback_data="daily_trial")
        )
    
    keyboard.add(
        InlineKeyboardButton("📞 تواصل مع المطور", callback_data="contact_dev"),
        InlineKeyboardButton("🔄 تشغيل بروكسي", callback_data="run_proxy")
    )
    
    if user.status == UserStatus.SUBSCRIBED:
        keyboard.add(
            InlineKeyboardButton("🌐 اختبار على موقع", callback_data="test_site"),
            InlineKeyboardButton("📈 رصيدي: {} ⭐".format(user.balance), callback_data="balance")
        )
    
    return keyboard

def get_subscription_menu() -> InlineKeyboardMarkup:
    """قائمة شراء الاشتراكات"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    for plan in SubscriptionPlan:
        text = "{} ⭐ - اشتراك {} يوم".format(
            plan.value["stars"],
            plan.value["days"]
        )
        keyboard.add(InlineKeyboardButton(text, callback_data=f"buy_{plan.name}"))
    
    keyboard.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
    return keyboard

def get_admin_menu() -> InlineKeyboardMarkup:
    """قائمة الأدمن"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        ("🔑 إنشاء رموز تجريبية", "create_promo"),
        ("➕ إضافة رصيد", "add_balance"),
        ("📊 إحصائيات البوت", "bot_stats"),
        ("👥 قائمة المستخدمين", "list_users"),
        ("⛔ حظر مستخدم", "ban_user"),
        ("🔓 تجربة مجانية", "admin_trial"),
        ("🔙 رجوع", "main_menu")
    ]
    
    for text, callback in buttons:
        keyboard.add(InlineKeyboardButton(text, callback_data=callback))
    
    return keyboard

# ---------- HANDLERS ----------
@bot.message_handler(commands=['start'])
async def start_handler(message: Message):
    """معالجة أمر /start"""
    user_id = message.from_user.id
    
    # التحقق من الاشتراك في القناة
    if not await is_member(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        keyboard.add(InlineKeyboardButton("✅ تم الاشتراك", callback_data="check_subscription"))
        
        await bot.send_message(
            message.chat.id,
            "🔒 **الوصول مقيد**\n\n"
            "يجب الاشتراك في قناتنا أولاً:\n"
            f"{CHANNEL_USERNAME}\n\n"
            "بعد الاشتراك اضغط على ✅ تم الاشتراك",
            reply_markup=keyboard
        )
        return
    
    # إنشاء أو جلب بيانات المستخدم
    user = await get_user(user_id)
    if not user:
        user = User(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            status=UserStatus.ADMIN if user_id in ADMIN_IDS else UserStatus.TRIAL
        )
        await save_user(user)
    
    if user.is_banned:
        await bot.send_message(message.chat.id, "❌ تم حظرك من استخدام البوت.")
        return
    
    # عرض القائمة الرئيسية
    welcome_text = (
        f"مرحباً {message.from_user.first_name} 👋\n\n"
        f"🆔 ID: `{user_id}`\n"
        f"📅 اشتراكك حتى: {user.subscription_until.strftime('%Y-%m-%d') if user.subscription_until else 'غير مشترك'}\n"
        f"⭐ رصيدك: {user.balance} نجمة\n\n"
        "اختر من القائمة:"
    )
    
    await bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=get_main_menu(user),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
async def check_subscription(call: CallbackQuery):
    """التحقق من الاشتراك"""
    user_id = call.from_user.id
    
    if await is_member(user_id):
        await bot.answer_callback_query(call.id, "✅ تم التحقق من اشتراكك!")
        await start_handler(call.message)
    else:
        await bot.answer_callback_query(call.id, "❌ لم يتم العثور على اشتراكك!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "enter_promo")
async def enter_promo_handler(call: CallbackQuery):
    """إدخال الرمز التجريبي"""
    await bot.send_message(
        call.message.chat.id,
        "🔑 **أدخل الرمز التجريبي:**\n\n"
        "أرسل الرمز الآن...",
        parse_mode="Markdown"
    )
    
    @bot.message_handler(func=lambda m: m.chat.id == call.message.chat.id)
    async def process_promo(message: Message):
        promo_code = message.text.upper().strip()
        
        # البحث عن الرمز في قاعدة البيانات
        promo_data = await promo_collection.find_one({"code": promo_code})
        if not promo_data:
            await bot.send_message(message.chat.id, "❌ الرمز غير صالح أو منتهي الصلاحية!")
            return
        
        promo = PromoCode(**promo_data)
        user = await get_user(message.from_user.id)
        
        if user.user_id in promo.used_by:
            await bot.send_message(message.chat.id, "❌ لقد استخدمت هذا الرمز مسبقاً!")
            return
        
        if len(promo.used_by) >= promo.max_uses:
            await bot.send_message(message.chat.id, "❌ تم استخدام هذا الرمز لأقصى عدد من المرات!")
            return
        
        # تفعيل الرمز
        until = datetime.utcnow() + timedelta(hours=promo.duration_hours)
        user.subscription_until = until
        user.status = UserStatus.SUBSCRIBED
        promo.used_by.append(user.user_id)
        
        await save_user(user)
        await promo_collection.update_one(
            {"code": promo_code},
            {"$set": {"used_by": promo.used_by}}
        )
        
        await bot.send_message(
            message.chat.id,
            f"✅ **تم تفعيل الرمز بنجاح!**\n\n"
            f"⏰ المدة: {promo.duration_hours} ساعة\n"
            f"📅 ينتهي في: {until.strftime('%Y-%m-%d %H:%M')}",
            reply_markup=get_main_menu(user),
            parse_mode="Markdown"
        )
        
        bot.remove_message_handler(process_promo)

@bot.callback_query_handler(func=lambda call: call.data == "daily_trial")
async def daily_trial_handler(call: CallbackQuery):
    """تجربة يومية"""
    user = await get_user(call.from_user.id)
    now = datetime.utcnow()
    
    # التحقق من استخدام التجربة اليوم
    if user.last_trial_date and user.last_trial_date.date() == now.date():
        await bot.answer_callback_query(call.id, "❌ لقد استخدمت تجربة اليوم بالفعل!", show_alert=True)
        return
    
    if user.cards_today >= 3:
        await bot.answer_callback_query(call.id, "❌ لقد استخدمت جميع محاولاتك اليومية!", show_alert=True)
        return
    
    user.last_trial_date = now
    user.cards_today = 0
    await save_user(user)
    
    await bot.send_message(
        call.message.chat.id,
        "🆓 **التجربة اليومية**\n\n"
        "يمكنك الآن فحص 3 بطاقات مجاناً!\n"
        "أرسل البطاقة الأولى:\n\n"
        "📝 **التنسيق:**\n"
        "`رقم البطاقة|تاريخ الانتهاء|CVV`",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
async def buy_subscription_handler(call: CallbackQuery):
    """شراء اشتراك"""
    plan_name = call.data.split("_")[1]
    plan = SubscriptionPlan[plan_name]
    
    user = await get_user(call.from_user.id)
    
    if user.balance < plan.value["stars"]:
        await bot.answer_callback_query(
            call.id,
            f"❌ رصيدك غير كافي!\nمطلوب: {plan.value['stars']} ⭐\nرصيدك: {user.balance} ⭐",
            show_alert=True
        )
        return
    
    # خصم الرصيد وتفعيل الاشتراك
    user.balance -= plan.value["stars"]
    user.status = UserStatus.SUBSCRIBED
    user.subscription_until = datetime.utcnow() + timedelta(days=plan.value["days"])
    
    await save_user(user)
    
    await bot.send_message(
        call.message.chat.id,
        f"✅ **تم شراء الاشتراك بنجاح!**\n\n"
        f"📦 الباقة: {plan.value['days']} يوم\n"
        f"⭐ المبلغ: {plan.value['stars']} نجمة\n"
        f"📅 ينتهي في: {user.subscription_until.strftime('%Y-%m-%d')}\n\n"
        f"📊 الرصيد المتبقي: {user.balance} ⭐",
        reply_markup=get_main_menu(user),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "contact_dev")
async def contact_dev_handler(call: CallbackQuery):
    """عروض الاشتراك قبل المراسلة"""
    text = (
        "💎 **عروض الاشتراك:**\n\n"
        "15 ⭐ - اشتراك أسبوع\n"
        "25 ⭐ - اشتراك 15 يوم\n"
        "50 ⭐ - اشتراك 25 يوم\n\n"
        "للشراء راسل: @المطور"
    )
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("📞 مراسلة المطور", url="https://t.me/المطور"))
    keyboard.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
    
    await bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_card")
async def check_card_handler(call: CallbackQuery):
    """فحص البطاقات"""
    user = await get_user(call.from_user.id)
    
    if user.status != UserStatus.SUBSCRIBED and user.status != UserStatus.ADMIN:
        if user.cards_today >= 3:
            await bot.answer_callback_query(
                call.id,
                "❌ لقد استخدمت جميع محاولاتك!\nاشترك للحصول على بوت دائم سريع.",
                show_alert=True
            )
            return
    
    await bot.send_message(
        call.message.chat.id,
        "💳 **أرسل البطاقة للفحص:**\n\n"
        "📝 **التنسيق:**\n"
        "`رقم البطاقة|تاريخ الانتهاء|CVV`\n\n"
        "⚠️ **الحد الأقصى: 20 بطاقة في المرة**",
        parse_mode="Markdown"
    )
    
    @bot.message_handler(func=lambda m: m.chat.id == call.message.chat.id)
    async def process_cards(message: Message):
        cards = [card.strip() for card in message.text.split('\n') if card.strip()]
        
        if len(cards) > 20:
            await bot.send_message(message.chat.id, "❌ الحد الأقصى 20 بطاقة فقط!")
            return
        
        # تحديث عداد البطاقات للمستخدم التجريبي
        if user.status == UserStatus.TRIAL:
            user.cards_today += len(cards)
            if user.cards_today > 3:
                await bot.send_message(
                    message.chat.id,
                    "❌ اكتملت عدد تجربتك!\nاشترك للحصول على بوت دائم سريع."
                )
                bot.remove_message_handler(process_cards)
                return
            await save_user(user)
        
        # محاكاة فحص البطاقات
        results = []
        for i, card in enumerate(cards, 1):
            # محاكاة النتائج العشوائية
            status = random.choice(["✅ مقبولة", "❌ ميتة", "⚠️ تطلب رمز"])
            balance = random.choice([0, random.randint(10, 100), random.randint(100, 1000)])
            
            if status == "✅ مقبولة":
                result_text = f"{i}. {card[:12]}**** - ✅ مقبولة"
                if balance > 0:
                    result_text += f" (رصيد: ~${balance})"
            else:
                result_text = f"{i}. {card[:12]}**** - {status}"
            
            results.append(result_text)
        
        # عرض النتائج
        result_message = "📊 **نتائج الفحص:**\n\n" + "\n".join(results)
        
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🔄 تشغيل بروكسي", callback_data="run_proxy"),
            InlineKeyboardButton("🌐 اختبار على موقع", callback_data="test_site")
        )
        
        await bot.send_message(
            message.chat.id,
            result_message,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
        bot.remove_message_handler(process_cards)

@bot.callback_query_handler(func=lambda call: call.data == "test_site")
async def test_site_handler(call: CallbackQuery):
    """اختبار البطاقات على موقع"""
    user = await get_user(call.from_user.id)
    
    if user.status != UserStatus.SUBSCRIBED and user.status != UserStatus.ADMIN:
        await bot.answer_callback_query(call.id, "❌ هذه الميزة للمشتركين فقط!", show_alert=True)
        return
    
    await bot.send_message(
        call.message.chat.id,
        "🌐 **اختبار على موقع**\n\n"
        "أرسل 4 بطاقات للاختبار (كل بطاقتين بروكسي مختلف):\n\n"
        "📝 **التنسيق:**\n"
        "`بطاقة1|تاريخ1|CVV1`\n"
        "`بطاقة2|تاريخ2|CVV2`\n"
        "`بطاقة3|تاريخ3|CVV3`\n"
        "`بطاقة4|تاريخ4|CVV4`",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
async def admin_panel_handler(call: CallbackQuery):
    """لوحة الأدمن"""
    user = await get_user(call.from_user.id)
    
    if user.status != UserStatus.ADMIN:
        await bot.answer_callback_query(call.id, "❌ غير مسموح!", show_alert=True)
        return
    
    await bot.edit_message_text(
        "🛠 **لوحة التحكم الإدارية**\n\n"
        "اختر الإجراء المطلوب:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_admin_menu(),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "create_promo")
async def create_promo_handler(call: CallbackQuery):
    """إنشاء رموز تجريبية"""
    await bot.send_message(
        call.message.chat.id,
        "🔑 **إنشاء رمز تجريبي:**\n\n"
        "أرسل التنسيق:\n"
        "`المدة_بالساعات|عدد_الاستخدامات`\n\n"
        "مثال: `24|5` لرمز مدته 24 ساعة و 5 استخدامات",
        parse_mode="Markdown"
    )
    
    @bot.message_handler(func=lambda m: m.chat.id == call.message.chat.id and m.from_user.id in ADMIN_IDS)
    async def process_promo_creation(message: Message):
        try:
            hours, uses = map(int, message.text.split('|'))
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            promo = PromoCode(
                code=code,
                duration_hours=hours,
                created_by=message.from_user.id,
                max_uses=uses
            )
            
            await promo_collection.insert_one(promo.dict())
            
            await bot.send_message(
                message.chat.id,
                f"✅ **تم إنشاء الرمز:**\n\n"
                f"🔑 الكود: `{code}`\n"
                f"⏰ المدة: {hours} ساعة\n"
                f"🔢 الاستخدامات: {uses}\n\n"
                f"📅 الإنشاء: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await bot.send_message(message.chat.id, f"❌ خطأ في التنسيق: {str(e)}")
        
        bot.remove_message_handler(process_promo_creation)

@bot.callback_query_handler(func=lambda call: call.data == "bot_stats")
async def bot_stats_handler(call: CallbackQuery):
    """إحصائيات البوت"""
    total_users = await users_collection.count_documents({})
    active_users = await users_collection.count_documents({"status": "subscribed"})
    trial_users = await users_collection.count_documents({"status": "trial"})
    total_checks = await logs_collection.count_documents({"type": "card_check"})
    
    stats_text = (
        "📊 **إحصائيات البوت:**\n\n"
        f"👥 إجمالي المستخدمين: {total_users}\n"
        f"✅ المشتركين النشطين: {active_users}\n"
        f"🆓 المستخدمين التجريبيين: {trial_users}\n"
        f"💳 إجمالي عمليات الفحص: {total_checks}\n\n"
        f"🕒 آخر تحديث: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    )
    
    await bot.edit_message_text(
        stats_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "list_users")
async def list_users_handler(call: CallbackQuery):
    """قائمة المستخدمين"""
    users = await users_collection.find().sort("created_at", -1).limit(10).to_list(10)
    
    users_list = []
    for user_data in users:
        user = User(**user_data)
        profile_link = f"tg://user?id={user.user_id}"
        users_list.append(
            f"👤 [{user.first_name}]({profile_link})\n"
            f"🆔 `{user.user_id}` | 📅 {user.created_at.strftime('%Y-%m-%d')}\n"
            f"🔸 الحالة: {user.status.value}\n"
        )
    
    text = "👥 **آخر 10 مستخدمين:**\n\n" + "\n".join(users_list)
    
    await bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_trial")
async def admin_trial_handler(call: CallbackQuery):
    """الأدمن يمكنه تجربة أي شيء"""
    user = await get_user(call.from_user.id)
    user.status = UserStatus.ADMIN
    user.subscription_until = datetime.utcnow() + timedelta(days=36500)  # 100 سنة
    user.balance = 999999
    
    await save_user(user)
    
    await bot.answer_callback_query(
        call.id,
        "✅ تم تفعيل صلاحيات الأدمن الكاملة!\nيمكنك الآن تجربة كل الميزات بدون قيود.",
        show_alert=True
    )

# ---------- RUN BOT ----------
async def main():
    print("🤖 البوت يعمل...")
    await bot.polling(none_stop=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
