// js aws version

// 3팀 데이터 전체 조회
async function fetchData3() {
    const response = await fetch('http://57.180.41.44:5011/3datas'); 
    if (!response.ok) { // !: response not ok
        console.error('Failed to fetch data:', response.statusText); // http응답의 상태 메시지
        return;
    }
    const datas = await response.json(); // 응답 객체의 JSON 데이터를 파싱해 js 객체로 변환

    const tbody = document.querySelector('.t2 tbody'); // 요소 선택
    tbody.innerHTML = '';  // 기존 내용을 초기화

    // 데이터 추가
    datas.forEach(data => { // data: api로부터 가져온 JSON 데이터
        const row = document.createElement('tr');
        // 템플릿 리터럴을 통해 문자열 안에 변수 삽입(백틱 사용)
        row.innerHTML = `<td>${data.messageId}</td><td>${data.message}</td>`; 
        tbody.appendChild(row);
    });
}   

// 2,3팀 데이터 전체 조회
async function fetchData23() {
    const response = await fetch('http://57.180.41.44:5011/23datas');
    if (!response.ok) {
        console.error('Failed to fetch data:', response.statusText); 
        return;
    }
    const datas = await response.json();

    const tbody = document.querySelector('.t3 tbody');
    tbody.innerHTML = '';

    datas.forEach(data => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${data.messageId}</td><td>${data.message}</td>`
        tbody.appendChild(row);
    })
}

// 답변 있을시 confirmStatus 업데이트
async function updateConfirm(messageId) {
    const response = await fetch(`http://57.180.41.44:5011/confirm/${messageId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            confirmStatus: 1  // 새로운 confirmStatus 값
        })
    });
    
    if (response.ok) {
        console.log('confirmStatus 업데이트 성공');
    } else {
        console.error('confirmStatus 업데이트 실패');
    }
}

// 개인 데이터 조회
async function fetchData() {
    const response = await fetch('http://57.180.41.44:5011/datas');
    if (!response.ok) {
        console.error('Failed to fetch data:', response.statusText);
        return;
    }
    const { firstmessages, answermessages } = await response.json();

    const tbody = document.querySelector('.t1 tbody');
    tbody.innerHTML = ''; // 기존 내용을 초기화

    // firstmessages 데이터를 테이블에 추가
    // 삼항연산자 조건 ? 참일 때 : 거짓일 때
    firstmessages.forEach(fm => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${fm.messageId}</td>
            <td>${fm.purposeIdx}</td>
            <td>${fm.message}</td>
            <td>${fm.mean}</td>
            <td>${fm.meanAddPhrase}</td>
            <td>${fm.meanAddMor}</td>
            <td>${fm.meanAddAll}</td>
            <td>${fm.runningTime}</td>
            <td>${fm.sendDate ? fm.sendDate : ''}</td> 
            <td><button onclick="sendMessage('${fm.messageId}')">메시지 보내기</button></td>
            <td>${fm.yesValue} x</td>
            <td>${fm.noValue} x</td>
            <td>${fm.confirmStatus === 0 ? 'answer no' : 'answer yes'}</td>
        `;
        tbody.appendChild(row);

        // 해당 messageId에 대한 answer 추가
        const relatedAnswers = answermessages.filter(answer => answer.messageId === fm.messageId);

        // 답변이 달린 경우 confirmStatus 업데이트
        if (relatedAnswers.length > 0) {
            // fm.confirmStatus = 1; // "answer yes"로 변경
            // row.cells[12].innerText = 'answer yes'; // 테이블의 confirmStatus 텍스트 업데이트
            updateConfirm(fm.messageId)

            // 기존의 내용을 유지하고 답변 추가
            relatedAnswers.forEach(answer => {
                const answerRow = document.createElement('tr');
                answerRow.innerHTML = `
                    <td>${answer.answerId}</td>
                    <td></td>
                    <td>ㄴ ${answer.answer}</td>
                    <td>${answer.mean}</td>
                    <td>${answer.meanAddPhrase}</td>
                    <td>${answer.meanAddMor}</td>
                    <td>${answer.meanAddAll}</td>
                    <td></td>
                    <td>${answer.sendDate}</td>
                    <td>${answer.receiveDate}</td>
                    <td></td>
                    <td></td>
                    <td>${answer.yesOrNo === 0 ? 'no' : 'yes'}</td>
                `;
                tbody.appendChild(answerRow);
            });
        } 
    });
}



async function sendMessage(messageId) {
    const sendDate = new Date().toISOString(); // 현재 시간을 ISO 형식으로 가져옴

    const response = await fetch(`http://57.180.41.44:5011/sending/${messageId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sendDate }) // sendDate를 포함 // 자바스크립트 객체를 json 형식으로 변환
    });

    if (response.ok) {
        const result = await response.json();
        alert(result.message); // 성공 메시지 표시
        fetchData(); // 데이터 새로 고침
    } else {
        const error = await response.json();
        alert(`Error: ${error.detail.message}`); // 에러 메시지 표시
    }
}

// 페이지 로드 시 데이터 가져오기
window.onload = async function() {
    // Promise.all: 비동기 함수를 병렬로 호출하는 방법
    await Promise.all([fetchData3(), fetchData23(), fetchData()]);
}

// firstmessages 등록
document.getElementById('submit').addEventListener('click', async function (event) {
    event.preventDefault(); // 기본 버튼 클릭 동작 방지

    // 입력 값 가져오기
    const data = {
        messageId: document.getElementById('messageId').value,
        purposeIdx: document.getElementById('purIdx').value,
        message: document.getElementById('message').value,
        mean: document.getElementById('mean').value,
        meanAddPhrase: document.getElementById('meanAddPhrase').value,
        meanAddMor: document.getElementById('meanAddMor').value,
        meanAddAll: document.getElementById('meanAddAll').value,
        runningTime: document.getElementById('runningTime').value,
        yesValue: document.getElementById('yesValue').value,
        noValue: document.getElementById('noValue').value,
    };

    try {
        const response = await fetch('http://57.180.41.44:5011/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // 자바스크립트 객체를 json 형식으로 변환
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        alert(result.message); // 성공 메시지 표시
    } catch (error) {
        console.error('Error:', error);
        alert('데이터 전송 중 오류가 발생했습니다.');
    }
});

