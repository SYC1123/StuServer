from socket import *
from time import ctime
import pymssql
import datetime
import json

from SQLServer import SQLServer


def chooseflag(info, sqlserver):
    # 选课权限
    '''
    :param info: 注册信息
    :param sqlserver: 数据库助手
    :return: 注册结果
    '''
    sql = 'select * from time '
    response = sqlserver.ExecQuery(sql)
    return str(response[0][1])


def stu_login(info, sqlserver):
    '''
    登录
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    account = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    sql = 'select * from student where student_id=%s ' % (account)
    response = sqlserver.ExecQuery(sql)
    if len(response) != 0:
        # 该用户存在
        # print(response)
        # print(response[0][4])
        if response[0][2] != info[1]:
            return '2'
        else:
            jsonData = []
            data = {}
            data['ID'] = str(response[0][0])
            data['Name'] = str(response[0][1])
            data['Password'] = str(response[0][2])
            data['Tel'] = str(response[0][3])
            data['Sex'] = str(response[0][4])
            data['Grade'] = int(response[0][5])
            data['College'] = str(response[0][6])
            sql = 'select major_name from major where major_id=%s ' % (str(response[0][7]))
            xx = sqlserver.ExecQuery(sql)
            data['major_name'] = str(xx[0][0])
            data['major_id'] = str(response[0][7])
            jsonData.append(data)
            jsondatar = json.dumps(jsonData, ensure_ascii=False)
            print(jsondatar)
            return jsondatar[1:len(jsondatar) - 1]
    else:
        return '3'


def office_login(info, sqlserver):
    '''
    教务处登录
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    account = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    sql = 'select * from office where office_id=%s ' % (account)
    response = sqlserver.ExecQuery(sql)
    if len(response) != 0:
        # 该用户存在
        print(response)
        # print(response[0][4])
        if response[0][1] != info[1]:
            return '2'
        else:
            jsonData = []
            data = {}
            data['ID'] = str(response[0][0])
            data['Password'] = str(response[0][1])
            data['College'] = str(response[0][2])
            jsonData.append(data)
            jsondatar = json.dumps(jsonData, ensure_ascii=False)
            print(jsondatar)
            return jsondatar[1:len(jsondatar) - 1]
    else:
        return '3'


def tea_login(info, sqlserver):
    '''
    教师登录
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    account = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    sql = 'select * from teacher where teacher_id=%s ' % (account)
    response = sqlserver.ExecQuery(sql)
    if len(response) != 0:
        # 该用户存在
        # print(response)
        # print(response[0][4])
        if response[0][3] != info[1]:
            return '2'
        else:
            jsonData = []
            data = {}
            data['ID'] = str(response[0][0])
            sql = 'select major_name from major where major_id=%s ' % (str(response[0][1]))
            xx = sqlserver.ExecQuery(sql)
            data['major_name'] = str(xx[0][0])
            data['Name'] = str(response[0][2])
            data['Password'] = str(response[0][3])
            data['Tel'] = str(response[0][4])
            data['Sex'] = str(response[0][5])
            data['College'] = str(response[0][6])
            data['major_id'] = str(response[0][1])
            jsonData.append(data)
            jsondatar = json.dumps(jsonData, ensure_ascii=False)
            print(jsondatar)
            return jsondatar[1:len(jsondatar) - 1]
    else:
        return '3'


def stu_change(info, sqlserver):
    '''
    学生修改信息
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    tel = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    stu_id = "'" + info[2] + "'"
    sql = "UPDATE student SET student_tel = %s,student_password= %s WHERE student_id = %s" % (tel, password, stu_id)
    sqlserver.ExecNonQuery(sql)
    return '修改成功！'


def tea_change(info, sqlserver):
    '''
    教师修改信息
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    tel = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    tea_id = "'" + info[2] + "'"
    sql = "UPDATE teacher SET teacher_tel = %s,teacher_password= %s WHERE teacher_id = %s" % (tel, password, tea_id)
    sqlserver.ExecNonQuery(sql)
    return '修改成功！'


def query_grade(info, sqlserver):
    '''
    查询成绩
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    stu_id = "'" + info[0] + "'"
    grade = int(info[1])
    sql = "select * from student_course where student_id=%s and sc_grade=%d" % (stu_id, grade)
    response = sqlserver.ExecQuery(sql)
    # print(response)
    jsonData = []
    for row in response:
        data = {}
        data['Stu_ID'] = str(row[0])
        data['Course_ID'] = row[1]
        sql = 'select course_name from course where course_id=%s ' % (str(row[1]))
        xx = sqlserver.ExecQuery(sql)
        data['course_name'] = str(xx[0][0])
        data['Score'] = row[2]
        sql = 'select course_credit from course where course_id=%s ' % (str(row[1]))
        xx = sqlserver.ExecQuery(sql)
        data['Grade'] = str(xx[0][0])
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(str(jsonData))
    return str(jsonData)


def query_course(info, sqlserver):
    '''
    查询课程
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    grade = int(info[0])
    major_id = "'" + (info[1]) + "'"
    sql = "select course.course_name,course.course_photo,course.course_credit," \
          "course.course_id,course.course_place,course.course_capacity," \
          "course.course_restcapacity,course.course_time,teacher_name from " \
          "course,major_course,teacher where course.course_id=major_course.course_id " \
          "and course.teacher_id=teacher.teacher_id and course.course_grade=%d and " \
          "major_course.major_id=%s and course.course_id not in (select course_id from student_course)" % (
              grade, major_id)
    response = sqlserver.ExecQuery(sql)
    print(response)
    jsonData = []
    for row in response:
        data = {}
        data['Course_name'] = str(row[0])
        data['Course_Photo'] = str(row[1])
        data['Course_Credit'] = row[2]
        data['Course_ID'] = str(row[3])
        data['Course_Place'] = str(row[4])
        data['Course_capacity'] = row[5]
        data['Course_restcapacity'] = row[6]
        data['Course_Time'] = str(row[7])
        data['Teacher_name'] = str(row[8])
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(str(jsonData))
    return str(jsonData)


def choose_course(info, sqlserver):
    '''
    选课
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[0] + "'"
    stu_id = "'" + info[1] + "'"
    grade = int(info[2]) + 1
    num = int(info[3]) - 1
    sql = "UPDATE course SET course_restcapacity = %d WHERE course_id = %s" % (num, course_id)
    sqlserver.ExecNonQuery(sql)
    sql = '''insert into student_course(student_id,course_id,sc_grade) values (%s,%s,%d)''' % (stu_id, course_id, grade)
    print(sql)
    sqlserver.ExecNonQuery(sql)
    return "选课成功！"


def get_teacourse(info, sqlserver):
    '''
    查看教师授课
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    tea_id = "'" + (info[0]) + "'"
    sql = "select * from course where Teacher_ID=%s" % (tea_id)
    response = sqlserver.ExecQuery(sql)
    print(response)
    jsonData = []
    for row in response:
        data = {}
        data['Course_ID'] = str(row[0])
        data['Course_name'] = str(row[2])
        data['Course_Credit'] = row[5]
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(str(jsonData))
    return str(jsonData)


def get_teastu(info, sqlserver):
    '''
    查询选该课的学生
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + (info[0]) + "'"
    sql = "select * from student_course where course_id=%s and  SC_Result is null" % course_id
    response = sqlserver.ExecQuery(sql)
    print(response)
    jsonData = []
    for row in response:
        data = {}
        data['Stu_ID'] = str(row[0])
        data['Course_ID'] = str(row[1])
        sql = 'select student_name from student where student_id=%s ' % (str(row[0]))
        xx = sqlserver.ExecQuery(sql)
        data['Stu_Name'] = str(xx[0][0])
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(str(jsonData))
    return str(jsonData)


def input_score(info, sqlserver):
    '''
    输入成绩
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[1] + "'"
    stu_id = "'" + info[0] + "'"
    grade = float(info[2])
    sql = "UPDATE student_course SET sc_result = %f WHERE student_id=%s and course_id = %s" % (grade, stu_id, course_id)
    sqlserver.ExecNonQuery(sql)
    return "录入成功！"


def get_teachecourse(info, sqlserver):
    '''
    查看教师授课
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    tea_id = "'" + (info[0]) + "'"
    sql = "select * from course where teacher_id=%s" % tea_id
    response = sqlserver.ExecQuery(sql)
    print(response)
    jsonData = []
    for row in response:
        data = {}
        data['Course_name'] = str(row[2])
        data['Course_Photo'] = str(row[9])
        data['Course_Credit'] = row[5]
        data['Course_ID'] = str(row[0])
        data['Course_Place'] = str(row[6])
        data['Course_capacity'] = row[7]
        data['Course_restcapacity'] = row[8]
        data['Course_Time'] = str(row[10])
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
    print(str(jsonData))
    return str(jsonData)


def change_score(info, sqlserver):
    '''
    教务处修改学生成绩
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[1] + "'"
    stu_id = "'" + info[0] + "'"
    grade = float(info[2])
    sql = "select * from student_course WHERE student_id=%s and course_id = %s" % (stu_id, course_id)
    response = sqlserver.ExecQuery(sql)
    if len(response) == 0:
        return '1'
    else:
        sql = "UPDATE student_course SET sc_result = %f WHERE student_id=%s and course_id = %s" % (
            grade, stu_id, course_id)
        sqlserver.ExecNonQuery(sql)
        return "修改成功！"


def flag(info, sqlserver):
    '''
    选课控制
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    flag = int(info[0])
    sql = "UPDATE time SET time = %d WHERE time_id=1" % flag
    sqlserver.ExecNonQuery(sql)
    return "录入成功！"


def del_course(info, sqlserver):
    '''
    教务处删除课程
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[0] + "'"
    sql = "select * from course WHERE course_id=%s " % course_id
    response = sqlserver.ExecQuery(sql)
    if len(response) == 0:
        return '1'
    else:
        sql = "DELETE FROM course WHERE course_id = %s " % course_id
        sqlserver.ExecNonQuery(sql)
        return '删除成功！'


def get_course(info, sqlserver):
    '''
    得到要修改的课程信息
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[0] + "'"
    sql = "select * from course WHERE course_id=%s " % course_id
    response = sqlserver.ExecQuery(sql)
    print(response)
    if len(response) == 0:
        return '1'
    else:
        jsonData = []
        data = {}
        data['ID'] = str(response[0][0])
        data['Teacher_ID'] = str(response[0][1])
        data['Course_name'] = str(response[0][2])
        data['Grade'] = str(response[0][3])
        data['Course_Credit'] = str(response[0][5])
        data['Course_Place'] = str(response[0][6])
        data['Course_capacity'] = str(response[0][7])
        data['Course_restcapacity'] = str(response[0][8])
        data['Course_Time'] = str(response[0][10])
        jsonData.append(data)
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
        print(jsondatar)
        return jsondatar[1:len(jsondatar) - 1]


def change(info, sqlserver):
    '''
    修改课程信息
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[0] + "'"
    tea_id = "'" + info[1] + "'"
    c_name = "'" + info[2] + "'"
    grade = int(info[3])
    credit = int(info[4])
    place = "'" + info[5] + "'"
    cap = int(info[6])
    time = "'" + info[7] + "'"
    sql = "select * from teacher WHERE teacher_id = %s" % tea_id
    response = sqlserver.ExecQuery(sql)
    if len(response) == 0:
        return '1'
    else:
        sql = "UPDATE course SET teacher_id=%s,course_name=%s,course_grade=%d," \
              "course_credit=%d,course_place=%s,course_capacity=%d,course_restcapacity=%d," \
              "course_time=%s WHERE  course_id = %s" % (tea_id, c_name, grade, credit, place, cap, cap, time, course_id)
        sqlserver.ExecNonQuery(sql)
        return "修改成功！"


def add(info, sqlserver):
    '''
    添加课程
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    course_id = "'" + info[0] + "'"
    tea_id = "'" + info[1] + "'"
    c_name = "'" + info[2] + "'"
    grade = int(info[3])
    credit = int(info[4])
    place = "'" + info[5] + "'"
    cap = int(info[6])
    time = "'" + info[7] + "'"
    url = "'" + info[8] + "'"
    sql = "select * from teacher WHERE teacher_id = %s" % tea_id
    response = sqlserver.ExecQuery(sql)
    if len(response) == 0:
        return '1'
    else:
        sql = "select * from course WHERE course_id = %s" % course_id
        response = sqlserver.ExecQuery(sql)
        if len(response) != 0:
            return '2'
        else:
            sql = "insert into course (course_id, teacher_id,course_name,course_grade," \
                  "course_nature,course_credit,course_place,course_capacity,course_restcapacity," \
                  "course_photo,course_time) values (%s,%s,%s,%d,%d,%d,%s,%d,%d,%s,%s) " % (
                  course_id, tea_id, c_name, grade, 1, credit, place, cap, cap, url, time)
            print(sql)
            sqlserver.ExecNonQuery(sql)
            return "添加成功！"


def chang_pass(info, sqlserver):
    '''
    教务处改密码
    :param info:
    :param sqlserver:
    :return:
    '''
    info = info.split("&")
    off_id = "'" + info[0] + "'"
    password = "'" + info[1] + "'"
    sql = "UPDATE office SET office_password = %s WHERE office_id = %s" % (password, off_id)
    sqlserver.ExecNonQuery(sql)
    return '修改成功！'


if __name__ == '__main__':
    sqlserver = SQLServer('(local)', 'sa', '874795069syc', 'Student')
    # 1 定义域名和端口号
    HOST, POST = '', 6666
    # 2 定义缓冲区大小 缓存输入或输出的大小，为了解决速度不匹配的问题
    BUFFER_SIZE = 1024
    ADDR = (HOST, POST)
    # 3 创建服务器的套接字 AF_INET:IPV4 SOCK_STREAM:协议
    tcpServerSocket = socket(AF_INET, SOCK_STREAM)
    # 4 绑定域名和端口号
    tcpServerSocket.bind(ADDR)
    # 5 监听连接，最大连接数一般默认5，如果服务器高并发则增大
    tcpServerSocket.listen(5)  # 被动等待连接
    print('服务器创建成功，等待客户端连接。。。。。')
    while True:
        # 6.1 打开一个客户端对象 同意你连接
        tcpCilentSocket, addr = tcpServerSocket.accept()
        print('连接服务器的客户端对象', addr)
        # 6.2循环过程
        while True:
            # 6.3拿到数据recv()从缓冲区读取指定长度的数据
            # decode(）解码bytes——>str  encode()——>编码 str——>bytes
            data = tcpCilentSocket.recv(BUFFER_SIZE).decode()
            result = None
            if not data:
                break
            print('data=', data)
            command = data[:data.find(':')]
            if command == 'stu_login':
                info = data[data.find(':') + 1:]
                result = stu_login(info, sqlserver)
            elif command == 'office_login':
                info = data[data.find(':') + 1:]
                result = office_login(info, sqlserver)
            elif command == 'tea_login':
                info = data[data.find(':') + 1:]
                result = tea_login(info, sqlserver)
            elif command == 'stu_change':
                info = data[data.find(':') + 1:]
                result = stu_change(info, sqlserver)
            elif command == 'tea_change':
                info = data[data.find(':') + 1:]
                result = tea_change(info, sqlserver)
            elif command == 'query_grade':
                info = data[data.find(':') + 1:]
                result = query_grade(info, sqlserver)
            elif command == 'query_course':
                info = data[data.find(':') + 1:]
                result = query_course(info, sqlserver)
            elif command == 'check':
                result = chooseflag("", sqlserver)
            elif command == 'choose_course':
                info = data[data.find(':') + 1:]
                result = choose_course(info, sqlserver)
            elif command == 'get_teacourse':
                info = data[data.find(':') + 1:]
                result = get_teacourse(info, sqlserver)
            elif command == 'get_teastu':
                info = data[data.find(':') + 1:]
                result = get_teastu(info, sqlserver)
            elif command == 'input_score':
                info = data[data.find(':') + 1:]
                result = input_score(info, sqlserver)
            elif command == 'get_teachecourse':
                info = data[data.find(':') + 1:]
                result = get_teachecourse(info, sqlserver)
            elif command == 'change_score':
                info = data[data.find(':') + 1:]
                result = change_score(info, sqlserver)
            elif command == 'flag':
                info = data[data.find(':') + 1:]
                result = flag(info, sqlserver)
            elif command == 'del_course':
                info = data[data.find(':') + 1:]
                result = del_course(info, sqlserver)
            elif command == 'get_course':
                info = data[data.find(':') + 1:]
                result = get_course(info, sqlserver)
            elif command == 'change':
                info = data[data.find(':') + 1:]
                result = change(info, sqlserver)
            elif command == 'add':
                info = data[data.find(':') + 1:]
                result = add(info, sqlserver)
            elif command == 'chang_pass':
                info = data[data.find(':') + 1:]
                result = chang_pass(info, sqlserver)
            # 6.4 发送时间还有信息
            tcpCilentSocket.send(result.encode())
        # 7 关闭资源
        tcpCilentSocket.close()
    tcpServerSocket.close()
