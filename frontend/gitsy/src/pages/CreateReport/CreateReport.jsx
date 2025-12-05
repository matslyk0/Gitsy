import styles from "./CreateReport.module.css";

import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Card from "../../components/Card/Card.jsx";

import axios from "axios";
import React, { useState } from "react";

function ReportForm({ url, setUrl, onAnalyse, disabled }) {
  return (
    <div className={styles.reportForm}>
      <input
        disabled={disabled}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter a GitHub Repo URL"
        type="text"
        value={url}
      />
      <button onClick={onAnalyse}>Analyse</button>
    </div>
  );
}

function FormatMetric(metric) {}

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
  const [url, setUrl] = useState("");
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  async function onAnalyse() {
    if (!url) return;

    setIsLoading(true);
    const params = { repo_url: url };
    setUrl("");

    const apiUrl =
      import.meta.env.MODE === "development"
        ? "http://localhost:8000/create-report/generate"
        : "/api/create-report/generate";

    try {
      const response = await axios.get(apiUrl, { params: params });
      setReport(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <Banner />
      <main className={styles.main}>
        <h1 className={styles.createReportHeader}>Create a Report Here</h1>

        <ReportForm
          url={url}
          setUrl={setUrl}
          onAnalyse={onAnalyse}
          disabled={isLoading}
        />

        <div>
          {isLoading && (
            <h2 className={styles.reportStatus}> Processing... </h2>
          )}
        </div>

        <ReportDisplay report={report} />
      </main>
      <Footer />
    </>
  );
}
