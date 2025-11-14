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
  const commitFrequency = (() => {
    if (!report) return null;

    const { status_code, data, error_name, error_message } =
      report.commit_frequency;

    if (status_code === 200) {
      return `${data.toFixed(3)} hrs`;
    } else {
      console.log(`${status_code} - ${error_name} - ${error_message}`);
      return error_message;
    }
  })();

  const issuesCloseTime = (() => {
    if (!report) return null;

    const { status_code, data, error_name, error_message } =
      report.issues_close_time;

    if (status_code === 200) {
      return `${data.toFixed(3)} hrs`;
    } else {
      console.log(`${status_code} - ${error_name} - ${error_message}`);
      return error_message;
    }
  })();

  const pullsCloseTime = (() => {
    if (!report) return null;

    const { status_code, data, error_name, error_message } =
      report.pulls_close_time;

    if (status_code === 200) {
      return `${data.toFixed(3)} hrs`;
    } else {
      console.log(`${status_code} - ${error_name} - ${error_message}`);
      return error_message;
    }
  })();

  const codeChurn = (() => {
    if (!report) return null;

    const { status_code, data, error_name, error_message } = report.code_churn;

    if (status_code === 200) {
      const { additions, deletions, total, net } = data;
      return `
        Additions: ${additions},
        Deletions: ${deletions},
        Total: ${total},
        Net: ${net}
        `;
    } else {
      console.log(`${status_code} - ${error_name} - ${error_message}`);
      return error_message;
    }
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
