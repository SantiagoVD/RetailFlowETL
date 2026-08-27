import { describe, expect, it } from "vitest";
import { validateFile } from "./uploadValidation";

describe("upload validation", () => {
  it("accepts supported files within the size limit", () => {
    expect(validateFile(new File(["sale_id\n1"], "sales.csv", { type: "text/csv" }), "sales")).toBeNull();
  });
  it("rejects unsupported extensions and oversized files", () => {
    expect(validateFile(new File(["x"], "sales.exe"), "sales")).toContain("CSV");
    expect(validateFile(new File([new Uint8Array(10 * 1024 * 1024 + 1)], "sales.csv"), "sales")).toContain("10 MB");
  });
});
