import { useEffect, useMemo, useState } from "react";
import { ArrowLeft, CheckCircle2, CircleAlert, Download, ExternalLink, FileWarning, LoaderCircle, SkipForward } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import { MetricStrip } from "../components/MetricStrip";
import { StatusBadge } from "../components/StatusBadge";
import type { Dataset, ErrorSummary, ResultPreview, RunDetail } from "../types";

const datasetLabels: Record<Dataset, string> = { sales: "Ventas", customers: "Clientes", products: "Productos", stores: "Tiendas", payments: "Pagos", inventory: "Inventario" };

export function RunDetailPage() {
  const { runId = "" } = useParams();
  const [run, setRun] = useState<RunDetail | null>(null);
  const [result, setResult] = useState<ResultPreview | null>(null);
  const [errors, setErrors] = useState<ErrorSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    const load = async () => {
      try {
        const current = await api.getRun(runId);
        if (!alive) return;
        setRun(current);
        const artifactRun = current.status === "SKIPPED" && current.original_run_id ? current.original_run_id : current.run_id;
        if (current.status === "SUCCESS" || current.status === "SKIPPED") {
          const [preview, quality] = await Promise.all([
            api.getResult(artifactRun).catch(() => null),
            current.records_rejected ? api.getErrors(artifactRun).catch(() => null) : Promise.resolve(null),
          ]);
          if (alive) { setResult(preview); setErrors(quality); }
        } else if (current.records_rejected > 0) {
          if (alive) setErrors(await api.getErrors(current.run_id));
        }
      } catch (caught) {
        if (alive) setError(caught instanceof Error ? caught.message : "No se pudo cargar esta ejecución");
      } finally {
        if (alive) setLoading(false);
      }
    };
    void load();
    return () => { alive = false; };
  }, [runId]);

  const artifactRunId = useMemo(() => run?.status === "SKIPPED" && run.original_run_id ? run.original_run_id : run?.run_id, [run]);
  const download = async (quarantine = false) => {
    if (!artifactRunId) return;
    const response = quarantine ? await api.getQuarantineDownload(artifactRunId) : await api.getDownload(artifactRunId);
    window.open(response.download_url, "_blank", "noopener,noreferrer");
  };

  if (loading) return <section className="loading-page"><LoaderCircle className="spin" size={21} />Cargando detalle de ejecución</section>;
  if (error || !run) return <section className="page-section"><div className="inline-error"><CircleAlert size={17} />{error || "Ejecución no encontrada"}</div><Link className="back-link" to="/"><ArrowLeft size={16} />Nueva carga</Link></section>;

  return <section className="page-section detail-page">
    <Link className="back-link" to="/"><ArrowLeft size={16} />Nueva carga</Link>
    <div className="detail-heading">
      <div>
        <span className="eyebrow">DETALLE DE EJECUCIÓN</span>
        <h1>{datasetLabels[run.dataset]} <span className="slash">/</span> {run.source_file}</h1>
        <div className="run-id-line">{run.run_id}{run.upload_id && <><span>·</span>{run.upload_id}</>}</div>
      </div>
      <StatusBadge status={run.status} />
    </div>
    {run.status === "SKIPPED" && (
      <div className="info-banner">
        <SkipForward size={18} />
        <div><strong>Contenido ya procesado</strong><span>Esta subida se omitió por idempotencia SHA-256. Abajo se muestra el resultado original.</span></div>
        {run.original_run_id && <Link to={`/runs/${run.original_run_id}`} className="text-link">Ver ejecución original <ExternalLink size={14} /></Link>}
      </div>
    )}
    {run.status === "FAILED" && <div className="error-banner"><CircleAlert size={18} /><div><strong>ETL falló</strong><span>{run.error_message || "El pipeline reportó un fallo."}</span></div></div>}
    <MetricStrip received={run.records_received} valid={run.records_valid} rejected={run.records_rejected} />
    <div className="detail-meta"><div><span>Inicio</span><strong>{new Date(run.start_time).toLocaleString()}</strong></div><div><span>Fin</span><strong>{run.end_time ? new Date(run.end_time).toLocaleString() : "—"}</strong></div><div><span>Duración</span><strong>{run.duration_ms == null ? "—" : `${(run.duration_ms / 1000).toFixed(2)} segundos`}</strong></div></div>
    {result && <section className="output-section"><div className="subsection-heading"><div><span className="eyebrow">SALIDA GOLD</span><h2>Vista previa Gold</h2></div><button className="secondary-button" onClick={() => void download()}><Download size={16} />Descargar Gold</button></div><div className="preview-note">Mostrando {result.preview_count.toLocaleString()} de {result.total_records.toLocaleString()} registros <span>·</span> {result.source_key.split("/").slice(0, 2).join("/")}</div><div className="table-frame preview-table"><table><thead><tr>{result.columns.map((column) => <th key={column}>{column}</th>)}</tr></thead><tbody>{result.rows.map((row, index) => <tr key={index}>{result.columns.map((column) => <td key={column}>{String(row[column] ?? "—")}</td>)}</tr>)}</tbody></table></div></section>}
    {errors && <section className="output-section quality-section"><div className="subsection-heading"><div><span className="eyebrow">CALIDAD DE DATOS</span><h2>Registros rechazados</h2></div><button className="secondary-button" onClick={() => void download(true)}><Download size={16} />Descargar Cuarentena</button></div><div className="quality-summary">{Object.entries(errors.summary).map(([code, count]) => <div key={code}><FileWarning size={15} /><strong>{code}</strong><span>{count}</span></div>)}</div><div className="table-frame"><table><thead><tr><th>Registro</th><th>Códigos de error</th><th>Mensajes</th></tr></thead><tbody>{errors.preview.map((item, index) => <tr key={index}><td>{String(item.record_id ?? "—")}</td><td>{item.error_codes.join(", ")}</td><td>{item.error_messages.join("; ")}</td></tr>)}</tbody></table></div></section>}
    {!result && !errors && run.status === "SUCCESS" && <div className="empty-output"><CheckCircle2 size={18} />La ejecución terminó correctamente sin vista previa Gold ni salida de calidad.</div>}
  </section>;
}
