# RC_Fruit
robocom智慧果园c++版本代码（自开发）



# 标记 (检测内存泄漏)

valgrind --leak-check=full ./testMem  


# 编译链接库

g++ -o filename.so -shared -static-libstdc++ -fPIC filename.cpp -I ${headfilepath}/


# opencv
   filename.so:
	g++ -o filename.so -shared -fPIC filename.cpp -lopencv_core -lopencv_highgui -lopencv_imgcodecs  -ltwocams -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_videoio -lz -lwebp -lpthread -ltiff -lpng
	
	
# arm64 架构libjsper-dev
sudo add-apt-repository "deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ xenial main multiverse restricted universe"
sudo apt update
sudo apt install libjasper1 libjasper-dev
