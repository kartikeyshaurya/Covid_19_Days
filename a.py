for i in {10..50} 
do 
 
	link="https://edx-video.net/University_of_TorontoXUTQML101x-V00" 
	rest="00_DTH.mp4" 
	wget "$link$i$rest" 
 
done 