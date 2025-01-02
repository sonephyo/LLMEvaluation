import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Error } from "./pages/Error.tsx";
import { GeneratePrompt } from "./pages/generate-prompt/GeneratePrompt.tsx";
import { Analysis } from "./pages/analysis/Analysis.tsx";
import { PromptStorage } from "./pages/prompt storage/PromptStorage.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/prompt",
        element: <GeneratePrompt />,
      },
      {
        path: "/analysis",
        element: <Analysis />,
      },
      {
        path: "/data",
        element: <PromptStorage />,
      },
    ],
    errorElement: <Error />,
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
