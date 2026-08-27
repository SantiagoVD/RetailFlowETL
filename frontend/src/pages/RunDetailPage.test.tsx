import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import { RunDetailPage } from "./RunDetailPage";

describe("RunDetailPage", () => {
  afterEach(() => vi.restoreAllMocks());

  it("shows quality output when a successful run has no Gold", async () => {
    vi.spyOn(api, "getRun").mockResolvedValue({
      run_id: "RUN-invalid",
      dataset: "sales",
      source_file: "invalid.csv",
      status: "SUCCESS",
      records_received: 4,
      records_valid: 0,
      records_rejected: 4,
      start_time: "2026-01-01T00:00:00Z",
      end_time: "2026-01-01T00:00:01Z",
      duration_ms: 1000,
      gold_keys: [],
      quarantine_key: "quarantine/sales/run.parquet",
    });
    vi.spyOn(api, "getResult").mockRejectedValue(new Error("Gold is unavailable"));
    vi.spyOn(api, "getErrors").mockResolvedValue({ run_id: "RUN-invalid", records_rejected: 4, summary: { OUT_OF_RANGE: 4 }, preview: [] });
    render(<MemoryRouter initialEntries={["/runs/RUN-invalid"]}><Routes><Route path="/runs/:runId" element={<RunDetailPage />} /></Routes></MemoryRouter>);
    await waitFor(() => expect(screen.getByText("Registros rechazados")).toBeInTheDocument());
    expect(screen.queryByText("La ejecución terminó correctamente sin vista previa Gold ni salida de calidad.")).not.toBeInTheDocument();
  });
});
