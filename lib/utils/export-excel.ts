// lib/utils/export-excel.ts
import * as XLSX from "xlsx";
import type { CsvColumn } from "./export-csv";

export function exportToExcel<T>(
  data: T[],
  columns: CsvColumn<T>[],
  filename: string,
  sheetName = "Sheet1"
): void {
  if (data.length === 0) return;

  const rows = data.map((row) => {
    const obj: Record<string, string | number> = {};
    columns.forEach((col) => {
      const value = col.formatter
        ? col.formatter((row as Record<string, unknown>)[col.key], row)
        : ((row as Record<string, unknown>)[col.key] as string | number) ?? "";
      obj[col.label] = value;
    });
    return obj;
  });

  const worksheet = XLSX.utils.json_to_sheet(rows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

  const colWidths = columns.map((col) => ({
    wch: Math.max(col.label.length, 15),
  }));
  worksheet["!cols"] = colWidths;

  XLSX.writeFile(workbook, `${filename}.xlsx`);
}