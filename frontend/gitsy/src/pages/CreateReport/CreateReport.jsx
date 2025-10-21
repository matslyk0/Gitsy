import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import styles from "./CreateReport.module.css";
import axios from "axios";
import React, { useState } from "react";

function CreateReportForm({ onClick }) {
  return (
    <div className={styles.createReportForm}>
      <input type="text" id="urlInput" placeholder="Enter github repo url" />
      <button onClick={onClick}>Analyse</button>
    </div>
  );
}

function ReportDisplay({ report }) {
  return (
    <div className={styles.reportDisplay}>
      <ul>
        <li>Time Between Commits (hrs): {report?.commit_frequency}</li>
        <li>
          Code Churn (Lines of Code):
          <ul>
            <li>Additions: {report?.code_churn?.additions}</li>
            <li>Deletions: {report?.code_churn?.deletions}</li>
            <li>Total: {report?.code_churn?.total}</li>
            <li>Net: {report?.code_churn?.net}</li>
          </ul>
        </li>
        <li>Issues Close Time (hrs): {report?.issues_close_time}</li>
        <li>Pulls Close Time (hrs): {report?.pulls_close_time}</li>
      </ul>
    </div>
  );
}

export default function CreateReport() {
  const mainStyle = {
    alignItems: "center",
    border: "0px solid white" /* for debugging */,
    display: "flex",
    flexDirection: "column",
    flex: "1",
    justifyContent: "center",
  };

  const [report, setReport] = useState([]);

  async function CallAnalysisFunction() {
    const baseUrl =
      import.meta.env.MODE === "development" ? "http://localhost:8000" : "/api";

    const enteredUrl = document.getElementById("urlInput").value;
    document.getElementById("urlInput").value = "";

    const endpointUrl = "${baseUrl}/create-report/generate";
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
      <main style={mainStyle}>
        <h1 className={styles.createReportHeader}>Create a Report Here</h1>
        <CreateReportForm onClick={CallAnalysisFunction} />
        <ReportDisplay report={report} />
      </main>
      <Footer />
    </>
  );
}
