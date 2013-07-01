#!/bin/sh
#rm `ls|head -1`
first_shot=`ls|head -1|cut -c 5-8`
quantity=`ls|wc -l|awk '{print $1}'`

if [ "$quantity" -lt 100 ]; then 
   echo "photos less then 100"; 
   exit 1; 
else if [ "$quantity" -lt 1000 ]; then
         zc=3 #zero count 000 - 3, 0000 - 4
      else
         zc=4
      fi
fi

count=0; 
for i in `ls -tr`; do  # приводим к виду img-1.jpeg img-50.jpeg img-654.jpeg img-1234.jpeg
   mv $i img-${count}.jpeg; 
   count=$(($count+1)); 
done

if [ "$zc" -eq 3 ]; then #приводим к виду img-001.jpeg img-050.jpeg
   for i in {0..9}; do 
      mv img-${i}.jpeg img-00${i}.jpeg
   done
   for i in {10..99}; do
      mv img-${i}.jpeg img-0${i}.jpeg
   done
fi
if [ "$zc" -eq 4 ]; then
   for i in {0..9}; do 
      mv img-${i}.jpeg img-000${i}.jpeg
   done
   for i in {10..99}; do
      mv img-${i}.jpeg img-00${i}.jpeg
   done
   for i in {100..999}; do
      mv img-${i}.jpeg img-0${i}.jpeg
   done
fi


#for i in `seq 1 $quantity`; do 
#   echo mv GOPR`echo $(($((${first_shot}-1))+\`echo ${i}|sed -e 's/^00//g' -e 's/^0//g'\`))`.JPG img-$i.jpeg; 
#done

ffmpeg -f image2 -i img-%0${zc}d.jpeg -r 12 -vcodec rawvideo -pix_fmt yuv420p -s 1920x1440 output_fullhd.avi
ffmpeg -f image2 -i img-%0${zc}d.jpeg -r 12 -vcodec rawvideo -pix_fmt yuv420p -s 1280x960 output_hd.avi
