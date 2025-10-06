import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Home from "./pages/Home.jsx";
import GetStarted from "./pages/GetStarted.jsx";
import CreateReport from "./pages/CreateReport.jsx";
import Login from "./pages/Login.jsx";
import SignUp from "./pages/SignUp.jsx";
import "./index.css";

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/get-started", element: <GetStarted /> },
  { path: "/create-report", element: <CreateReport /> },
  { path: "/login", element: <Login /> },
  { path: "/sign-up", element: <SignUp /> },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
