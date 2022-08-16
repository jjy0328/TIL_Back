# Tutorial
# FreeCodeCamp FastAPI - clone Coding

from operator import gt
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1 : {
        "name" : "zero",
        "age" : 17,
        "year" : "year 12"
    }
}

class Student(BaseModel):
    name: str
    age : int
    year: str


# update시, 일부만 바꿔도 될 수 있도록 하는 class를 따로 만들어 둠
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


# 엔드포인트 생성 : url의 엔드포인트
# : 통신 채널의 한 끝. 다른 작업을 수행
# amazon.com/delete-user 에서 'delete-user'
# GET - get an information 
#       (데이터에 대한 정보를 얻거나 반환)
# POST - create something new 
#        (새로운 것을 생성 후 데이터베이스에 넣거나 새로운 객체로 생성)
# PUT -  update
#        (데이터 업데이트 혹은 특정 객체에서 무언가를 업데이트)
# DELETE -  delete something

@app.get("/")
def index():
    return{"name" : "First Data"}

# 명령 프롬프트 :
# /Users/j/Desktop/projects/snubpy/fastapi/tutorial>uvicorn myapi:app --reload : 서버용 빠른 api 프로젝트를 실행하기 위한 기본 명령줄

# Endpoint parameter :
# url의 끝네 입력과 관련된 데이터를 반환하는데 사용
# 경로 파라메터 , 쿼리 파라메터로 나뉨


# 1. 경로 파라메터
# 수집하려는 모든 정보를 엔드포인트의 url에 추가하여야 함

# @app.get("/get-student/{student_id}") # {} : 동적 변수
# def get_student(student_id: int):     # 학생변수 초기화, 데이터 유형 지정
#     return students[student_id]   # 하나의 값을 반환하길 원하면 []안에 하나 지정 


@app.get("/get-student/{student_id}") # {} : 동적 변수
def get_student(student_id: int = Path(None, #path : 일단 비움. 오류 캐치에 유리
                                        description = "The ID of the student you want to view",
                                        # gt: 초과, lt : 미만, ge : 이상, le : 이하
                                        gt=0, lt=3)): # 정수 -> gt=0  
    return students[student_id]



# 2. 쿼리 파라메터
# google.com/result?search=Python -> 'search(key)=Python(value)' = 쿼리 파라메터
# 경로 매개변수와 매우 유사한 url 값을 전달하는데 사용

# none : docs의 description란에 required가 사라짐

# @app.get("/get-by-name")
# def get_student(*, name: Optional[str] = None, test : int): # default argument는 none default argument 앞에 와선 안됨
#                                                             # 쿼리 매개변수를 원하는 위치에 둘 수 있도록 '*'추가 
#     for student_id in students:
#         if students[student_id]["name"] == name:
#             return students[student_id]
#     return {"Data" : "Not found"} 


# 경로와 쿼리 파라메터 합치기
@app.get("/get-by-name/{student_id}")
def get_student(*, studnet_id: int, name: Optional[str] = None, test : int): 
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data" : "Not found"}
 


# Request body and post method

# 사용자가 제출하는 세부정보 -> 새 학생 개체를 만듦
# docs에서 저장을 저장했을 시, 새로고침하면 저장된 정보가 다 사라짐
@app.post("/create-student/{student_id}") # id의 경로 매개변수
def create_student(student_id: int, student: Student): # Studnet class를 사용하여 새 학생 객체 생성
    if student_id in students:     # student_id가 dic파일에 존재할시, error 메세지
        return{"Error" : "Student exists"}

    students[student_id] = student
    return student[student_id]



# Put Method
# 이미 존재하는 것을 업데이트
@app.put("/update-student/{studet_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students: # 정보가 존재하지 않으면 update 못함
        return{"Error" : "Student does not exist"}

    # 한가지만 수정하면 나머지가 null처리가 되기 때문에 방지용
    if student.name != None:
        students[student_id].name = student.name
    
    if student.age != None:
        students[student_id].age = student.age
 
    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]


# Delete Method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {"Error" : "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted successfully"}