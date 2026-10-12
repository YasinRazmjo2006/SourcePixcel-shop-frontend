// lib/utils/export-csv.ts

export interface CsvColumn<T> {
  key: keyof T | string;
  label: string;
  formatter?: (value: unknown, row: T) => string;
}

export function exportToCSV<T extends Record<string, unknown>>(
  data: T[],
  columns: CsvColumn<T>[],
  filename: string
): void {
  if (data.length === 0) return;

  const headers = columns.map((c) => c.label).join(",");

  const rows = data.map((row) =>
    columns
      .map((col) => {
        const value = col.formatter
          ? col.formatter(row[col.key as keyof T], row)
          : String(row[col.key as keyof T] ?? "");
        // Escape quotes and wrap in quotes if contains comma
        const escaped = value.replace(/"/g, '""');
        return /[",\n]/.test(escaped) ? `"${escaped}"` : escaped;
      })
      .join(",")
  );

  // Add BOM for UTF-8 (Excel support)
  const bom = "\uFEFF";
  const csv = bom + [headers, ...rows].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

  downloadBlob(blob, `${filename}.csv`);
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
