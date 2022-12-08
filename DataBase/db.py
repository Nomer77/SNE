import aiosqlite


class TeleData:

    def __init__(self, db_file):
        self.base = db_file

    async def add_user(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("INSERT INTO users ('tele_id') VALUES (?)", (tele_id,))
            await connect.commit()

    async def is_user_exists(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT id FROM users WHERE tele_id = ?", (tele_id,)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return bool(len(result))

    async def add_task(self, tele_id, task, time=None):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("INSERT INTO tasks ('task', 'time', 'owner') VALUES (?, ?, ?)", (task, time, tele_id))
            await connect.commit()


    async def is_task_exists(self, tele_id, task, time):
        async with aiosqlite.connect(self.base) as connect:
            if time is None:
                async with connect.execute("SELECT id FROM tasks WHERE owner = ? AND task = ? AND time is NULL", (tele_id, task)) as cursor:
                    result = await cursor.fetchone()
                    await cursor.close()
                    return bool(result)
            else:
                async with connect.execute("SELECT id FROM tasks WHERE owner = ? AND task = ? AND time = ?", (tele_id, task, time)) as cursor:
                    result = await cursor.fetchone()
                    await cursor.close()
                    return bool(result)

    async def get_tasks(self, tele_id='%', is_complete='%', time='%', is_recalled='%', task_id='%'):
        if time is None:
            async with aiosqlite.connect(self.base) as connect:
                async with connect.execute("SELECT id, task, time FROM tasks WHERE owner LIKE ? AND is_complete LIKE ? AND is_recalled LIKE ? AND id LIKE ? AND time is NULL", (tele_id, is_complete, is_recalled, task_id)) as cursor:
                    result = await cursor.fetchall()
                    await cursor.close()
                    return result
        if time == '%':
            async with aiosqlite.connect(self.base) as connect:
                      async with connect.execute("SELECT id, task, time FROM tasks WHERE owner LIKE ? AND is_complete LIKE ? AND (time LIKE ? OR time is NULL) AND is_recalled LIKE ? AND id LIKE ?", (tele_id, is_complete, time, is_recalled, task_id)) as cursor:
                          result = await cursor.fetchall()
                          await cursor.close()
                          return result
        else:
            async with aiosqlite.connect(self.base) as connect:
                async with connect.execute("SELECT id, task, time FROM tasks WHERE owner LIKE ? AND is_complete LIKE ? AND time = ? AND is_recalled LIKE ? AND id LIKE ?", (tele_id, is_complete, time, is_recalled, task_id)) as cursor:
                    result = await cursor.fetchall()
                    await cursor.close()
                    return result


    async def delete_task(self, tele_id, task_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("DELETE FROM tasks WHERE owner = ? AND id = ?", (tele_id, task_id))
            await connect.commit()

    async def update_task(self, task_id, new_task, new_time):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE tasks SET task = ?, time = ? WHERE id = ?", (new_task, new_time, task_id))
            await connect.commit()

    async def set_complete(self, tele_id, task_id):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE tasks SET is_complete = 1, is_recalled = 2 WHERE id = ? AND owner = ?", (task_id, tele_id))
            await connect.commit()

# Last

    # async def get_tasks(self, tele_id='%', is_complete='%', time='%', is_recalled='%', task_id='%'):
    #     async with aiosqlite.connect(self.base) as connect:
    #         request = "SELECT task FROM tasks WHERE owner LIKE (?) AND is_complete LIKE (?) AND (time LIKE (?) OR " \
    #                   "time is NULL) AND is_recalled LIKE (?) AND id LIKE (?)"
    #         async with connect.execute(request, (tele_id, is_complete, time, is_recalled, task_id)) as cursor:
    #             result = await cursor.fetchall()
    #             await cursor.close()
    #             return result





    async def get_task_time(self, tele_id, task):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT time FROM tasks WHERE task = ? AND owner = ?",
                                       (task, tele_id)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return result

    async def get_task_user(self, task, time):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT owner FROM tasks WHERE task = ? AND time = ?", (task, time)) as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return result

    async def set_recalled(self, tele_id, task):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE tasks SET is_recalled = 1 WHERE task = ? AND owner = ?", (task, tele_id))
            await connect.commit()

    async def delete_all_task(self):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("DELETE FROM tasks")
            await connect.commit()

    async def get_task_owner(self, task_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT owner FROM tasks WHERE id = ?", (task_id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return result

    async def get_users(self):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT tele_id FROM users") as cursor:
                result = await cursor.fetchall()
                await cursor.close()
                return result

    async def get_valute_status(self, tele_id):
        async with aiosqlite.connect(self.base) as connect:
            async with connect.execute("SELECT valute FROM users WHERE tele_id = ?", (tele_id, )) as cursor:
                result = await cursor.fetchone()
                await cursor.close()
                return bool(result[0])

    async def valute_transform(self, tele_id, value):
        async with aiosqlite.connect(self.base) as connect:
            await connect.execute("UPDATE users SET valute = ? WHERE tele_id = ?", (value, tele_id))
            await connect.commit()
