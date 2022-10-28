import time
import pymysql


class DataBase(object):
    def __init__(self, database="lite_app") -> None:
        self.count = 0
        try:
            self.mysql = pymysql.connect(host='10.19.126.78',
                                         port=3307,
                                         user='root',
                                         password='catlab1a509',
                                         database=database)
        except Exception:
            time.sleep(2)
            self.__init__()

    def insert_download_mission(self, lite_app_id, full_app_id):
        insert_sql = "insert into " \
                     "download_mission(lite_app_id, full_app_id) " \
                     "values (%s, %s)"

        cursor = self.mysql.cursor()
        cursor.execute(insert_sql, (lite_app_id, full_app_id))
        cursor.close()
        self.mysql.commit()

    def update_lite_download_mission(self, lite_download, lite_app_id):
        update_sql = "update download_mission set lite_download= %s where lite_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (lite_download, lite_app_id))
        cursor.close()
        self.mysql.commit()

    def update_full_download_mission(self, full_download, full_app_id):
        update_sql = "update download_mission set full_download= %s where full_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (full_download, full_app_id))
        cursor.close()
        self.mysql.commit()

    def update_file_compare_by_lite_app_id(self, lite_app_id, compared):
        update_sql = "update download_mission set file_compared= %s where lite_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (compared, lite_app_id))
        cursor.close()
        self.mysql.commit()

    def update_permission_compare_by_lite_app_id(self, lite_app_id, compared):
        update_sql = "update download_mission set permission_compared= %s where lite_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (compared, lite_app_id))
        cursor.close()
        self.mysql.commit()

    def update_component_compare_by_lite_app_id(self, lite_app_id, compared):
        update_sql = "update download_mission set component_compared= %s where lite_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (compared, lite_app_id))
        cursor.close()
        self.mysql.commit()

    def update_method_compare_by_lite_app_id(self, lite_app_id, compared):
        update_sql = "update download_mission set method_compared= %s where lite_app_id= %s"
        cursor = self.mysql.cursor()
        cursor.execute(update_sql, (compared, lite_app_id))
        cursor.close()
        self.mysql.commit()

    def query_download_mission_by_full_app_id(self, full_app_id):
        query_sql = "select * from download_mission where full_app_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (full_app_id,))
        return cursor.fetchone()

    def query_download_mission_by_lite_app_id(self, lite_app_id):
        query_sql = "select * from download_mission where lite_app_id = %s"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql, (lite_app_id,))
        return cursor.fetchone()

    def query_download_mission(self):
        query_sql = "select * from download_mission"
        cursor = self.mysql.cursor()
        cursor.execute(query_sql)
        return cursor.fetchall()
