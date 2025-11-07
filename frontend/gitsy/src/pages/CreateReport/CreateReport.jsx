import styles from "./CreateReport.module.css";

import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Card from "../../components/Card/Card.jsx";

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
    InsufficientDataError: "Not enough data!",
    GitHubAPIError: "GitHub request failed!",
    GitHubTimeOutError: "GitHub took too long!",
    RepoTooLargeError: "Repository must be under 10,000 commits!",
  };

  const commitFrequency = (() => {
    if (!report) return null;

    const { data, error } = report.commit_frequency;
    if (error) return errorMessages[error] || "Unknown error occurred!";

    return data;
  })();
  const issuesCloseTime = (() => {
    if (!report) return null;

    const { data, error } = report.issues_close_time;
    if (error) return errorMessages[error] || "Unknown error occurred!";

    return data;
  })();
  const pullsCloseTime = (() => {
    if (!report) return null;

    const { data, error } = report.pulls_close_time;
    if (error) return errorMessages[error] || "Unknown error occurred!";

    return data;
  })();
  const codeChurn = (() => {
    if (!report) return null;

    const { data, error } = report.code_churn;
    if (error) return errorMessages[error] || "Unknown error occurred!";

    const { additions, deletions, total, net } = data;
    return `
      Additions: ${additions},
      Deletions: ${deletions},
      Total: ${total},
      Net: ${net}
      `;
  })();

  return (
    <div className={styles.reportDisplay}>
      <Card metricName="Commit Frequency" metricData={commitFrequency} />
      <Card metricName="Issues Close Time" metricData={issuesCloseTime} />
      <Card metricName="Pulls Close Time" metricData={pullsCloseTime} />
      <Card metricName="Code Churn" metricData={codeChurn} />
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

  const [report, setReport] = useState(null);

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
