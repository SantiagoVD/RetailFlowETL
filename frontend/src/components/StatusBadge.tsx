import { CheckCircle2, CircleAlert, CircleDashed, Clock3, SkipForward } from "lucide-react";
import type { RunStatus } from "../types";

const labels: Record<RunStatus, string> = { SUCCESS: "Éxito", FAILED: "Fallido", SKIPPED: "Omitido", PROCESSING: "Procesando", UPLOADING: "Subiendo" };

export function StatusBadge({ status }: { status: RunStatus }) {
  const icon = status === "SUCCESS" ? <CheckCircle2 size={14} /> : status === "FAILED" ? <CircleAlert size={14} /> : status === "SKIPPED" ? <SkipForward size={14} /> : status === "PROCESSING" ? <Clock3 size={14} /> : <CircleDashed size={14} />;
  return <span className={`status-badge status-${status.toLowerCase()}`}>{icon}{labels[status]}</span>;
}
