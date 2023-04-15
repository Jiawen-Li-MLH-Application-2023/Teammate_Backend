import pymysql

import os

###Define default LIMIT and OFFSET
LIMIT = 50
OFFSET = 0

class TeamResource:
    @classmethod
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = "admin"
        password = "1234567890"
        h = "e6156.coxz1yzswsen.us-east-1.rds.amazonaws.com"
        conn = pymysql.connect(
            user = user,
            password = password,
            host = h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn
    @staticmethod
    def browse_all_team(course_id, limit, offset):
        if not (course_id):
            return False, "Please fill in all blanks!"
        sql1 = "SELECT * FROM teammate_db.Team WHERE Course_id = %s";
        sql2 = "SELECT * From teammate_db.Team WHERE Course_id = %s LIMIT %s OFFSET %s"
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(course_id))
        records = cur.fetchall()
        length = len(records)
        cur.execute(sql2, args=(course_id, int(limit), int(offset)))
        records = cur.fetchall()
        return length, records

    @staticmethod
    def browse_team_info_by_input(course_id, team_captain_uni):
        if not (course_id and team_captain_uni):
            return False, "Please fill in all blanks!"
        sql = "SELECT * From teammate_db.Team WHERE Course_id = %s and team_captain_uni = %s"
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=(course_id, team_captain_uni))
        records = cur.fetchall()
        return records

    @staticmethod
    def add_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
        if not (team_name and course_id and team_captain_uni and team_captain):
            return False, "Please fill in all blanks!"
        team_name = team_name.strip()
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        print(team_captain_uni, course_id)
        sql1 = """
                    SELECT * From teammate_db.Team 
                    WHERE Team_Captain_Uni = %s and Course_id = %s
                    """
        cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        print(records)
        if len(records) >= 1:
            return False, "Duplicated Team"
        sql2 = """
                      insert into teammate_db.Team (Team_Name, Team_Captain_Uni, Team_Captain, Course_id, Number_needed, Team_message)
                      values (%s, %s, %s, %s, %s, %s);
                     """
        cur.execute(sql2, args=(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message))
        sql3 = """
              Insert into teammate_db.StudentsInTeam  (Uni, Student_Name, Team_id, Course_id)
              values (%s, %s, (SELECT Team_id
                            FROM teammate_db.Team
                            where Team_Captain_Uni=%s
                            and Course_id=%s
                                ), %s);
               """
        cur.execute(sql3, args=(team_captain_uni, team_captain, team_captain_uni, course_id, course_id))
        result = cur.rowcount
        if result == 1:
            return True, "Success"
        else:
            return False, "Add Team failed"


    @staticmethod
    def edit_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
        if not (team_captain_uni and course_id):
            return False
        conn = TeamResource._get_connection()
        team_name, team_captain, course_id = team_name.strip(), team_captain.strip(), course_id.strip()
        cur = conn.cursor()
        sql1 = """
            SELECT * FROM teammate_db.Team where team_captain_uni = %s and course_id = %s
            """
        res = cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = """
            UPDATE teammate_db.Team 
            set team_captain = %s, number_needed = %s, team_message = %s, team_name = %s
            where team_captain_uni = %s and course_id = %s
            """;
        cur.execute(sql2, args=(team_captain, number_needed, team_message, team_name, team_captain_uni, course_id))
        return True

    @staticmethod
    def delete_team(team_captain_uni, course_id, team_id):
        if not (course_id and team_captain_uni and team_id):
            return False
        sql1 = """
        SELECT * FROM teammate_db.Team where Team_Captain_Uni = %s and Course_id = %s
        """
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = """
            DELETE FROM teammate_db.StudentsInTeam 
                    where Team_id = %s
                """;
        cur.execute(sql2, args=team_id)
        sql3 = "DELETE FROM teammate_db.Team where Team_Captain_Uni = %s and Course_id = %s";
        cur.execute(sql3, args=(team_captain_uni, course_id))
        return True

    @staticmethod
    def get_all_team_member(team_id, course_id):
        sql = "SELECT * FROM teammate_db.StudentsInTeam where Team_id = %s and Course_id = %s";
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=(team_id, course_id))
        result = cur.fetchall()
        return result

    @staticmethod
    def add_team_member(uni, student_name, team_id, course_id):
        if not (uni and student_name and team_id and course_id):
            return False, "Please fill in all blanks!"
        uni = uni.strip()
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        sql1 = """
                SELECT * From teammate_db.StudentsInTeam 
                WHERE Uni = %s and Team_id = %s and Course_id = %s 
                """
        cur.execute(sql1, args=(uni, team_id, course_id))
        records = cur.fetchall()
        if len(records) >= 1:
            return False, "DUPLICATED MEMBER"
        sql2 = """
                 insert into teammate_db.StudentsInTeam  (Uni, Student_Name, Team_id, Course_id)
                 values (%s, %s, %s, %s);
                """
        cur.execute(sql2, args=(uni, student_name, team_id, course_id))
        result = cur.rowcount
        if result == 1:
            return True, "Success"
        else:
            return False, "Failure"

    @staticmethod
    def delete_team_member(uni, team_id, course_id):
        if not (uni and team_id and course_id):
            return False
        sql1 = """
        SELECT * From teammate_db.StudentsInTeam WHERE Uni = %s and Team_id = %s and Course_id = %s
        """
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(uni, team_id, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = "DELETE FROM teammate_db.StudentsInTeam WHERE Uni = %s  and Team_id = %s and Course_id = %s";
        cur.execute(sql2, args=(uni, team_id, course_id))
        return True

    @staticmethod
    def find_my_teammate(dept, timezone):
        sql = '''
        Select * From students_login_db.students_profile
        where timezone = %s and major = %s
        '''
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=(timezone, dept))
        result = cur.fetchall()
        return result
