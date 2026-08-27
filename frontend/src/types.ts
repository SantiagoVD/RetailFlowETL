export const DATASETS = ["sales", "customers", "products", "stores", "payments", "inventory"] as const;
export type Dataset = (typeof DATASETS)[number];
export type RunStatus = "UPLOADING" | "PROCESSING" | "SUCCESS" | "FAILED" | "SKIPPED";

export interface RunSummary {
  run_id: string;
  upload_id?: string | null;
  original_run_id?: string | null;
  dataset: Dataset;
  source_file: string;
  status: RunStatus;
  records_received: number;
  records_valid: number;
  records_rejected: number;
  start_time: string;
  end_time?: string | null;
  duration_ms?: number | null;
}

export interface RunDetail extends RunSummary {
  bronze_key?: string | null;
  silver_key?: string | null;
  gold_keys: string[];
  quarantine_key?: string | null;
  error_message?: string | null;
}

export interface UploadAuthorization {
  upload_id: string;
  dataset: Dataset;
  file_name: string;
  object_key: string;
  upload_url: string;
  fields: Record<string, string>;
  expires_in: number;
  max_upload_bytes: number;
}

export interface UploadStatus {
  upload_id: string;
  run_id?: string;
  original_run_id?: string | null;
  dataset?: Dataset;
  status: RunStatus;
  records_received?: number;
  records_valid?: number;
  records_rejected?: number;
}

export interface ResultPreview {
  run_id: string;
  dataset: Dataset;
  total_records: number;
  preview_count: number;
  columns: string[];
  rows: Record<string, unknown>[];
  source_key: string;
}

export interface ErrorSummary {
  run_id: string;
  records_rejected: number;
  summary: Record<string, number>;
  preview: { record_id: unknown; error_codes: string[]; error_messages: string[] }[];
}

export interface DownloadResponse {
  download_url: string;
  expires_in: number;
}
