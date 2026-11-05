import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";

// Importe de CSS base entra na tarefa 2 (design system — ADR-002).
const raiz = document.getElementById("root");
if (!raiz) {
  throw new Error("Elemento #root ausente no index.html");
}

createRoot(raiz).render(
  <StrictMode>
    <App />
  </StrictMode>
);
