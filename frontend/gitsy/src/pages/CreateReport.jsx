import Banner from "../components/Banner/Banner.jsx";
import Footer from "../components/Footer/Footer.jsx";
import axios from "axios";
import React, { useState } from "react";

export default function CreateReport() {
  const [report, setReport] = useState([]);

  async function CallAnalysisFunction() {
    const enteredUrl = document.getElementById("urlInput").value;
    document.getElementById("urlInput").value = "";

    const endpointUrl = "http://localhost:8000/create-report/generate";
    const params = { repo_url: enteredUrl };

    try {
      const response = await axios.get(endpointUrl, { params: params });
      setReport(response.data);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <>
      <Banner />
      <main>
        <h1 style={{ color: "white" }}>Create Report Below</h1>
        <input type="text" id="urlInput" placeholder="Enter github repo url" />
        <button onClick={CallAnalysisFunction}>Analyse</button>;
        <ul style={{ color: "white" }}>
          <li>Time Between Commits (hrs): {report.commit_frequency}</li>
          <li>
            Code Churn (Lines of Code):
            <ul>
              <li>Additions: {report?.code_churn?.additions}</li>
              <li>Deletions: {report?.code_churn?.deletions}</li>
              <li>Total: {report?.code_churn?.total}</li>
              <li>Net: {report?.code_churn?.net}</li>
            </ul>
          </li>
          <li>Issues Close Time (hrs): {report.issues_close_times}</li>
          <li>Pulls Close Time (hrs): {report.pulls_close_times}</li>
        </ul>
      </main>
      <Footer />
    </>
  );
}
