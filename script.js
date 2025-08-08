const recButton = document.getElementById("rec-button");
const textInput = document.getElementById("text-input");
const sendTextBtn = document.getElementById("send-text");
const chatLog = document.getElementById("chat-log");

let mediaRecorder;
let audioChunks = [];

function addChatEntry(role, text) {
  const div = document.createElement("div");
  div.className = role;
  div.innerText = text;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'ja-JP';
  window.speechSynthesis.speak(utterance);
}

recButton.addEventListener("mousedown", async () => {
  recButton.src = "rec_recording.png";
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];
  mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", audioBlob);
    const res = await fetch("/api/audio", { method: "POST", body: formData });
    const data = await res.json();
    addChatEntry("assistant", data.reply);
    speak(data.reply);
  };
  mediaRecorder.start();
});

recButton.addEventListener("mouseup", () => {
  recButton.src = "rec.png";
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
});

sendTextBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  if (!text) return;
  addChatEntry("user", text);
  textInput.value = "";
  const res = await fetch("/api/text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  const data = await res.json();
  addChatEntry("assistant", data.reply);
  speak(data.reply);
});