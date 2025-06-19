# WebRTC 음성/영상 통화 테스트 가이드

새로 추가된 WebRTC 신호 교환(WebSocket) 기능을 간단히 사용해보는 방법을 설명합니다.

---

## 1. 서버 실행

기존 WebSocket 채팅 기능과 동일하게 `uvicorn app.main:app --reload` 명령으로 실행합니다.

---

## 2. 예시 HTML

아래 코드를 `call.html` 파일로 저장 후 브라우저에서 열면 두 브라우저 간 통화를 시험해 볼 수 있습니다.

```html
<!DOCTYPE html>
<html>
<body>
  <video id="local" autoplay muted></video>
  <video id="remote" autoplay></video>
  <button onclick="startCall()">Start</button>
  <script>
    const room = "demo";
    const username = prompt("name?");
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/webrtc/${room}?username=${username}`);
    const pc = new RTCPeerConnection();
    ws.onmessage = async e => {
      const data = JSON.parse(e.data);
      if (data.type === "offer") {
        await pc.setRemoteDescription(data.offer);
        const ans = await pc.createAnswer();
        await pc.setLocalDescription(ans);
        ws.send(JSON.stringify({type: "answer", answer: ans}));
      } else if (data.type === "answer") {
        await pc.setRemoteDescription(data.answer);
      } else if (data.type === "candidate") {
        pc.addIceCandidate(data.candidate);
      }
    };
    pc.onicecandidate = ({candidate}) => {
      if (candidate) ws.send(JSON.stringify({type: "candidate", candidate}));
    };
    async function startCall() {
      const stream = await navigator.mediaDevices.getUserMedia({video:true,audio:true});
      document.getElementById('local').srcObject = stream;
      stream.getTracks().forEach(t => pc.addTrack(t, stream));
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      ws.send(JSON.stringify({type: "offer", offer}));
    }
    pc.ontrack = ev => (document.getElementById('remote').srcObject = ev.streams[0]);
  </script>
</body>
</html>
```

두 개의 브라우저 창을 열어 같은 방 이름을 입력하면 P2P 통화를 시도할 수 있습니다. 신호 데이터는 본 서버를 통해 교환됩니다.
