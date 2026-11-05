import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "./App";

// CA-01 (pré-condição): a aplicação renderiza sem erro com TypeScript strict.
describe("test_ca_01_fundacao", () => {
  it("test_ca_01_app_renderiza_sem_erro", () => {
    render(<App />);
    expect(screen.getByText("Stable")).toBeInTheDocument();
  });
});
