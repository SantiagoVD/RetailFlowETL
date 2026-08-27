import { useRef, useState } from "react";
import { AlertCircle, ArrowRight, CheckCircle2, FileSpreadsheet, FileUp, LoaderCircle, UploadCloud } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { StatusBadge } from "../components/StatusBadge";
import { DATASETS, type Dataset, type RunStatus } from "../types";
import { validateFile } from "../features/uploads/uploadValidation";

const datasetLabels: Record<Dataset, string> = { sales: "Ventas", customers: "Clientes", products: "Productos", stores: "Tiendas", payments: "Pagos", inventory: "Inventario" };

function delay(ms: number) { return new Promise((resolve) => window.setTimeout(resolve, ms)); }

export function UploadPage() {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [dataset, setDataset] = useState<Dataset>("sales");
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<RunStatus | null>(null);
  const [dragging, setDragging] = useState(false);

  const chooseFile = (next: File | undefined) => {
    setError(null);
    const validationError = validateFile(next || null, dataset);
    if (validationError) { setFile(null); setError(validationError); return; }
    setFile(next || null);
  };

  const process = async () => {
    const validationError = validateFile(file, dataset);
    if (validationError) { setError(validationError); return; }
    if (!file) return;
    try {
      setError(null); setStatus("UPLOADING");
      const authorization = await api.createUpload({ dataset, file_name: file.name, content_type: file.type || "application/octet-stream" });
      await api.uploadToS3(authorization, file);
      setStatus("PROCESSING");
      for (let attempt = 0; attempt < 120; attempt += 1) {
        const current = await api.getUploadStatus(authorization.upload_id);
        if (current.status === "SUCCESS" || current.status === "FAILED" || current.status === "SKIPPED") {
          setStatus(current.status);
          if (current.run_id) navigate(`/runs/${current.run_id}`);
          return;
        }
        await delay(2500);
      }
      setError("El procesamiento tardó demasiado. Vuelve a intentarlo más tarde.");
      setStatus(null);
    } catch (caught) {
      setStatus(null); setError(caught instanceof Error ? caught.message : "La solicitud de procesamiento falló");
    }
  };

  return <section className="page-section upload-page">
    <div className="section-heading"><div><span className="eyebrow">NUEVA EJECUCIÓN</span><h1>Subir un conjunto de datos</h1><p>Inicia una ejecución ETL asíncrona desde una frontera de entrada S3 controlada.</p></div><div className="api-state"><span />API conectada</div></div>
    <div className="upload-layout">
      <div className="form-panel">
        <label className="field-label" htmlFor="dataset">Conjunto de datos</label>
        <select id="dataset" className="select-control" value={dataset} onChange={(event) => setDataset(event.target.value as Dataset)} disabled={status !== null}>
          {DATASETS.map((item) => <option value={item} key={item}>{datasetLabels[item]}</option>)}
        </select>
        <div className="field-row"><span className="field-label">Archivo de origen</span><span className="field-hint">CSV · JSON · XLSX / máx. 10 MB</span></div>
        <button type="button" className={`dropzone ${dragging ? "dragging" : ""}`} onClick={() => inputRef.current?.click()} onDragOver={(event) => { event.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); chooseFile(event.dataTransfer.files[0]); }} disabled={status !== null}>
          <input ref={inputRef} type="file" hidden accept=".csv,.json,.xlsx" onChange={(event) => chooseFile(event.target.files?.[0])} />
          {file ? <><div className="file-icon"><FileUp size={22} /></div><strong>{file.name}</strong><span>{(file.size / 1024).toFixed(1)} KB · Listo para subir</span></> : <><div className="upload-icon"><UploadCloud size={28} /></div><strong>Suelta un archivo aquí</strong><span>o búscalo en este dispositivo</span></>}
        </button>
        <div className="example-download"><FileSpreadsheet size={17} /><span>¿No tienes un archivo?</span><a href="/examples/retailflow_ventas_ejemplo.xlsx" download>Descarga un Excel de ejemplo</a></div>
        {error && <div className="inline-error"><AlertCircle size={16} />{error}</div>}
        <button type="button" className="primary-button" onClick={process} disabled={!file || status !== null}>{status === "UPLOADING" ? <><LoaderCircle className="spin" size={17} />Autorizando subida</> : status === "PROCESSING" ? <><LoaderCircle className="spin" size={17} />Procesando ETL</> : <><ArrowRight size={17} />Procesar conjunto de datos</>}</button>
      </div>
      <div className="run-rail">
        <div className="rail-heading"><span className="eyebrow">FLUJO ETL</span><span className="rail-note">Asíncrono</span></div>
        <div className={`rail-step ${status ? "is-active" : ""}`}><div className="rail-icon"><UploadCloud size={17} /></div><div><strong>Entrada</strong><span>Subida S3 prefirmada</span></div>{status === "UPLOADING" ? <LoaderCircle className="spin rail-state" size={16} /> : status ? <CheckCircle2 className="rail-state complete" size={16} /> : <span className="rail-state pending" />}</div>
        <div className={`rail-step ${status === "PROCESSING" ? "is-active" : ""}`}><div className="rail-icon"><LoaderCircle size={17} /></div><div><strong>Procesamiento ETL</strong><span>Bronze · Calidad · Silver · Gold</span></div>{status === "PROCESSING" ? <LoaderCircle className="spin rail-state" size={16} /> : status && status !== "UPLOADING" ? <CheckCircle2 className="rail-state complete" size={16} /> : <span className="rail-state pending" />}</div>
        <div className={`rail-step ${status === "SUCCESS" || status === "SKIPPED" || status === "FAILED" ? "is-active" : ""}`}><div className="rail-icon"><CheckCircle2 size={17} /></div><div><strong>Resultado</strong><span>Metadatos y salidas descargables</span></div>{status === "SUCCESS" || status === "SKIPPED" ? <StatusBadge status={status} /> : status === "FAILED" ? <StatusBadge status={status} /> : <span className="rail-state pending" />}</div>
        <div className="rail-footer"><CheckCircle2 size={15} /><span>Los archivos nunca pasan por API Gateway. El navegador los sube directamente a S3.</span></div>
      </div>
    </div>
  </section>;
}
