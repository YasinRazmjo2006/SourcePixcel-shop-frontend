// lib/utils/export-pdf.ts
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import type { CsvColumn } from "./export-csv";

export interface PdfOptions<T> {
  title: string;
  subtitle?: string;
  data: T[];
  columns: CsvColumn<T>[];
  filename: string;
  locale?: "fa" | "en";
}

export function exportToPDF<T extends Record<string, unknown>>({
  title,
  subtitle,
  data,
  columns,
  filename,
  locale = "fa",
}: PdfOptions<T>): void {
  const doc = new jsPDF({
    orientation: "landscape",
    unit: "mm",
    format: "a4",
  });

  const pageWidth = doc.internal.pageSize.getWidth();

  // Header
  doc.setFillColor(239, 64, 86); // #EF4056
  doc.rect(0, 0, pageWidth, 25, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(18);
  doc.setFont("helvetica", "bold");
  doc.text(title, pageWidth / 2, 12, { align: "center" });

  if (subtitle) {
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(subtitle, pageWidth / 2, 19, { align: "center" });
  }

  // Date
  doc.setTextColor(160, 163, 168);
  doc.setFontSize(9);
  const dateStr =
    locale === "fa"
      ? new Date().toLocaleDateString("fa-IR")
      : new Date().toLocaleDateString("en-US");
  doc.text(`Generated: ${dateStr}`, pageWidth - 10, 32, { align: "right" });

  // Table
  const head = [columns.map((c) => c.label)];
  const body = data.map((row) =>
    columns.map((col) => {
      if (col.formatter) return col.formatter(row[col.key as keyof T], row);
      return String(row[col.key as keyof T] ?? "");
    })
  );

  autoTable(doc, {
    head,
    body,
    startY: 38,
    styles: {
      fontSize: 9,
      cellPadding: 3,
      halign: locale === "fa" ? "right" : "left",
    },
    headStyles: {
      fillColor: [239, 64, 86],
      textColor: [255, 255, 255],
      fontStyle: "bold",
    },
    alternateRowStyles: {
      fillColor: [250, 250, 250],
    },
    margin: { top: 38, left: 10, right: 10 },
    didDrawPage: (data) => {
      // Footer
      const pageCount = doc.getNumberOfPages();
      const pageNum = doc.getCurrentPageInfo().pageNumber;
      doc.setFontSize(8);
      doc.setTextColor(160, 163, 168);
      doc.text(
        `SourcePixcel — Page ${pageNum} of ${pageCount}`,
        pageWidth / 2,
        doc.internal.pageSize.getHeight() - 5,
        { align: "center" }
      );
    },
  });

  doc.save(`${filename}.pdf`);
}
