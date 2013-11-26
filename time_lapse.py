__author__ = 'onotole'
import os,re,random,shutil,time

pathSD="/Volumes/NO NAME"
delayBefore=600  #10 min
tmpDir="/tmp/.timelapse" + str(random.randint(0,100)) + "/"
dstPath="~/Desktop/"

def normalize(number, measure):
    result=''
    for i in range(len(str(measure))-len(str(number))):
        result+= '0'
    result += str(number)
    return result

def createFileList(path=pathSD):
    path_f=[]
    for d, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                path = os.path.join (d,f)
                path_f.append(path)
    path_f.sort()
    return path_f

def findTimeLapserRaw(path_f):
    oldCreateTime=0.
    for file in path_f:
        createTime = os.path.getctime(file)
        if oldCreateTime > 0 and createTime - oldCreateTime > delayBefore:
            startTimeLapse=file
        if oldCreateTime > 0 and oldCreateTime - createTime > delayBefore:
            pass #print (createTime, oldCreateTime, file, "smth get wrong")
        oldCreateTime = createTime

    filesToTimeLapse=path_f[path_f.index(startTimeLapse):]
    return filesToTimeLapse

def preparing(filesToTimeLapse,tmpDir=tmpDir):
    #create tmpdir and copy images to it
    if os.path.exists(tmpDir):
        os.removedirs(tmpDir)
    os.mkdir(tmpDir)
    length = len(filesToTimeLapse)
    for i in range(length):
        shutil.copyfile(filesToTimeLapse[i],tmpDir + 'img-' + normalize(i,length)+".jpg")
    zeroCount=len(str(length))

def convert(tmpDir, dstPath, zeroCount):
    convertCommand = 'cd '+ tmpDir +'; ffmpeg -f image2 -i img-%0'+ str(zeroCount) + 'd.jpg -r 24 -vcodec rawvideo -pix_fmt yuv420p -s 1280x960 '+\
                 dstPath + 'OutputVideo' + str(time.time()).split('.')[0] + '.avi'
    os.system(convertCommand)
    os.system('rm -rf '+tmpDir)

if __name__ == "__main__":
    pass

path_f=createFileList(pathSD)

filesToTimeLapse=findTimeLapserRaw(path_f)

preparing(filesToTimeLapse,tmpDir)

convert(tmpDir,dstPath,len(str(len(filesToTimeLapse))))