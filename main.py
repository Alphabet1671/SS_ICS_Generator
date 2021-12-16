import random
import datetime
from flask import *

"""aws push command:
aws lightsail push-container-image --service-name flask-service --label flask-container --image flask
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json
"""


periodMap = [
    ["A", "B", "C", "D", "E", "F"],
    ["G", "D", "E", "H", "A", "B"],
    ["F", "H", "A", "C", "G", "D"],
    ["B", "C", "G", "E", "F", "H"],
    ["D", "E", "F", "A", "B", "C"],
    ["H", "A", "B", "G", "D", "E"],
    ["C", "G", "D", "F", "H", "A"],
    ["E", "F", "H", "B", "C", "G"]
]

"""for these two maps, index 0 is for regular day and index 1 is for wednesdays"""
startTimeMap = [
    [
        ["081500", "081500"],
        ["091000", "091000"],
        ["100500", "100500"],
        ["115000", "122500"],
        ["132000", "132000"],
        ["141500", "141500"]
    ],
    [
        ["093500", "093500"],
        ["103000", "103000"],
        ["112500", "112500"],
        ["122000", "124500"],
        ["134000", "134000"],
        ["143500", "143500"]
    ]
]
endTimeMap = [
    [
        ["090500", "090500"],
        ["100500", "100500"],
        ["114500", "114500"],
        ["124000", "131500"],
        ["141000", "141000"],
        ["150000", "150000"]
    ],
    [
        ["102500", "102500"],
        ["112000", "112000"],
        ["121500", "121500"],
        ["131000", "133500"],
        ["143000", "143000"],
        ["152500", "152500"]
    ]
]


class Course:
    def __init__(self, name_, block_, lab_, late_):
        self.name = name_
        self.block = block_
        self.lab = lab_
        self.late = late_


class StudentSchedule:
    def __init__(self, StudentID_, A_, B_, C_, D_, E_, F_, G_, H_):
        self.studentID = StudentID_
        self.A = A_
        self.B = B_
        self.C = C_
        self.D = D_
        self.E = E_
        self.F = F_
        self.G = G_
        self.H = H_

    def courseObj(self, label):
        if label == "A": return self.A
        if label == "B": return self.B
        if label == "C": return self.C
        if label == "D": return self.D
        if label == "E": return self.E
        if label == "F": return self.F
        if label == "G": return self.G
        if label == "H": return self.H


ScheduleForLouis = StudentSchedule(
    "189716",
    Course("Art of Persuasion", "A", False, True),
    Course("Adv. Physics", "B", True, True),
    Course("Free", "C", False, True),
    Course("US History", "D", False, False),
    Course("Latin I", "E", False, False),
    Course("Symphonic Band", "F", False, False),
    Course("Free", "G", False, True),
    Course("Multi-Variable Calc", "H", False, True)
)


def StartTime(index, late, wed):
    return startTimeMap[int(wed)][index - 1][int(late)]


def EndTime(index, late, wed, lab):
    if (index == 1 or index == 4) and (lab == True):
        return endTimeMap[int(wed)][index][int(late)]
    else:
        return endTimeMap[int(wed)][index - 1][int(late)]


def period(day, period_):
    return periodMap[day][period_]


def random_UID():
    a = random.randint(0, 100000)
    b = hex(random.randint(0, 65535))[2:]
    c = hex(random.randint(0, 65535))[2:]
    d = hex(random.randint(0, 65535))[2:]
    return "4F2F7F11-" + str(d) + "-" + str(c) + "-" + str(b) + "-6634746" + str(a)


def new_event(name, startTime, endTime, location, t, f):
    year = t.strftime("%Y")
    month = t.strftime("%m")
    day = t.strftime("%d")
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    second = t.strftime("%S")

    f.write("BEGIN:VEVENT")
    f.write("\n")
    f.write('TRANSP:OPAQUE')
    f.write('\n')
    f.write("DTEND;TZID=America/New_York:{}{}{}T{}".format(year, month, day, endTime))
    f.write('\n')
    f.write('UID:{}'.format(random_UID()))
    f.write('\n')
    f.write('DTSTAMP:20210903T163112Z')
    f.write('\n')
    f.write("LOCATION:{}".format(location))
    f.write("\n")
    f.write("URL;VALUE=URI:")
    f.write("\n")
    f.write("SEQUENCE:0")
    f.write("\n")
    f.write('X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC')
    f.write('\n')
    f.write('SUMMARY:{}'.format(name))
    f.write('\n')
    f.write('LAST-MODIFIED:{}{}{}T{}{}{}Z'.format(year, month, day, hour, minute, second))
    f.write('\n')
    f.write("CREATED:{}{}{}T{}{}{}Z".format(year, month, day, hour, minute, second))
    f.write("\n")
    f.write('DTSTART;TZID=America/New_York:{}{}{}T{}'.format(year, month, day, startTime))
    f.write('\n')
    f.write('BEGIN:VALARM')
    f.write('\n')
    f.write('X-WR-ALARMUID:{}'.format(random_UID()))
    f.write('\n')
    f.write("UID:{}".format(random_UID()))
    f.write("\n")
    f.write("DESCRIPTION:Reminder")
    f.write("\n")
    f.write("ACKNOWLEDGED:20210903T163112Z")
    f.write("\n")
    f.write('TRIGGER:-PT5M')
    f.write('\n')
    f.write("ACTION:DISPLAY")
    f.write("\n")
    f.write('END:VALARM')
    f.write('\n')
    f.write('END:VEVENT')
    f.write('\n')


def isChecked(str):
    if str == "True":
        return True
    else:
        return False


global studentSchedule

Heading = ['BEGIN:VCALENDAR',
           'METHOD:PUBLISH',
           'VERSION:2.0',
           'X-WR-CALNAME:SSA Calendar',
           "PRODID:-//Apple Inc.//macOS 11.5.2//EN",
           'X-APPLE-CALENDAR-COLOR:#34AADC',
           'X-WR-TIMEZONE:America/New_York',
           "CALSCALE:GREGORIAN",
           "BEGIN:VTIMEZONE",
           "TZID:America/New_York",
           "BEGIN:DAYLIGHT",
           "TZOFFSETFROM:-0500",
           "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU",
           "DTSTART:20070311T020000",
           "TZNAME:EDT",
           "TZOFFSETTO:-0400",
           "END:DAYLIGHT",
           "BEGIN:STANDARD",
           "TZOFFSETFROM:-0400",
           "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU",
           "DTSTART:20071104T020000",
           "TZNAME:EST",
           "TZOFFSETTO:-0500",
           "END:STANDARD",
           "END:VTIMEZONE"
           ]

"""
Initializing the cycle day map

This is to match cycle day with a datetime object.

remember to adjust for years!!!

"""

app = Flask(__name__)
global studentID

@app.route("/schedule-filler/")
def schedule_nav_page():
    return render_template("schedule-filler.html")


@app.route("/")
def index(): return render_template("index.html")


@app.route("/fill_schedule", methods=["POST", "GET"])
def fillSchedulePage():
    global studentSchedule
    if request.method == "POST":
        studentID = request.form["studentID"]
        blockA = Course(request.form["blockA"], "A", isChecked(request.form.get("blockAlab", False)),
                        isChecked(request.form.get("blockAlate", False)))
        blockB = Course(request.form["blockB"], "B", isChecked(request.form.get("blockBlab", False)),
                        isChecked(request.form.get("blockBlate", False)))
        blockC = Course(request.form["blockC"], "C", isChecked(request.form.get("blockClab", False)),
                        isChecked(request.form.get("blockClate", False)))
        blockD = Course(request.form["blockD"], "D", isChecked(request.form.get("blockDlab", False)),
                        isChecked(request.form.get("blockDlate", False)))
        blockE = Course(request.form["blockE"], "E", isChecked(request.form.get("blockElab", False)),
                        isChecked(request.form.get("blockElate", False)))
        blockF = Course(request.form["blockF"], "F", isChecked(request.form.get("blockFlab", False)),
                        isChecked(request.form.get("blockFlate", False)))
        blockG = Course(request.form["blockG"], "G", isChecked(request.form.get("blockGlab", False)),
                        isChecked(request.form.get("blockGlate", False)))
        blockH = Course(request.form["blockH"], "H", isChecked(request.form.get("blockHlab", False)),
                        isChecked(request.form.get("blockHlate", False)))
        studentSchedule = StudentSchedule(studentID, blockA, blockB, blockC, blockD, blockE, blockF, blockG, blockH)

        print(studentSchedule)
        cycleDayMap = []
        f = open("blockSchedule.txt", "r")
        currentTime = datetime.datetime.now()
        for lineTxt in f:
            txt = lineTxt.split("+")
            if txt[0] != "\n":
                timeObj = datetime.datetime.strptime(txt[0], "%A,%b%d").replace(year=currentTime.year)
                data = [timeObj, txt[1]]
                cycleDayMap.append(data)

        f.close()

        dateLst = []
        courseNameLst = []
        startTimeLst = []
        endTimeLst = []

        for day in cycleDayMap:
            periodLst = periodMap[int(day[1]) - 1]
            periodNum = 1
            if day[0].strftime("%w") == "3":
                isWed = 1
            else:
                isWed = 0
            for i in periodLst:
                if studentSchedule.courseObj(i).name != "Free":
                    dateLst.append(day[0])
                    courseNameLst.append(studentSchedule.courseObj(i).name)
                    startTimeLst.append(StartTime(periodNum, studentSchedule.courseObj(i).late, isWed))
                    endTimeLst.append(
                        EndTime(periodNum, studentSchedule.courseObj(i).late, isWed, studentSchedule.courseObj(i).lab))
                    print(str(day[0]) + "=" + studentSchedule.courseObj(i).name + "=" + str(periodNum) + "\n")
                periodNum += 1

        f = open(studentSchedule.studentID + "_schedule.ics", "w")
        for i in Heading:
            f.write(i + "\n")

        for i in range(len(dateLst)):
            new_event(courseNameLst[i], startTimeLst[i], endTimeLst[i], "School", dateLst[i], f)

        f.write("END:VCALENDAR")

    return redirect("/file_download", 302)


@app.route("/file_download")
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e)


@app.route("/return-files/")
def sendFile():
    try:
        fileName = studentID+"_schedule.ics"
        return send_file(fileName, attachment_filename="Your Schedule.ics")
    except Exception as e:
        return str(e)


@app.route("/adv-filler-page/")
def adv_filler():
    return render_template("adv-schedule-filler.html")


@app.route("/send-adv-schedule/", methods=["POST", "GET"])
def send_adv_schedule():

    # Not completed backend!!!!
    advScheduleLst = [
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
    ]

    for day in range(0, 7):
        for prd in range(0, 6):
            inputId = "day-"+str(day+1)+"-period-"+str(prd+1)+"-in"
            advScheduleLst[day][prd] = request.form[inputId]
    studentID_adv = request.form["stu-id-in"]
    # Input processing wrote into 2D lst
    cycleDays = []
    f = open("blockSchedule.txt", "r")
    currentTime = datetime.datetime.now()
    for lineTxt in f:
        txt = lineTxt.split("+")
        if txt[0] != "\n":
            timeObj = datetime.datetime.strptime(txt[0], "%A,%b%d").replace(year=currentTime.year)
            data = [timeObj, int(txt[1])]
            cycleDays.append(data)
    f.close()
    # Pulled cycle day schedule from file
    f = open(studentID_adv+"_schedule.ics", "w")
    for day in cycleDays:
        for p in range(0, 6):
            if advScheduleLst[day[1]-1][p] != "":
                new_event(advScheduleLst[day[1]-1][p], StartTime(p, False, False), EndTime(p, False, False, False), "School", day[0], f) #Need adjustment for Weds
    f.write("END:VCALENDAR")
    f.close()
    try:
        fileName = studentID_adv+"_schedule.ics"
        return send_file(fileName, attachment_filename="Your Schedule.ics")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)
