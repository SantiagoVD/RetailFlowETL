import type { Dataset, DownloadResponse, ErrorSummary, ResultPreview, RunDetail, RunSummary, UploadAuthorization, UploadStatus } from "../types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:3000").replace(/\/$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    });
  } catch {
    throw new Error("No se pudo conectar con el API");
  }
  const body = (await response.json().catch(() => ({}))) as { error?: { message?: string } } & T;
  if (!response.ok) {
    throw new Error(body.error?.message || "La solicitud al API falló");
  }
  return body;
}

export const api = {
  createUpload: (payload: { dataset: Dataset; file_name: string; content_type: string }) =>
    request<UploadAuthorization>("/uploads", { method: "POST", body: JSON.stringify(payload) }),
  uploadToS3: async (authorization: UploadAuthorization, file: File) => {
    const form = new FormData();
    Object.entries(authorization.fields).forEach(([key, value]) => form.append(key, value));
    form.append("file", file);
    let response: Response;
    try {
      response = await fetch(authorization.upload_url, { method: "POST", body: form });
    } catch {
      throw new Error("No se pudo subir el archivo a S3. Verifica la conexión e inténtalo nuevamente.");
    }
    if (!response.ok) throw new Error("No se pudo subir el archivo a S3");
  },
  getUploadStatus: (uploadId: string) => request<UploadStatus>(`/uploads/${encodeURIComponent(uploadId)}`),
  listRuns: (limit = 50) => request<{ items: RunSummary[] }>(`/runs?limit=${limit}`),
  getRun: (runId: string) => request<RunDetail>(`/runs/${encodeURIComponent(runId)}`),
  getResult: (runId: string, limit = 50) => request<ResultPreview>(`/runs/${encodeURIComponent(runId)}/result?limit=${limit}`),
  getErrors: (runId: string, limit = 50) => request<ErrorSummary>(`/runs/${encodeURIComponent(runId)}/errors?limit=${limit}`),
  getDownload: (runId: string) => request<DownloadResponse>(`/runs/${encodeURIComponent(runId)}/download`),
  getQuarantineDownload: (runId: string) => request<DownloadResponse>(`/runs/${encodeURIComponent(runId)}/quarantine-download`),
};
