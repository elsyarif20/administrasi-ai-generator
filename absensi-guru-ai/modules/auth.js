import {
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { doc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { auth, db } from "../config/firebase.js";

export async function login(email, password) {
  try {
    const cred = await signInWithEmailAndPassword(auth, email, password);
    const profileRef = doc(db, "users", cred.user.uid);
    const profileSnap = await getDoc(profileRef);

    if (!profileSnap.exists()) {
      throw new Error("Profil pengguna tidak ditemukan pada collection users.");
    }

    const userData = profileSnap.data();
    if (!["guru", "admin"].includes(userData.role)) {
      throw new Error("Role tidak valid. Role harus guru/admin.");
    }

    return {
      uid: cred.user.uid,
      email: cred.user.email,
      name: userData.name || cred.user.email,
      role: userData.role,
      phone: userData.phone || ""
    };
  } catch (error) {
    throw new Error(`Login gagal: ${error.message}`);
  }
}

export async function logout() {
  try {
    await signOut(auth);
  } catch (error) {
    throw new Error(`Logout gagal: ${error.message}`);
  }
}

export function observeAuth(callback) {
  return onAuthStateChanged(auth, callback);
}

export async function getUserProfile(uid) {
  try {
    const ref = doc(db, "users", uid);
    const snap = await getDoc(ref);
    if (!snap.exists()) {
      return null;
    }
    return snap.data();
  } catch (error) {
    throw new Error(`Gagal ambil profil: ${error.message}`);
  }
}
