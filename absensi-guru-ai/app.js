import {
  collection,
  addDoc,
  onSnapshot,
  orderBy,
  query,
  where,
  getDocs
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { auth, db, serverTimestamp } from "./config/firebase.js";
import { login, logout, observeAuth, getUserProfile } from "./modules/auth.js";
import { startCamera, takeSnapshot, stopCamera } from "./modules/camera.js";
import { loadFaceModels, verifyFace } from "./modules/face.js";
import { getCurrentLocation, validateSchoolRadius } from "./modules/gps.js";
import { exportToExcel, exportToPdf } from "./modules/report.js";
import { sendWhatsAppNotification } from "./modules/wa.js";

const SCHOOL_COORDINATE = {
  latitude: -6.2000,
  longitude: 106.8166
};

const ATTENDANCE_RADIUS = 100;
const FONNTE_TOKEN = "ISI_TOKEN_FONNTE_ANDA";

const el = {
  loginSection: document.getElementById("loginSection"),
  guruSection: document.getElementById("guruSection"),
  adminSection: document.getElementById("adminSection"),
  loginForm: document.getElementById("loginForm"),
  email: document.getElementById("email"),
  password: document.getElementById("password"),
  video: document.getElementById("video"),
  snapshotCanvas: document.getElementById("snapshotCanvas"),
  startCameraBtn: document.getElementById("startCameraBtn"),
  absenBtn: document.getElementById("absenBtn"),
  absenResult: document.getElementById("absenResult"),
  guruInfo: document.getElementById("guruInfo"),
  logoutGuru: document.getElementById("logoutGuru"),
  logoutAdmin: document.getElementById("logoutAdmin"),
  exportExcelBtn: document.getElementById("exportExcelBtn"),
  exportPdfBtn: document.getElementById("exportPdfBtn"),
  logTableBody: document.getElementById("logTableBody"),
  attendanceChart: document.getElementById("attendanceChart"),
  themeToggle: document.getElementById("themeToggle")
};

let currentUser = null;
let attendanceLogs = [];
let attendanceChart = null;
let unsubLogs = null;

function setStatus(message, type = "info") {
  el.absenResult.textContent = message;
  el.absenResult.style.borderColor = type === "error" ? "#ef4444" : "#10b981";
}

function setVisible(section) {
  [el.loginSection, el.guruSection, el.adminSection].forEach((node) => node.classList.add("hidden"));
  section.classList.remove("hidden");
}

function formatDate(value) {
  const date = value?.toDate ? value.toDate() : new Date(value || Date.now());
  return date.toLocaleString("id-ID");
}

function getStatusByTime(date = new Date()) {
  const hours = date.getHours();
  const minutes = date.getMinutes();
  if (hours < 7 || (hours === 7 && minutes === 0)) {
    return "Tepat Waktu";
  }
  return "Terlambat";
}

function renderTable(logs) {
  el.logTableBody.innerHTML = "";
  logs.forEach((log) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${log.timeLabel}</td>
      <td>${log.name}</td>
      <td>${log.status}</td>
      <td>${Number(log.distanceMeters).toFixed(2)}</td>
      <td>${log.latitude.toFixed(5)}, ${log.longitude.toFixed(5)}</td>
    `;
    el.logTableBody.appendChild(tr);
  });
}

function renderChart(logs) {
  const tepatWaktu = logs.filter((l) => l.status === "Tepat Waktu").length;
  const terlambat = logs.filter((l) => l.status === "Terlambat").length;

  if (attendanceChart) attendanceChart.destroy();

  attendanceChart = new Chart(el.attendanceChart, {
    type: "bar",
    data: {
      labels: ["Tepat Waktu", "Terlambat"],
      datasets: [
        {
          label: "Jumlah",
          data: [tepatWaktu, terlambat],
          backgroundColor: ["#10b981", "#ef4444"]
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function bindRealtimeLogs() {
  if (unsubLogs) unsubLogs();

  const q = query(collection(db, "attendance"), orderBy("createdAt", "desc"));
  unsubLogs = onSnapshot(
    q,
    (snapshot) => {
      attendanceLogs = snapshot.docs.map((d) => {
        const data = d.data();
        return {
          id: d.id,
          ...data,
          timeLabel: formatDate(data.createdAt)
        };
      });
      renderTable(attendanceLogs);
      renderChart(attendanceLogs);
    },
    (error) => {
      console.error("Realtime log gagal:", error);
      alert(`Gagal membaca log realtime: ${error.message}`);
    }
  );
}

async function handleAttendance() {
  try {
    if (!currentUser) {
      throw new Error("User belum login.");
    }

    setStatus("Memproses absensi...", "info");
    await loadFaceModels();

    const snapshotBase64 = takeSnapshot(el.video, el.snapshotCanvas);
    const location = await getCurrentLocation();
    const gpsValidation = validateSchoolRadius(location, SCHOOL_COORDINATE, ATTENDANCE_RADIUS);

    if (!gpsValidation.isWithinRadius) {
      throw new Error(`Anda di luar radius sekolah (jarak ${gpsValidation.distance.toFixed(2)} m).`);
    }

    if (!currentUser.faceDescriptor) {
      throw new Error("Face descriptor user belum terdaftar di profile.");
    }

    const faceValidation = await verifyFace(snapshotBase64, currentUser.faceDescriptor);
    if (!faceValidation.match) {
      throw new Error(`Wajah tidak cocok. Jarak descriptor: ${faceValidation.distance.toFixed(4)}.`);
    }

    const status = getStatusByTime(new Date());

    const docPayload = {
      uid: auth.currentUser.uid,
      name: currentUser.name,
      email: currentUser.email,
      status,
      latitude: location.latitude,
      longitude: location.longitude,
      distanceMeters: gpsValidation.distance,
      photoBase64: snapshotBase64,
      createdAt: serverTimestamp()
    };

    await addDoc(collection(db, "attendance"), docPayload);

    setStatus(`Absensi berhasil: ${status}. Notifikasi WA sedang dikirim.`, "ok");

    try {
      await sendWhatsAppNotification({
        token: FONNTE_TOKEN,
        target: currentUser.phone,
        message: `Halo ${currentUser.name}, absensi Anda sukses (${status}) pada ${new Date().toLocaleString("id-ID")}.`
      });
    } catch (waError) {
      setStatus(`Absensi sukses, tetapi WA gagal: ${waError.message}`, "error");
    }
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function hydrateCurrentUser(firebaseUser) {
  const profile = await getUserProfile(firebaseUser.uid);
  if (!profile) throw new Error("Profil user tidak ditemukan.");

  currentUser = {
    uid: firebaseUser.uid,
    email: firebaseUser.email,
    name: profile.name || firebaseUser.email,
    role: profile.role,
    phone: profile.phone || "",
    faceDescriptor: profile.faceDescriptor || null
  };
}

function bindEvents() {
  el.loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const user = await login(el.email.value.trim(), el.password.value.trim());
      currentUser = user;
      setStatus("Login sukses.", "ok");
    } catch (error) {
      alert(error.message);
    }
  });

  el.startCameraBtn.addEventListener("click", async () => {
    try {
      await startCamera(el.video);
      setStatus("Kamera aktif.", "ok");
    } catch (error) {
      setStatus(error.message, "error");
    }
  });

  el.absenBtn.addEventListener("click", handleAttendance);
  el.logoutGuru.addEventListener("click", async () => {
    await logout();
    stopCamera(el.video);
  });

  el.logoutAdmin.addEventListener("click", async () => {
    await logout();
  });

  el.exportExcelBtn.addEventListener("click", () => {
    try {
      exportToExcel(attendanceLogs);
    } catch (error) {
      alert(error.message);
    }
  });

  el.exportPdfBtn.addEventListener("click", () => {
    try {
      exportToPdf(attendanceLogs);
    } catch (error) {
      alert(error.message);
    }
  });

  el.themeToggle.addEventListener("click", () => {
    document.documentElement.classList.toggle("light");
  });
}

observeAuth(async (firebaseUser) => {
  try {
    if (!firebaseUser) {
      currentUser = null;
      if (unsubLogs) unsubLogs();
      setVisible(el.loginSection);
      return;
    }

    await hydrateCurrentUser(firebaseUser);

    if (currentUser.role === "guru") {
      el.guruInfo.textContent = `Login sebagai ${currentUser.name} (${currentUser.email})`;
      setVisible(el.guruSection);
    } else if (currentUser.role === "admin") {
      setVisible(el.adminSection);
      bindRealtimeLogs();
    } else {
      throw new Error("Role user tidak dikenali.");
    }
  } catch (error) {
    alert(error.message);
    await logout();
  }
});

bindEvents();

// util registrasi face descriptor untuk user (jalankan sekali dari console saat onboarding)
window.registerDescriptorForCurrentUser = async function registerDescriptorForCurrentUser() {
  try {
    if (!auth.currentUser) throw new Error("Harus login dulu.");
    await loadFaceModels();
    const base64 = takeSnapshot(el.video, el.snapshotCanvas);
    const descriptor = await verifyFace(base64, await (async () => {
      const img = await faceapi.fetchImage(base64);
      const result = await faceapi
        .detectSingleFace(img, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceDescriptor();
      if (!result) throw new Error("Wajah tidak terdeteksi.");
      return Array.from(result.descriptor);
    })(), 2);

    if (!descriptor.match) {
      throw new Error("Gagal men-generate descriptor.");
    }

    alert("Gunakan Firestore Console untuk menyimpan faceDescriptor ke dokumen users/{uid}.");
  } catch (error) {
    alert(error.message);
  }
};

// contoh query cepat untuk admin (opsional)
window.loadTodayAttendance = async function loadTodayAttendance() {
  try {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const q = query(collection(db, "attendance"), where("createdAt", ">=", today));
    const snap = await getDocs(q);
    console.log(`Log hari ini: ${snap.size}`);
  } catch (error) {
    console.error(error);
  }
};
