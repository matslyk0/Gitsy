import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Home from "./pages/Home/Home.jsx";
import GetStarted from "./pages/GetStarted/GetStarted.jsx";
import CreateReport from "./pages/CreateReport/CreateReport.jsx";
import Login from "./pages/Login/Login.jsx";
import SignUp from "./pages/SignUp/SignUp.jsx";
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
