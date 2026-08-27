import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { StatusBadge } from "./StatusBadge";

describe("StatusBadge", () => {
  it("renders skipped state clearly", () => {
    render(<StatusBadge status="SKIPPED" />);
    expect(screen.getByText("Omitido")).toBeInTheDocument();
  });
});
