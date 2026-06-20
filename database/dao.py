from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def anni_dd():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct year from team t 
                    where t.year >=1980 """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams_by_year(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select id,team_code,name from team t 
                            where t.year = %s """
        cursor.execute(query,(year,))
        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_salary(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ select team_id,sum(salary) as total
                    from salary s
                    where year = %s
                    group by team_id """
        cursor.execute(query, (year,))
        result = {row["team_id"]: row["total"] for row in cursor}

        cursor.close()
        conn.close()
        return result
