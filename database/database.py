import aiosqlite
import os

from config import DATABASE


# ==============================
# Database Initialization
# ==============================

async def init_database():

    folder = os.path.dirname(DATABASE)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS cases (

            case_id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            moderator_id INTEGER NOT NULL,

            action TEXT NOT NULL,

            reason TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings (

            warning_id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            moderator_id INTEGER NOT NULL,

            reason TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (

            guild_id INTEGER PRIMARY KEY,

            log_channel INTEGER,

            prefix TEXT DEFAULT '!'
        )
        """)


        await db.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            channel_id INTEGER NOT NULL,

            status TEXT DEFAULT 'open',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


        await db.commit()


# ==============================
# Add Moderation Case
# ==============================

async def add_case(
    guild_id,
    user_id,
    moderator_id,
    action,
    reason
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            INSERT INTO cases
            (
                guild_id,
                user_id,
                moderator_id,
                action,
                reason
            )

            VALUES (?, ?, ?, ?, ?)
            """,

            (
                guild_id,
                user_id,
                moderator_id,
                action,
                reason
            )
        )


        await db.commit()

        return cursor.lastrowid


# ==============================
# Add Warning
# ==============================

async def add_warning(
    guild_id,
    user_id,
    moderator_id,
    reason
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            INSERT INTO warnings
            (
                guild_id,
                user_id,
                moderator_id,
                reason
            )

            VALUES (?, ?, ?, ?)
            """,

            (
                guild_id,
                user_id,
                moderator_id,
                reason
            )
        )


        await db.commit()

        return cursor.lastrowid


# ==============================
# Get User Warnings
# ==============================

async def get_warnings(
    guild_id,
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            """
            SELECT *
            FROM warnings
            WHERE guild_id = ?
            AND user_id = ?
            """,

            (
                guild_id,
                user_id
            )
        )


        return await cursor.fetchall()
