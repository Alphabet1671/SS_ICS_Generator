import random
import datetime
from flask import *
from pdfminer.high_level import extract_text
import os

"""
lightsail push command:
aws lightsail push-container-image --service-name flask-service --label flask-container --image flask --region ca-central-1

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
        # Normal Day schedule
        ["081500", "081500"],
        ["091000", "091000"],
        ["103500", "103500"],
        ["115000", "122500"],
        ["132000", "132000"],
        ["141500", "141500"]
    ],
    [
        # Wednesday schedule
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
        # Normal schedule
        ["090500", "090500"],
        ["100500", "100500"],
        ["114500", "114500"],
        ["124000", "131500"],
        ["141000", "141000"],
        ["150000", "150000"]
    ],
    [
        # Wednesday schedule
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
    """
    OK this function is kinda poop, it would be better if startTime and endTime parameter can be passed through as dateTime object.
    
    This would require some changes in the startTimeMap and endTimeMap arrays.
    It would also need the complete restructure of the algorithm.
    
    """
    
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


app = Flask(__name__)

@app.route("/schedule-filler/")
def schedule_nav_page():
    return render_template("schedule-filler.html")


@app.route("/")
def index(): return render_template("index.html")


@app.route("/fill_schedule", methods=["POST", "GET"])
def fillSchedulePage():
    global studentSchedule
    global studentID
    global prevStudentID
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
                if studentSchedule.courseObj(i).name != "":
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

    try:
        os.remove(prevStudentID+".ics")
    except Exception as e:
        print(e)

    prevStudentID = studentID

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
        return send_file(fileName)
    except Exception as e:
        return str(e)


@app.route("/adv-filler-page/")
def adv_filler():
    return render_template("adv-schedule-filler.html")


@app.route("/send-adv-schedule/", methods=["POST", "GET"])
def send_adv_schedule():

    # Not completed backend!!!!
    advScheduleLst = [
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
    ]

    for day in range(0, 8):
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
            print(data)
    f.close()
    # Pulled cycle day schedule from file
    f = open(studentID_adv+"_schedule.ics", "w")

    for i in Heading:
        f.write(i+"\n")

    for day in cycleDays:
        for p in range(0, 6):
            print(day[1])
            if advScheduleLst[day[1]-1][p] != "":
                isWed = (day[0].strftime("%w") == "3")
                new_event(advScheduleLst[day[1]-1][p], StartTime(p+1, False, isWed), EndTime(p+1, True, isWed, False), "School", day[0], f)
    f.write("END:VCALENDAR")
    f.close()
    try:
        fileName = studentID_adv+"_schedule.ics"
        return send_file(fileName)
    except Exception as e:
        return str(e)

@app.route("/ocr-filler/")
def ocr_filler():
    return render_template("ocr-filler.html")

@app.route("/ocr-download/")
def download_ocr_file():
    try:
        fileName = "testICS.ics"
        return send_file(fileName)
    except Exception as e:
        return str(e)

@app.route("/send-ocr-schedule/", methods = ["POST","GET"])
def send_ocr_schedule():
    global prevStudentID
    if request.method == "POST":
        pdfFile = request.files["schedule-pdf"]
        pdfFile.save("temp.pdf")
        extractedText = extract_text("temp.pdf")
        extractedBlocks = extractedText.split("\n\n")
        extractedBlocks = extractedBlocks[20:40]

        blocksList = ["","","","","","","",""]  # order(0-7) ABCDEFGH
        locationList = ["","","","","","","",""]
        lateList = [0,0,0,0,0,0,0,0]


        for block in extractedBlocks:
            txt = block.replace("\n", " ")
            if txt[0:11] != "Unscheduled" and txt[0:9] != "Community":
                periodInfoStr = txt[txt.index("(")+8:txt.index(")")-1]
                currentBlockPeriod = ord(periodInfoStr[0])-ord("A")
                blocksList[currentBlockPeriod] = block.split("\n")[0].replace(":", "")
                locationList[currentBlockPeriod] = block[block.index(")")+1:len(block)].replace("\n","")
                print (locationList[currentBlockPeriod])
                if periodInfoStr[-1] == "L": lateList[currentBlockPeriod] = 1
                else: lateList[currentBlockPeriod] = 0

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

        print(cycleDayMap)

        f = open("testICS.ics", "w")


        for i in Heading:
            f.write(i + "\n")

        for day in cycleDayMap:
            periodLst = periodMap[int(day[1]) - 1]
            periodNum = 1
            if day[0].strftime("%w") == "3":
                isWed = 1
            else:
                isWed = 0
            for i in periodLst:
                j = ord(i)-ord("A")
                if blocksList[j] != "":
                    new_event(blocksList[j], StartTime(periodNum, lateList[j], isWed), EndTime(periodNum, lateList[j], isWed, 0), locationList[j], day[0], f)
                periodNum += 1

        f.write("END:VCALENDAR")


        return redirect("/ocr-download/")


@app.route("/upload-cycle-days/")
def upload_cycle_days():
    return render_template("cycle-days-upload.html")

@app.route("/write-cycle-days/", methods = ["POST","GET"])
def write_cycle_days():
    if request.method == "POST":
        txtFile = request.files["cycle-days-txt"]
        os.remove("blockSchedule.txt")
        txtFile.save("blockSchedule.txt")


    return redirect("/")

if __name__ == "__main__":
    app.run(port=2328, host="0.0.0.0", debug=True)
