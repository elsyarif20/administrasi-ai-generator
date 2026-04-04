function toRad(degree) {
  return (degree * Math.PI) / 180;
}

export function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

export async function getCurrentLocation() {
  try {
    if (!navigator.geolocation) {
      throw new Error("Browser tidak mendukung geolocation.");
    }

    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        reject,
        { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
      );
    });

    return {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      accuracy: position.coords.accuracy
    };
  } catch (error) {
    if (error.code === 1) {
      throw new Error("Izin GPS ditolak oleh pengguna.");
    }
    throw new Error(`Gagal mengambil lokasi: ${error.message}`);
  }
}

export function validateSchoolRadius(current, school, radiusMeters = 100) {
  const distance = haversineDistance(
    current.latitude,
    current.longitude,
    school.latitude,
    school.longitude
  );

  return {
    isWithinRadius: distance <= radiusMeters,
    distance
  };
}
