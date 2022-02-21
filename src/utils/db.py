import aiosqlite
from disnake import User

from .utils import aobject

class EcoUser(aobject):
    async def __init__(self, id: int, db, table):
        self.id = id
        self.db = db
        self.table = table
        cur = await self.db.cursor()
        await cur.execute(f"SELECT * FROM {self.table}")
        u = await cur.fetchall()
        users = [i[0] for i in u]
        if self.id not in users:
            self.inDatabase = False
        else:
            self.inDatabase = True
        await cur.close()

    async def getBalance(self):
        cur = await self.db.cursor()
        res = await cur.execute(f"SELECT balance FROM {self.table} WHERE id = {self.id}")
        a = await cur.fetchone()
        await cur.close()
        return a[0]

    async def setBalance(self, amount: int):
        cur = await self.db.cursor()
        await cur.execute(f"UPDATE {self.table} SET balance = {amount} WHERE id = {self.id}")
        await cur.close()
        await self.db.commit()
    
    async def openAccount(self):
        cur = await self.db.cursor()
        await cur.execute(f"SELECT * FROM {self.table}")
        users = [i[0] for i in await cur.fetchall()]
        if self.id in users:
            return False
        await cur.execute(f"INSERT INTO {self.table} (id, balance) VALUES ({self.id}, 0)")
        await cur.close()
        await self.db.commit()
        return True

class EconomyDatabase:
    async def __aenter__(self):
        self.file = "economy.db"
        self.db = await aiosqlite.connect(f"src/databases/{self.file}")
        cur = await self.db.cursor()
        self.table = self.file[:-3]
        await cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table}(id INTEGER, balance INTEGER)")
        await cur.close()
        await self.db.commit()

        return self
    
    async def EconomyLeaderboard(self):
        cur = await self.db.cursor()
        await cur.execute(f"SELECT * FROM {self.table} ORDER BY balance")
        a = await cur.fetchall()
        users = []
        for i in a:
            users.append(await EcoUser(a[0], self.db, self.table))
        return users[:10]

    async def getUser(self, user: User):
        return await EcoUser(user.id, self.db, self.table)

    async def __aexit__(self, a, b, c):
        await self.db.close()