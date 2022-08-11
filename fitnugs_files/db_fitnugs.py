from sqlite3 import Error

import cogs.fitnugs_files.fitnugsconfig as fn
from db.db_connection import DbConnection


class DbFitNugs(DbConnection):

    #           **************              CURRENCY TABLES             **********************

    def create_tables(self):
        #   FitNugs

        fitnugs = """CREATE TABLE IF NOT EXISTS fitnugs
                                   (id INTEGER PRIMARY KEY,
                                   user_id VARCHAR(255) NOT NULL,                                   
                                   timestamp VARCHAR(255) NOT NULL,
                                   activity VARCHAR(255) NOT NULL,
                                   minutes INTEGER NOT NULL,
                                   intensity VARCHAR(255),
                                   intensity_points INTEGER NOT NULL,
                                   total INTEGER NOT NULL)
                                   """
        self.create_tables_q.append(fitnugs)

        try:

            for t in self.create_tables_q:
                self.db.execute(t)
                print("CREATED FITNUGS TABLES")
        except Error as e:
            print(e)
            print("ERROR CREATING FITNUGS TABLES")

    async def add_workout(self, discord_user_id, discord_server_id, minutes, activity, intensity):
        try:
            user_id = await self.get_user_id(discord_user_id, discord_server_id)
            timestamp = await self.get_current_timestamp()
            multiplier = fn.intensity_multipliers[intensity]
            print(multiplier)
            total = int(minutes) * multiplier
            print(total)
            intensity_points = fn.intensity_points[intensity]
            sql = """   INSERT INTO fitnugs 
                                    (user_id, timestamp, activity, minutes, intensity, intensity_points, total)
                             VALUES (?, ?, ? , ? , ? , ? , ?)           """
            params = (user_id, timestamp, activity, minutes, intensity, intensity_points, total)
            self.db.execute(sql, params)
            print("success loging workout")
            return True
        except Error as e:
            print(e)
            print("error logging workout")
            return False

    async def get_workout_total(self, discord_user_id, discord_server_id, timespan):
        try:
            user_id = await self.get_user_id(discord_user_id, discord_server_id)
            now = await self.get_current_timestamp()
            timestamp = now - fn.timespan_values[timespan]

            sql = """   SELECT  SUM(minutes)
                               FROM    fitnugs 
                               WHERE   user_id = ? 
                               AND     timestamp > ? """

            params = (user_id, timestamp)
            self.db.execute(sql, params)
            result = self.db.fetchall()
            print("get_workout_total result")

            print(result)
            if result[0][0] == None:
                result = 0
                return result
            ### todo: check/format result, return 0 for users without entry
            return float(result[0][0])
        except Error as e:
            print(e)
            print("error getting workout total")
            return (0, 0)

    async def get_workout_leaderboard(self, timespan):
        now = await self.get_current_timestamp()
        timestamp = now - fn.timespan_values[timespan]

        sql = """   SELECT      user_id, SUM(minutes) as total, SUM(intensity_points) as points, COUNT(timestamp) as times
                    FROM        fitnugs 
                    GROUP BY    user_id
                    HAVING      timestamp > ? 
                    ORDER BY    total DESC,
                                points DESC,
                                times DESC"""

        params = (timestamp,)
        self.db.execute(sql, params)
        result = self.db.fetchall()
        print("get_workout_leaderboard result")

        print(result)
        return result
