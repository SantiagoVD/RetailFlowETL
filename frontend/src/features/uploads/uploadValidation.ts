import type { Dataset } from "../../types";

export const MAX_UPLOAD_BYTES = 10 * 1024 * 1024;
export const ALLOWED_EXTENSIONS = [".csv", ".json", ".xlsx"];

export function validateFile(file: File | null, dataset: Dataset): string | null {
  if (!file) return "Selecciona un archivo antes de iniciar la ejecución";
  if (file.size > MAX_UPLOAD_BYTES) return "El archivo supera el límite de 10 MB";
  const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
  if (!ALLOWED_EXTENSIONS.includes(extension)) return "Solo se admiten archivos CSV, JSON y XLSX";
  if (file.name.includes("/") || file.name.includes("\\") || file.name.startsWith(".")) return "Usa un nombre simple, sin rutas";
  if (!file.name.trim()) return "El nombre del archivo es obligatorio";
  void dataset;
  return null;
}
