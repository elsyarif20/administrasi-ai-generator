const MODEL_URL = "./assets/models";

let modelsLoaded = false;

export async function loadFaceModels() {
  try {
    if (modelsLoaded) return;

    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
      faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
      faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL)
    ]);

    modelsLoaded = true;
  } catch (error) {
    throw new Error(`Gagal memuat model face-api: ${error.message}`);
  }
}

export async function createDescriptorFromImage(dataUrl) {
  try {
    const img = await faceapi.fetchImage(dataUrl);
    const detection = await faceapi
      .detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceDescriptor();

    if (!detection) {
      throw new Error("Wajah tidak terdeteksi pada gambar.");
    }

    return Array.from(detection.descriptor);
  } catch (error) {
    throw new Error(`Gagal membuat face descriptor: ${error.message}`);
  }
}

export async function verifyFace(snapshotDataUrl, registeredDescriptor, threshold = 0.55) {
  try {
    if (!Array.isArray(registeredDescriptor) || registeredDescriptor.length !== 128) {
      throw new Error("Face descriptor terdaftar tidak valid.");
    }

    const currentDescriptor = await createDescriptorFromImage(snapshotDataUrl);
    const distance = faceapi.euclideanDistance(currentDescriptor, registeredDescriptor);

    return {
      match: distance <= threshold,
      distance
    };
  } catch (error) {
    throw new Error(`Validasi wajah gagal: ${error.message}`);
  }
}
