#!/bin/sh
#IFS=`echo -ne "\b"`
photo_path='.'
dst_path='.'
if [ $# -ge 1 ]; then
    dst_path="$1"
fi
if [ $# -ge 2 ]; then 
    photo_path="$2"
fi
tmp_path=$photo_path
if [ $# -eq 3 ]; then 
    tmp_path="$3"
    mkdir -p $tmp_path
fi

if [ $# -gt 3 ]; then
    echo "more then 2 arguments"
    exit 1
fi

quantity=0
for i in `find $photo_path -type f -iname "*jpg"`; do quantity=$(($quantity +1)); mv $i $tmp_path/`echo $i|sed -e 's/^.*\///g'`; done

if [ "$quantity" -lt 100 ]; then 
   echo "photos less then 100"; 
   exit 1; 
else if [ "$quantity" -lt 1000 ]; then
         zc=3 #zero count 000 - 3, 0000 - 4
      else
         zc=4
      fi
fi
cd $tmp_path
count=0; 
for i in `ls -tr`; do  # приводим к виду img-1.jpeg img-50.jpeg img-654.jpeg img-1234.jpeg
   mv $i img-${count}.jpg; 
   count=$(($count+1)); 
done

if [ "$zc" -eq 3 ]; then #приводим к виду img-001.jpeg img-050.jpeg
   for i in {0..9}; do 
      mv img-${i}.jpg img-00${i}.jpg
   done
   for i in {10..99}; do
      mv img-${i}.jpg img-0${i}.jpg
   done
fi
if [ "$zc" -eq 4 ]; then
   for i in {0..9}; do 
      mv img-${i}.jpg img-000${i}.jpg
   done
   for i in {10..99}; do
      mv img-${i}.jpg img-00${i}.jpg
   done
   for i in {100..999}; do
      mv img-${i}.jpg img-0${i}.jpg
   done
fi

#ffmpeg -f image2 -i img-%0${zc}d.jpg -r 12 -vcodec rawvideo -pix_fmt yuv420p -s 1920x1440 output_fullhd.avi
ffmpeg -f image2 -i img-%0${zc}d.jpg -r 12 -vcodec rawvideo -pix_fmt yuv420p -s 1280x960 ${dst_path}/output_hd.avi
cd -
