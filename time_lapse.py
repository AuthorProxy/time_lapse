__author__ = 'onotole'
import os,re,random,shutil,time
import argparse

parser = argparse.ArgumentParser(description='Great Description To Be Here')


pathSD="/Volumes/NO NAME"
delayBefore=600  #10 min
tmpDir="/tmp/.timelapse" + str(random.randint(0,100)) + "/"
dstPath="~/Desktop/"
quality='HD' #FullHD
rate=24

def lookingForSD():
    pathSD=[]
    if os.path.exists('/Volumes/'):
        mountPoint='/Volumes/'
    else :
        mountPoint='/media/'
    for disk in os.listdir(mountPoint):
        if 'DCIM' in os.listdir(os.path.join(mountPoint,disk)):
            pathSD.append(os.path.join(mountPoint,disk))
    if len(pathSD)>1:
        print ("I found more then one SD")
    try:
        result = pathSD[-1]
    except IndexError:
        print("SD not found")
        exit (1)
    return result

def normalize(number, measure):
    result=''
    for i in range(len(str(measure))-len(str(number))):
        result+= '0'
    result += str(number)
    return result

def createFullFileList(path=pathSD):
    path_f=[]
    for d, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('jpg') or f.endswith('JPG'):
                path = os.path.join (d,f)
                path_f.append(path)
    path_f.sort()
    return path_f

def findTimeLapserRaw(path_f, src_amount = 1):
    amount = src_amount
    oldCreateTime=0.
    for file in path_f:
        createTime = os.path.getctime(file)
        if oldCreateTime > 0 and createTime - oldCreateTime > delayBefore:
            startTimeLapse=file
        if oldCreateTime > 0 and oldCreateTime - createTime > delayBefore:
            pass  #print (createTime, oldCreateTime, file, "smth get wrong")
        oldCreateTime = createTime

    filesToTimeLapse=path_f[path_f.index(startTimeLapse):]
    filesToTimeLapses = [filesToTimeLapse[:]]
    while amount > 1 :
        filesToTimeLapse=[]
        previousStartTimeLapse = startTimeLapse
        oldCreateTime=0.
        for file in path_f:
            createTime = os.path.getctime(file)
            if oldCreateTime > 0 and createTime - oldCreateTime > delayBefore and createTime < os.path.getctime(previousStartTimeLapse):
                startTimeLapse=file
            if oldCreateTime > 0 and oldCreateTime - createTime > delayBefore:
                pass  #print (createTime, oldCreateTime, file, "smth get wrong")
            oldCreateTime = createTime

        filesToTimeLapse=path_f[path_f.index(startTimeLapse):path_f.index(previousStartTimeLapse)-1]
        filesToTimeLapses.append(filesToTimeLapse[:])
        amount -= 1
    return filesToTimeLapses

def preparing(filesToTimeLapse,tmpDir=tmpDir):

    if os.path.getsize(filesToTimeLapse[0])*len(filesToTimeLapse)*1.5 > shutil.disk_usage('/tmp/').free:
        raise Exception('not enough space')
    #create tmpdir and copy images to it
    if os.path.exists(tmpDir):
        os.removedirs(tmpDir)
    os.mkdir(tmpDir)
    length = len(filesToTimeLapse)
    for i in range(length):
        shutil.copyfile(filesToTimeLapse[i],tmpDir + 'img-' + normalize(i,length)+".jpg")
    zeroCount=len(str(length))

def convert(tmpDir, dstPath, zeroCount):
    if quality=='FullHD':
        size='1900x1425'
    else:
        size='1280x960'
    convertCommand = 'cd '+ tmpDir +'; ffmpeg -f image2 -i img-%0'+ str(zeroCount) + 'd.jpg -r ' + str(rate) + \
        ' -vcodec rawvideo -pix_fmt yuv420p -s ' + size + ' ' + dstPath + 'OutputVideo' + str(time.time()).split('.')[0] + '.avi'
    os.system(convertCommand)
    os.system('rm -rf '+tmpDir)



if __name__ == "__main__":
    path_f=createFullFileList(lookingForSD())
    filesToTimeLapses=findTimeLapserRaw(path_f,2)
    for filesToTimeLapse in filesToTimeLapses:
        preparing(filesToTimeLapse,tmpDir)
        convert(tmpDir,dstPath,len(str(len(filesToTimeLapse))))