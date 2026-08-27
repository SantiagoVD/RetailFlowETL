export function MetricStrip({ received, valid, rejected }: { received: number; valid: number; rejected: number }) {
  return <div className="metric-strip">
    <div className="metric"><span>Recibidos</span><strong>{received.toLocaleString()}</strong></div>
    <div className="metric metric-valid"><span>Válidos</span><strong>{valid.toLocaleString()}</strong></div>
    <div className="metric metric-rejected"><span>Rechazados</span><strong>{rejected.toLocaleString()}</strong></div>
  </div>;
}
