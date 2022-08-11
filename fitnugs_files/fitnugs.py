import disnake
from disnake.ext import commands

import cogs.fitnugs_files.fitnugsconfig as fn
from cogs.fitnugs_files.db_fitnugs import DbFitNugs


class FitNugsBot(commands.Cog):

    ####################################################################################################################
    ######################################   HELP FUNCTIONS   ##########################################################
    ####################################################################################################################
    async def log_workout(self, user_id, server_id, minutes, description, intensity):
        print("log_workout")
        print(minutes)
        print(description)
        print(intensity)
        db = DbFitNugs()
        await db.add_workout(user_id, server_id, minutes, description, intensity)
        db.conn.commit()
        db.conn.close()

    async def get_leaderboard(self, timespan):
        db = DbFitNugs()
        leaderboard_array = await db.get_workout_leaderboard(timespan)
        db.conn.commit()
        db.conn.close()
        print(leaderboard_array)
        return leaderboard_array

    ####################################################################################################################
    ######################################   SLASH COMMANDS   ##########################################################
    ####################################################################################################################
    @commands.slash_command(
        name=fn.workout_command_name,
        description=fn.workout_command_description
    )
    async def workout(self, inter: disnake.ApplicationCommandInteraction, minutes: int,
                      intensity: str = commands.Param(choices=fn.intensity_levels),
                      activity: str = commands.Param(choices=fn.activities), other: str = "activity"):
        print('workout')
        discord_user_id = inter.user.id
        discord_server_id = inter.guild_id

        if other != "activity":
            activity = other

        try:
            await self.log_workout(discord_user_id, discord_server_id, minutes, activity, intensity)
            await inter.response.send_message(
                str(minutes) + "minutes of '" + intensity + "  " + activity + "' were logged")

        except Exception as e:
            print(e)
            print("problem doing workout")
            await inter.response.send_message("there was an error logging your workout, please try again")

    @commands.slash_command(
        name=fn.workout_leaderboard_command_name,
        description=fn.workout_leaderboard_command_description
    )
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction,
                          timespan: str = commands.Param(choices=fn.leaderboard_timespans)):
        print("leaderboard " + timespan)

        try:
            leaderboard_array = await self.get_leaderboard(timespan)
            print(leaderboard_array)
            rank = 1
            message = "FITNUGS LEADERBOARD FOR PAST " + timespan.upper() + "\n"
            message += "-------------------------------------------------------------------" + "\n"
            for x in leaderboard_array:
                ##todo: change in db

                username = inter.guild.get_member(int(x[0]))
                print(username)
                message += str(rank) + "  -   " + str(username) + " (" + str(x[1]) + " minutes, " + str(
                    x[3]) + " workouts)" + "\n"
                rank += 1

            await inter.response.send_message(message)

        except Exception as e:
            print(e)
            print("problem getting leaderboard")
            await inter.response.send_message("there was an error getting the leaderboard, please try again")


def setup(bot: commands.Bot):
    #   MAKE SURE DB TABLES ARE CREATED
    try:
        db = DbFitNugs()
        db.create_tables()
    except Exception as e:
        print(e)

    bot.add_cog(FitNugsBot(bot))
