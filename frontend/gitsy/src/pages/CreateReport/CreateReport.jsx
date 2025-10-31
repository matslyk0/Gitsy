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
  const commit_frequency = report?.commit_frequency;
  const issues_close_time = report?.issues_close_time;
  const pulls_close_time = report?.pulls_close_time;

  const code_churn_valid = report?.code_churn?.success;
  let code_churn;
  if (code_churn_valid === true) {
    code_churn = (
      <ul>
        <li>Additions: {report.code_churn.data.additions}</li>
        <li>Deletions: {report.code_churn.data.deletions}</li>
        <li>Total: {report.code_churn.data.total}</li>
        <li>Net: {report.code_churn.data.net}</li>
      </ul>
    );
  } else if (code_churn_valid === false) {
    code_churn = (
      <p>The repository is too large to calculate its code churn!</p>
    );
  }

  return (
    <div className={styles.reportDisplay}>
      <ul>
        <li>Time Between Commits (hrs): {commit_frequency}</li>
        <li>Issues Close Time (hrs): {issues_close_time}</li>
        <li>Pulls Close Time (hrs): {pulls_close_time}</li>
      </ul>
      Code Churn (Lines of Code): {code_churn}
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
    const enteredUrl = document.getElementById("urlInput").value;
    document.getElementById("urlInput").value = "";
    const params = { repo_url: enteredUrl };

    const baseUrl =
      import.meta.env.MODE === "development" ? "http://localhost:8000" : "/api";
    const endpointUrl = `${baseUrl}/create-report/generate`;

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
