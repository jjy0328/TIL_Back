from market import app

# 출시할 땐 debug mode = OFF하기
if __name__ == '__main__':
    app.run(debug = True, port=5000)
    #app.run(port=5001) #port 번호 지정해서 실행