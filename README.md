# Medical Care 게시판
감기에 관하여 특정 시간대에 알맞는 메시지를 정한 후 답변을 보내고, 그에 따른 value 분석값을 얻을 수 있는 게시판 프로젝트입니다.

## 목차
  - [개요](#개요)
  - [프로그램 설명](#프로그램-설명)
  - [프로그램 화면](#프로그램-화면)
## 개요
  - 프로젝트명 : Medical Care 게시판
  - 프로젝트 진행기간 : 2024.03.18-2024.07.30
  - 사용 기술 : Python, HTML, CSS, JavaScript, MySQL, AWS, Postman
  - 팀 구성원 : 임해인 외 4명

## 프로그램 설명
<div align="center">
  <table>
    <tr>
      <td>
        <img src="https://github.com/user-attachments/assets/2cf49c12-1ddc-4951-bec7-c5573d6ee214" width="600" height="400">
      </td>
    </tr>
    <tr>
      <td align="center">Medical Care 게시판</td>
    </tr>
  </table>
</div>
사용자가 약을 잊지 않고 감기를 예방하는 메시지 구성과 메시지의 NLP 분석을 따른 value값을 계산해 보고자 제작하였습니다.

  - 메시지 추가하기 📥 <br>
    상단의 입력창에 요구하는 데이터를 입력하고 submit 버튼을 클릭하면 데이터베이스에 메시지가 저장되며, refresh 버튼을 클릭해
    웹 페이지에서 확인 가능합니다. 해당 게시판은 총 3개의 데이터베이스를 사용하고, 각 테이블마다 입력한 메시지가 추가됩니다.
    
  - 메시지 전송하기 ⤴️ <br>
    Receive Date 컬럼에 위치한 send 버튼을 클릭하면 send Date 컬럼에 메시지를 전송한 시간이 입력됩니다. 해당 시간은 일본의 표준시를 설정하여
    입력되도록 하였습니다.

  - 전송된 메시지에 대한 답변 보내기 ✍️ <br>
    전송된 메시지에 한해서 Postman을 통해 답변을 작성할 수 있습니다. 해당 답변은 입력한 순서대로 페이지에 정렬됩니다. 답변을 입력하면
    Yes or No 컬럼에 전송된 메시지에는 'answer no'에서 'answer yes'로, 답변에는 해당 메시지에 알맞는 답변일시 긍정의 반응인 'yes'가,
    어울리지 않는 답변일 시 부정의 반응인 'no'가 표시됩니다.

## 프로그램 화면

- 게시판 전체 페이지

<div align="center">
  <table align="center">
      <tr>
        <th>게시판 전체 페이지</th>
      </tr>
      <tr>
        <td>
          <img src="https://github.com/user-attachments/assets/2cf49c12-1ddc-4951-bec7-c5573d6ee214" width="400" height="200">
        </td>
      </tr>
      <tr>
        <td>
          - 메시지 추가 가능 <br>
          - 3개의 데이터베이스에 담긴 데이터 조회 가능
        </td>
      </tr>
  </table>
</div>

- 메시지 전송

<div align="center">
  <table align="center">
    <tr>
      <th>메시지 전송</th>
    </tr>
    <tr>
      <td>
        <img src="https://github.com/user-attachments/assets/c3ea9d0d-c9d4-44ec-8bc3-f7eb516ff6a7" width="400" height="200">
      </td>
    </tr>
    <tr>
        <td>
          - send 버튼으로 메시지 전송 <br>
          - Send Date 컬럼에 메시지 전송 시간 표시
        </td>
      </tr>
  </table>
</div>

  - 전송된 메시지 답변

<div align="center">
  <table align="center">
    <tr>
      <th>Postman 답변</th><th>답변 등록 확인</th>
    </tr>
    <tr>
      <td>
        <img src="https://github.com/user-attachments/assets/9622eb2b-dc2c-41c3-b5ce-a5a7c019e666" width="400" height="200">
      </td>
      <td>
        <img src="https://github.com/user-attachments/assets/e795f027-0c3e-4ad0-b705-0ca973898a50" width="400" height="200">
      </td>
    </tr>
    <tr>
      <td>
        - 답변에 필요한 데이터 입력 후 전송 <br>
      </td>
      <td>
        - 성공적으로 답변 전송 시 Yes or No 컬럼의 데이터 변화<br>
      </td>
    </tr>
  </table>
</div>
