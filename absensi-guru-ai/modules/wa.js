export async function sendWhatsAppNotification({ token, target, message }) {
  try {
    if (!token) throw new Error("Token Fonnte belum diatur.");
    if (!target) throw new Error("Nomor tujuan WhatsApp belum tersedia.");

    const response = await fetch("https://api.fonnte.com/send", {
      method: "POST",
      headers: {
        Authorization: token,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        target,
        message,
        countryCode: "62"
      })
    });

    const result = await response.json();
    if (!response.ok || result.status === false) {
      throw new Error(result.reason || "Fonnte menolak request.");
    }

    return result;
  } catch (error) {
    throw new Error(`Notifikasi WhatsApp gagal: ${error.message}`);
  }
}
