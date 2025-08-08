const recBtn = document.getElementById("rec-btn");
const recIcon = document.getElementById("rec-icon");
const textForm = document.getElementById("text-form");
const textInput = document.getElementById("text-input");
const responseContainer = document.getElementById("response-container");

let isRecording = false;

recBtn.addEventListener("mousedown", startRecording);
recBtn.addEventListener("mouseup", stopRecording);
recBtn.addEventListener("touchstart", startRecording);
recBtn.addEventListener("touchend", stopRecording);

function startRecording() {
  if (isRecording) return;
  isRecording = true;
  recIcon.src = "rec_recording.png";
  console.log("録音開始（ダミー）");
  // TODO: 実録音ロジックを挿入
}

function stopRecording() {
  if (!isRecording) return;
  isRecording = false;
  recIcon.src = "rec_idle.png";
  console.log("録音終了＆送信（ダミー）");
  // TODO: 音声データ送信処理
}

textForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = textInput.value.trim();
  if (!text) return;
  const response = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  const data = await response.json();
  responseContainer.innerText = data.reply;
});
