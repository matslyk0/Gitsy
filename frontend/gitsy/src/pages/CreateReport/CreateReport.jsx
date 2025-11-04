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
  const errorMessages = {
    "InsufficientDataError()": "Not enough data!",
    "GitHubAPIError()": "GitHub request failed!",
    "GitHubTimeOutError()": "GitHub took too long!",
    "RepoTooLargeError()": "Repository must be under 10,000 commits!",
  };

  const commitFrequency =
    errorMessages[report?.commit_frequency] ?? report?.commit_frequency;
  const issuesCloseTime =
    errorMessages[report?.issues_close_time] ?? report?.issues_close_time;
  const pullsCloseTime =
    errorMessages[report?.pulls_close_time] ?? report?.pulls_close_time;

  let codeChurn = "";
  if (errorMessages[report?.code_churn] == null) {
    if (report?.code_churn != null) {
      codeChurn = (
        <ul>
          <li>Additions: {report?.code_churn?.additions}</li>
          <li>Deletions: {report?.code_churn?.deletions}</li>
          <li>Total: {report?.code_churn?.total}</li>
          <li>Net: {report?.code_churn?.net}</li>
        </ul>
      );
    }
  } else {
    codeChurn = errorMessages[report?.code_churn];
  }

  return (
    <div className={styles.reportDisplay}>
      <ul>
        <li>Time Between Commits (hrs): {commitFrequency}</li>
        <li>Issues Close Time (hrs): {issuesCloseTime}</li>
        <li>Pulls Close Time (hrs): {pullsCloseTime}</li>
      </ul>
      Code Churn (Lines of Code): {codeChurn}
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
