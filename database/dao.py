from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def get_all_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct year 
                    from team 
                    where year >= 1980
                    order by year
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @ staticmethod
    def get_teams_by_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select id, team_code, name
                    from team 
                    where year = %s
                    order by team_code                              
                """

        cursor.execute(query,(year,))

        for row in cursor:
            team = Team(row["id"], row["team_code"], row["name"])
            result.append(team)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_salary(year):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ select  team_id, sum(salary) as tot_salary
                    from salary
                    where year = %s
                    group by team_id
                """

        cursor.execute(query,(year,))

        for row in cursor:
            result[row["team_id"]] = row["tot_salary"]

        cursor.close()
        conn.close()
        return result

