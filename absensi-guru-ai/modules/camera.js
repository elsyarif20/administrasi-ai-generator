let activeStream = null;

export async function startCamera(videoEl) {
  try {
    if (!navigator.mediaDevices?.getUserMedia) {
      throw new Error("Browser tidak mendukung akses kamera.");
    }

    activeStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false
    });

    videoEl.srcObject = activeStream;
    await videoEl.play();
  } catch (error) {
    throw new Error(`Gagal mengaktifkan kamera: ${error.message}`);
  }
}

export function takeSnapshot(videoEl, canvasEl) {
  try {
    if (!videoEl.videoWidth || !videoEl.videoHeight) {
      throw new Error("Video belum siap untuk snapshot.");
    }

    canvasEl.width = videoEl.videoWidth;
    canvasEl.height = videoEl.videoHeight;
    const ctx = canvasEl.getContext("2d");
    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);

    return canvasEl.toDataURL("image/jpeg", 0.9);
  } catch (error) {
    throw new Error(`Gagal mengambil snapshot: ${error.message}`);
  }
}

export function stopCamera(videoEl) {
  if (activeStream) {
    activeStream.getTracks().forEach((track) => track.stop());
    activeStream = null;
  }
  if (videoEl) {
    videoEl.srcObject = null;
  }
}
