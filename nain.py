import subprocess, re, random, os, sys, pymediainfo

videoPath = 'C:\\yt-dlp\\1\\imkaza.mp4'
edPath = 'C:\\yt-dlp\\1\\imkazaed.mp4'
cutPath = 'C:\\yt-dlp\\1\\imkazacut.mp4'
revPath = 'C:\\yt-dlp\\1\\imkazarev.mp4'
prepPath = 'C:\\yt-dlp\\1\\imkazarprep.mp4'
vlistpath = 'C:\\yt-dlp\\1\\full.ts'
vlistpath = 'C:\\yt-dlp\\1\\vlist.txt'
ffmpegfname = 'ffmpeg.exe'
ffprobefname = 'ffprobe.exe'
volvalmin = 0
volvalmaxp = 400
volvalmaxd = 5


# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def getos():
    if 'posix' == os.name:
        retstr = os.system("uname -a")
    else:
        retstr = sys.platform
    return retstr


def isAudio(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Audio' == track.track_type:
            return True
    return  False


def isVideo(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Video' == track.track_type:
            return True
    return  False


def isImage(filepath: str):
    if not os.path.exists(filepath):
        return False
    fileInfo = pymediainfo.MediaInfo.parse(filepath)
    for track in fileInfo.tracks:
        if 'Image' == track.track_type:
            return True
    return False


def convStr2Int(convstr: str):
    try:
        convval = int(convstr)
        return convval
    except ValueError:
        return None


def convStr2Float(convstr: str):
    try:
        convval = float(convstr)
        return convval
    except ValueError:
        return None


def isTime(teststr: str):
    if len(teststr) == 0:
        return  False
    if re.match('\d\d:\d\d:\d\d', teststr):
        testhrs = int(teststr[:1])
        if testhrs > 23:
            return False
        else:
            testmin = convStr2Int(teststr[3:4])
            testsec = convStr2Int(teststr[6:7])
            if testmin is None or testsec is None or testmin > 59 or testsec > 59:
                return False
            else:
                return True
    elif re.match('\d\d', teststr):
        testdur = convStr2Int(teststr[:1])
        if testdur > 59:
            return False
        else:
            return True
    elif re.match('\d\d.[\d]+', teststr) or re.match('\d.[\d]+', teststr):
        testdur = convStr2Float(teststr)
        if testdur is None or testdur > 59:
            return False
        else:
            return True
    elif len(teststr) == 1 and teststr.isdigit():
        testdur = convStr2Int(teststr)
        if testdur is None or testdur > 59:
            return False
        else:
            return True
    else:
        return False


def getmediaduration(mp3filename: str):
    global ffprobefname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if mp3filename == '':
        colorprint.out('PATH TO MP3 FILE IS EMPTY')
        return None
    if not os.path.exists(mp3filename):
        colorprint.out('PATH TO MP3 FILE DOES NOT EXIST')
        return None
    subarglist = [ ffprobefname, '-show_entries', 'format=duration','-i',mp3filename ]
    popen  = subprocess.Popen(subarglist, stdout = subprocess.PIPE)
    popen.wait()
    output = str(popen.stdout.read())
    if len(output) > 0 and '\\r\\n' in output:
        return output.split('\\r\\n')[1][9:]
    else:
        return None


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def videoList2TextFile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
        f.close()
    return True


def audioList2textfile(filename: str, datalist: list):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if os.path.exists(filename):
        colorprint.out('REQUESTED OBJECT (' + filename + ') IS ALREADY PRESENT IN THE SYSTEM')
        return False
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('ffconcat version 1.0\n\n')
        for line in datalist:
            # fline = 'file "' + line.replace('\\', '\\\\').replace(' ', '\\ ') + '"\n'
            flieln = 'file ' + line.replace('\\', '\\\\').replace('\'', '\\\'').replace(' ', '\\ ') + '\n'
            f.write(flieln)
        f.close()
    return True


def videoCutPart(videoPath: str, targetPath: str, startTime: str = '0', duration: str = '30',
                 splitStartTime: bool = False, includeAudio: bool = False, useCopyCodec: bool = False):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(videoPath):
        colorprint.out('REQUESTED FILE DOES NOT EXIST')
        return False
    if len(targetPath) == 0:
        colorprint.out('TARGET PATH INCORRECT')
        return False
    if not os.path.exists(os.path.dirname(targetPath)):
        colorprint.out('TARGET PATH DIRECTORY NAME INCORRECT')
        return False
    if useCopyCodec:
        if splitStartTime:
            startTimemod = convStr2Float(startTime)
            if startTime is None:
                return  False
            startTimemod *= 0.9
            startTimediff = startTime - startTimemod
            if includeAudio:
                arglist = [ ffmpegfname,
                            '-y',
                            '-ss',
                            str(startTimemod),
                            '-i',
                            videoPath,
                            '-ss',
                            str(startTimediff),
                            '-t',
                            duration,
                            '-acodec',
                            'copy',
                            '-vcodec',
                            'copy',
                            targetPath ]
            else:
                arglist = [ ffmpegfname,
                            '-y',
                            '-ss',
                            str(startTimemod),
                            '-i',
                            videoPath,
                            '-ss',
                            str(startTimediff),
                            '-t',
                            duration,
                            '-codec',
                            'copy',
                            targetPath ]
        else:
            if includeAudio:
                arglist = [ ffmpegfname,
                            '-y',
                            '-ss',
                            startTime,
                            '-i',
                            videoPath,
                            '-t',
                            duration,
                            '-acodec',
                            'copy',
                            '-vcodec',
                            'copy',
                            targetPath ]
            else:
                arglist = [ ffmpegfname,
                            '-ss',
                            '-y',
                            startTime,
                            '-i',
                            videoPath,
                            '-t',
                            duration,
                            '-codec',
                            'copy',
                            targetPath ]
    else:
        if splitStartTime:
            startTimemod = convStr2Float(startTime)
            if startTime is None:
                return False
            startTimemod *= 0.9
            startTimediff = startTime - startTimemod
            if includeAudio:
                arglist = [ ffmpegfname,
                            '-y',
                            '-ss',
                            str(startTimemod),
                            '-i',
                            videoPath,
                            '-ss',
                            str(startTimediff),
                            '-t',
                            duration,
                            '-acodec',
                            'copy',
                            targetPath ]
            else:
                arglist = [ ffmpegfname,
                            '-y',
                            '-ss',
                            str(startTimemod),
                            '-i',
                            videoPath,
                            '-ss',
                            str(startTimediff),
                            '-t',
                            duration,
                            targetPath ]
        else:
            arglist = [ ffmpegfname,
                        '-y',
                        '-ss',
                        startTime,
                        '-i',
                        videoPath,
                        '-t',
                        duration,
                        targetPath ]
    subprocess.run(arglist)
    if os.path.exists(targetPath) and isVideo(targetPath):
        return True
    else:
        return False



def videoReverse(videoPath: str, targetPath: str, inckudeAudio: bool = False):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(videoPath):
        colorprint.out('REQUESTED FILE DOES NOT EXIST')
        return False
    if len(targetPath) == 0:
        colorprint.out('TARGET PATH INCORRECT')
        return False
    if not os.path.exists(os.path.dirname(targetPath)):
        colorprint.out('TARGET PATH DIRECTORY NAME INCORRECT')
        return False
    if inckudeAudio:
        arglist = [ ffmpegfname,
                    '-y',
                    '-i',
                    videoPath,
                    '-vf',
                    ' reverse',
                    '-af',
                    'areverse',
                    targetPath ]
    else:
        arglist = [ ffmpegfname,
                    '-y',
                    '-i',
                    videoPath,
                    '-vf',
                    ' reverse',
                    targetPath ]
    subprocess.run(arglist)
    if os.path.exists(targetPath) and isVideo(targetPath):
        return True
    else:
        return False



def videoRemoveAudio(videoPath: str, targetPath: str):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(videoPath):
        colorprint.out('REQUESTED FILE DOES NOT EXIST')
        return False
    if len(targetPath) == 0:
        colorprint.out('TARGET PATH INCORRECT')
        return False
    if not os.path.exists(os.path.dirname(targetPath)):
        colorprint.out('TARGET PATH DIRECTORY NAME INCORRECT')
        return False
    arglist = [ ffmpegfname, '-y' ]
    arglist.append('-i')
    arglist.append(videoPath)
    arglist.append('-c')
    arglist.append('copy')
    arglist.append('-an')
    arglist.append(targetPath)
    subprocess.run(arglist)
    return os.path.exists(targetPath) and isVideo(targetPath)


def videoConvertToTS(vidlist: list):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if len(vidlist) == 0:
        colorprint.out('EMPTY VIDEO LIST SPECIFIED')
        return None
    convlist = []
    for vid in vidlist:
        if not os.path.exists(vid):
            colorprint.out('"'+ vid + '": PATH DOES NOT EXIST')
            continue
        tsname = ( '.'.join((vid[::-1].split('.'))[1:]))[::-1] + '.ts'
        arglist = [ ffmpegfname,
                    '-y',
                    '-i',
                    vid,
                    '-c',
                    'copy',
                    '-bsf:v',
                    'h264_mp4toannexb',
                    '-f',
                    'mpegts',
                    tsname ]
        subprocess.run(arglist)
        if os.path.exists(tsname) and isVideo(tsname):
            convlist.append(tsname)
    return convlist


# cmd
# ffmpeg -i <in> -filter:a "volume=6" <out>
def mediaChangeVolume(mediaPath: str, volVal: float, volMetrics:str = 'percent'):
    global ffmpegfname
    global volvalmin
    global volvalmaxp
    global volvalmaxd
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    volstr = ''
    if not os.path.exists(mediaPath):
        colorprint.out('REQUESTED FILE DOES NOT EXIST')
        return False
    if volvalmin > volVal:
        colorprint.out('VOLUME VALUE TOO LOW')
        return False
    elif volvalmaxp < volVal and 'percent' == volMetrics.lower():
        colorprint.out('VOLUME VALUE TOO HIGH')
        return False
    elif volvalmaxd < volVal and 'db' == volMetrics.lower():
        colorprint.out('VOLUME VALUE TOO HIGH')
        return False
    elif not 'percent' == volMetrics.lower() and 'db' == volMetrics.lower():
        colorprint.out('INCORRECT VOLUME VALUE METRICS')
        return False
    outpath = os.path.dirname(mediaPath)
    mpspl = os.path.splitext(mediaPath)
    outpath += os.path.sep + 'out.webm' # mpspl[1]
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                mediaPath,
                '-vcodec',
                'copy',
                '-filter:a',
                'volume=' + str(volVal),
                outpath ]
    subprocess.run(arglist)
    if os.path.exists(outpath) and (isVideo(outpath) or isAudio(outpath)):
        return True
    else:
        return False


def videoMerge(outFName: str, vidlist: list, doConversion: bool = True): # videolistFName:str):
    global ffmpegfname
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    concatstr = ''
    vidlistChecked = []
    if doConversion:
        for vid in vidlist:
            if not os.path.exists(vid):
                colorprint.out('FILE ' + vid + ' DOES BOT EXIST')
                continue
            vidlistChecked.append(vid)
        convres = videoConvertToTS(vidlistChecked)
        if convres is None or len(convres) == 0:
            colorprint.out('CONVERSION FAILED')
            return False
        concatstr = 'concat:' + '|'.join(convres)
    arglist = [ ffmpegfname,
                '-y',
                concatstr,
                '-codec',
                'copy',
                outFName ]
    subprocess.run(arglist)
    if os.path.exists(outFName) and isVideo(outFName):
        return True
    else:
        return False


def video2MP3(filename: str, ourputFName: str):
    global ffmpegfname
    if not os.path.exists(filename) or not isVideo(filename):
        return False
    if len(ourputFName) == 0:
        return False
    arglist = [ ffmpegfname,
                '-y',
                '-i',
                filename,
                '-b:a',
                '320k',
                '-vn',
                ourputFName ]
    subprocess.run(arglist)
    if os.path.exists(ourputFName) and isAudio(ourputFName):
        return True
    else:
        return False


def videoConvert(filename: str, outfilename: str):
    global ffmpegfname
    if not os.path.exists(filename) or not isVideo(filename):
        return False
    arglist = [ ffmpegfname,
                '-c:a',
                'copy',
                outfilename ]
    subprocess.run(arglist)
    if os.path.exists(outfilename) and isAudio(outfilename):
        return True
    else:
        return False


######### SCRIPT #########
if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    scriptdir = get_script_path()
    ffmpegfname = scriptdir + os.path.sep + ffmpegfname
    if not os.path.exists(ffmpegfname):
        colorprint.out('FFMPEG EXECUTABLE DOES NOT EXIST')
        systemExitCode = 1
        sys.exit(systemExitCode)
    ffprobefname =  scriptdir + os.path.sep+ ffprobefname
    if not os.path.exists(ffprobefname):
        colorprint.out('FFPROBE EXECUTABLE DOES NOT EXIST')
        systemExitCode = 2
        sys.exit(systemExitCode)
    if not mediaChangeVolume (mediaPath='C:\\yt-dlp\\Превращаем модуль ядра в драйвер символьного устройства.webm',
                              volVal=8):
        colorprint.out('COULD CHANGE MEDIA VOLUME')
        systemExitCode = 2
        sys.exit(systemExitCode)
    video2MP3("C:\\Users\\admin\\Downloads\\Haunted.mp4",
              "C:\\Users\\admin\\Downloads\\Poe - Haunted.mp3")
    videolist = [ cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath,
                  cutPath,
                  revPath ]
    if not videoMerge(prepPath, videolist):
        colorprint.out('COULD NOT MERGE VIDEOS')
        systemExitCode = 2
        sys.exit(systemExitCode)
    if not videoList2TextFile(vlistpath, videolist):
        colorprint.out('COULD NOT CREATE VIDEO FILE IST')
        systemExitCode = 2
        sys.exit(systemExitCode)
    if not videoMerge(prepPath, videolist):
        colorprint.out('COULD NOT MERGE VIDEOS')
        systemExitCode = 2
        sys.exit(systemExitCode)
    # reverse video
    if not videoReverse(cutPath, revPath):
        colorprint.out('FFPROBE EXECUTABLE DOES NOT EXIST')
        systemExitCode = 2
        sys.exit(systemExitCode)
    # cut 30 sec
    if not videoCutPart(videoPath, cutPath):
        colorprint.out('COULD NOT REMOVE AUDIO TRACK FROM VIDEO')
        systemExitCode = 3
        sys.exit(systemExitCode)
    # remove audio
    if not videoRemoveAudio(videoPath, edPath):
        colorprint.out('COULD NOT REMOVE AUDIO TRACK FROM VIDEO')
        systemExitCode = 3
        sys.exit(systemExitCode)
    print('DONE.')