const video = document.getElementById('video');

async function setup() {
  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('./models'),
    faceapi.nets.faceExpressionNet.loadFromUri('./models'),
  ]);

  startVideo();
}

function startVideo() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    })
    .catch(err => {
      console.error("カメラ起動失敗:", err);
      alert("カメラのアクセス許可が必要です！");
    });
}

video.addEventListener('play', () => {
  const canvas = document.getElementById('overlay');
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceExpressions();

    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
  }, 100);
});

setup();
