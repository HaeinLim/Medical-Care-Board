# aws서버 ver.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from databases import Database
from datetime import datetime, timedelta
import decimal
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# 일본 표준시 설정
def get_jp_time():
    return datetime.utcnow() + timedelta(hours=9)

DATABASE_URL1 = "mysql://admin:Seigakushakorea0308(!@127.0.0.1/boardDB1_lhi11"
DATABASE_URL2 = "mysql://admin:Seigakushakorea0308(!@127.0.0.1/boardDB2_lhi11"
DATABASE_URL3 = "mysql://admin:Seigakushakorea0308(!@127.0.0.1/boardDB3_lhi11"

database1 = Database(DATABASE_URL1)
database2 = Database(DATABASE_URL2)
database3 = Database(DATABASE_URL3)

async def start():
    print("Start up.")
    await database1.connect()
    await database2.connect()
    await database3.connect()

async def shutdown():
    print("Shutdown")
    await database1.disconnect()
    await database2.disconnect()
    await database3.disconnect()

# lifespan: fastapi 애플리케이션이 시작될 때 db 연결을 맺거나 종료될 때 연결을 닫아줌(비동기 컨텍스트 관리자로 구현)
# on_event 대신 사용, lifespan으로 이벤트 권장(안정적)
@asynccontextmanager # 비동기 컨텍스트 관리자
async def lifespan(app:FastAPI):
    await start()
    yield
    await shutdown()

app = FastAPI(lifespan=lifespan)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin에 대해 접근 허용 (실제 배포 시 '*' 대신 특정 origin을 설정하는 것이 좋음)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreateData(BaseModel):
    messageId: str
    purposeIdx: str
    message: str
    mean: decimal.Decimal
    meanAddPhrase: decimal.Decimal
    meanAddMor: decimal.Decimal
    meanAddAll: decimal.Decimal
    runningTime: str
    createdDate: Optional[datetime] = None # 원하는 시간을 넣기 위해 선택적 필드로
    yesValue: decimal.Decimal
    noValue: decimal.Decimal
    confirmStatus: Optional[bool] = False

class UpdateData(BaseModel):
    sendDate: Optional[datetime]

class CreateAnswer(BaseModel):
    answerId: str
    messageId: str
    answer: str
    mean: Optional[decimal.Decimal] = None
    meanAddPhrase: Optional[decimal.Decimal] = None
    meanAddMor: Optional[decimal.Decimal] = None
    meanAddAll: Optional[decimal.Decimal] = None
    receiveDate: Optional[datetime] = None
    yesOrNo: Optional[bool]

class UpdateConfirmStatus(BaseModel):
    confirmStatus: bool

# 개인 데이터 전체 가져오기
# 개인 조회 문제: join 사용시 answermessages와 겹치는 컬럼때문에 데이터가 덮힘
#  => 조회 쿼리를 두개로 나눔
@app.get("/datas")
async def get_all_datas():
    try:
        query1 = """
        SELECT * FROM firstmessages
        """
        datas1 = await database1.fetch_all(query1)

        query2 = """
        SELECT * FROM answermessages
        """
        datas2 = await database1.fetch_all(query2)

        if not datas1 and not datas2:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Datas not found",
                    "message": "The requested resource was not found on the server. Please check your request and try again."
                }
            )
        return {"firstmessages": datas1, "answermessages": datas2}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
    
# 3팀 messageId, message 전체 조회
@app.get("/3datas")
async def get_3messages():
    try:
        query = """
        SELECT messageId, message FROM firstmessages    
        """
        datas = await database2.fetch_all(query)

        if not datas:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Datas not found",
                    "message": "The requested resource was not found on the server. Please check your request and try again."
                }
            )
        # return datas
        return [{"messageId": data[0], "message": data[1]} for data in datas] # JSON 형식으로 반환

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
    
# 모든 팀 messageId, message 전체 조회
@app.get("/23datas")
async def get_23messages():
    try:
        query = """
        SELECT messageId, message FROM firstmessages    
        """
        datas = await database3.fetch_all(query)

        if not datas:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Datas not found",
                    "message": "The requested resource was not found on the server. Please check your request and try again."
                }
            )
        return [{"messageId": data[0], "message": data[1]} for data in datas]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
    
# firstmessages 데이터 삽입
@app.post("/data")
async def create_data(data: CreateData):
    
    data.createdDate = get_jp_time()
    query = """
    INSERT INTO firstmessages (messageId, purposeIdx, message, mean, meanAddPhrase, meanAddMor, meanAddAll, runningTime, createdDate, yesValue, noValue, confirmStatus)
    VALUES (:messageId, :purposeIdx, :message, :mean, :meanAddPhrase, :meanAddMor, :meanAddAll, :runningTime, :createdDate, :yesValue, :noValue, :confirmStatus)
    """
    values = data.dict()
    try:
        await database1.execute(query, values=values)
        await database2.execute(query, values=values)
        await database3.execute(query, values=values)
        return {"message": "Data created successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
    
# answermessages 데이터 삽입
@app.post("/answer")
async def create_answer(data: CreateAnswer):
    query = """
    SELECT sendDate, mean, meanAddPhrase, meanAddMor, meanAddAll, noValue, yesValue FROM firstmessages WHERE messageId = :messageId
    """
    existing_data = await database1.fetch_one(query, values={"messageId": data.messageId})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    
    # 필요한 데이터 가져오기
    sendDate = existing_data["sendDate"]
    mean = existing_data["mean"]
    meanAddPhrase = existing_data["meanAddPhrase"]
    meanAddMor = existing_data["meanAddMor"]
    meanAddAll = existing_data["meanAddAll"]
    yesValue = existing_data["yesValue"]
    noValue = existing_data["noValue"]

    # 반응에 따른 값 계산식 설정
    multiplier = yesValue if data.yesOrNo else noValue

    # 계산
    mean_result = mean * multiplier
    meanAddPhrase_result = meanAddPhrase * multiplier
    meanAddMor_result = meanAddMor * multiplier
    meanAddAll_result = meanAddAll * multiplier

    query = """
    INSERT INTO answermessages(answerId, messageId, answer, mean, meanAddPhrase, meanAddMor, meanAddAll, receiveDate, sendDate, yesOrNo)
    VALUES(:answerId, :messageId, :answer, :mean, :meanAddPhrase, :meanAddMor, :meanAddAll, :receiveDate, :sendDate, :yesOrNo)
    """
    values = data.dict()
    # 위에서 가져온, 계산한 데이터 직접 삽입
    values["receiveDate"] = get_jp_time()  # 일본 표준시로 설정
    values["sendDate"] = sendDate  # sendDate 추가
    values["mean"] = mean_result
    values["meanAddPhrase"] = meanAddPhrase_result
    values["meanAddMor"] = meanAddMor_result
    values["meanAddAll"] = meanAddAll_result

    try:
        await database1.execute(query, values=values)
        await database2.execute(query, values=values)
        await database3.execute(query, values=values)

        confirmStatus = True
        await update_confirm(data.messageId, UpdateConfirmStatus(messageId=data.messageId, confirmStatus=confirmStatus))

        return {"message": "Answer message created successfully."}
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 오류 메시지 출력
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )
    
# 답변 있을 때 confirmStatus 변경
@app.put("/confirm/{messageId}")
async def update_confirm(messageId: str, data: UpdateConfirmStatus):
    query = "SELECT * FROM firstmessages WHERE messageId = :messageId"
    existing_data = await database1.fetch_one(query, values={"messageId": messageId})
    
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    
    query = """
    UPDATE firstmessages
    SET confirmStatus = :confirmStatus
    WHERE messageId = :messageId
    """
    values = {"confirmStatus": data.confirmStatus, "messageId": messageId}

    try:
        result = await database1.execute(query, values=values)
        if result is None:  # DB에서 업데이트된 행이 없는 경우
            raise HTTPException(status_code=400, detail="Update failed, no rows affected.")
        
        await database2.execute(query, values=values)
        await database3.execute(query, values=values)

        return {"message": "ConfirmStatus updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )

# sendDate
# 입력된 데이터에 sendDate만 추가하는 것으로 update문, put을 사용
@app.put("/sending/{messageId}")
async def send_date(messageId: str, data: UpdateData):
     
    query = "SELECT * FROM firstmessages WHERE messageId = :messageId"
    existing_data = await database1.fetch_one(query, values={"messageId": messageId})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    if data.sendDate is None:  # sendDate가 None인 경우 현재 시간 설정
        data.sendDate = get_jp_time()
    query = """
    UPDATE firstmessages
    SET
        sendDate = :sendDate
    WHERE messageId = :messageId
    """
    values = data.dict()
    values["messageId"] = messageId
    try:
        await database1.execute(query, values=values)
        await database2.execute(query, values=values)
        await database3.execute(query, values=values)
        return {"message": "Data sent successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )

# 데이터 삭제
@app.delete("/data/{messageId}")
async def delete_firstmessages(messageId: str):
    query = "SELECT * FROM firstmessages WHERE messageId = :messageId"
    existing_data = await database1.fetch_one(query, values={"messageId": messageId})
    if existing_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    
    query = "DELETE FROM firstmessages WHERE messageId = :messageId"
    try:
        await database1.execute(query, values={"messageId": messageId})
        await database2.execute(query, values={"messageId": messageId})
        await database3.execute(query, values={"messageId": messageId})
        return {"message": "Data deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )