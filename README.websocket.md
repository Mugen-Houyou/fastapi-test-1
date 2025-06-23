# WebSocket 실시간 채팅 테스트 가이드

프로젝트에 새로이 추가된 WebSocket 실시간 채팅 기능을 간단하게 테스트하는 방법을 설명합니다.

---

## 1. 서버 실행

별도의 커맨드 없이 `uvicorn app.main:app --reload`로 본서버를 실행하면 작동합니다. 메시지 보존을 위해 로컬 또는 외부 Redis 인스턴스가 필요하며, 연결 주소는 `.env` 파일의 `REDIS_URL` 로 지정합니다. Redis 인스턴스 구성 시 auth 패스워드를 지정하여야 하며, 지정한 패스워드는 `.env` 파일의 `REDIS_AUTH_PASSWORD`에도 넣으면 됩니다.

---

## 2. 간단한 브라우저 테스트

1. 아래 예시 HTML 파일을 로컬에 저장합니다(파일명은 예: `chat.html`).

```html
<!DOCTYPE html>
<html>
<body>
  <input id="message" type="text" placeholder="메시지 입력"/>
  <button onclick="sendMessage()">전송</button>
  <div id="messages"></div>

  <script>
    const roomId = "general"; // 방 이름
    const username = prompt("이름 입력:");
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/chat/${roomId}?username=${username}`);

    ws.onmessage = function(event) {
      const messages = document.getElementById('messages');
      messages.innerHTML += `<p>${event.data}</p>`;
    };

    function sendMessage() {
      const input = document.getElementById('message');
      ws.send(input.value);
      input.value = '';
    }
  </script>
</body>
</html>
```

2. 브라우저에서 위 파일을 열고 두 개 이상의 탭(또는 다른 브라우저)에서 접속해 메시지를 주고받아 보세요.

---

## 3. CLI 도구(wscat) 사용 예시

`wscat` 이나 [`websocat`](https://github.com/vi/websocat/releases) 같은 WebSocket 클라이언트 도구를 설치했다면 터미널에서 바로 테스트할 수도 있습니다.

예시(`websocat` 필요):

![image](https://github.com/user-attachments/assets/86d22c6a-b4c3-4c82-955a-cb0ab5c6036f)

```bash
./websocat.x86_64-unknown-linux-musl  ws://localhost:8000/api/v1/ws/chat/general?username=alice
```

새 터미널을 열어 다른 사용자로 접속 후 메시지를 입력하면 서로의 메시지가 실시간으로 전달되는 것을 확인할 수 있습니다.

또한 Redis 서버가 살아 있는 한 재접속 시 채팅 기록이 보존되며 클라이언트에서 이전 기록이 복원되는 것을 확인할 수 있습니다.
