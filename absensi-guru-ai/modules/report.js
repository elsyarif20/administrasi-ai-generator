export function exportToExcel(records) {
  try {
    const rows = records.map((r) => ({
      Waktu: r.timeLabel,
      Nama: r.name,
      Status: r.status,
      "Jarak (m)": r.distanceMeters?.toFixed?.(2) ?? "-",
      Latitude: r.latitude,
      Longitude: r.longitude
    }));

    const worksheet = XLSX.utils.json_to_sheet(rows);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Absensi");
    XLSX.writeFile(workbook, `laporan-absensi-${Date.now()}.xlsx`);
  } catch (error) {
    throw new Error(`Export Excel gagal: ${error.message}`);
  }
}

export function exportToPdf(records) {
  try {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ orientation: "landscape" });
    doc.setFontSize(14);
    doc.text("Laporan Absensi Guru AI", 14, 14);

    let y = 24;
    doc.setFontSize(10);
    records.forEach((r, idx) => {
      const line = `${idx + 1}. ${r.timeLabel} | ${r.name} | ${r.status} | ${r.distanceMeters?.toFixed?.(2) ?? "-"} m`;
      doc.text(line, 14, y);
      y += 7;
      if (y > 190) {
        doc.addPage();
        y = 20;
      }
    });

    doc.save(`laporan-absensi-${Date.now()}.pdf`);
  } catch (error) {
    throw new Error(`Export PDF gagal: ${error.message}`);
  }
}
