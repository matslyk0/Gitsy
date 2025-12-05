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

function FormatMetric(metric) {
  const { status_code, data, error_name, error_message } = metric;

  if (status_code !== 200) return error_message;

  // do not round the metric if it is an object, e.g. code churn
  if (typeof data === "object") return data;

  return data.toFixed(3);
}

function ReportDisplay({ report }) {
  if (!report) return null;

  const commitFrequency = FormatMetric(report.commit_frequency);
  const issuesCloseTime = FormatMetric(report.issues_close_time);
  const pullsCloseTime = FormatMetric(report.pulls_close_time);
  const codeChurn = FormatMetric(report.code_churn);

  return (
    <div className={styles.reportDisplay}>
      <Card
        metricName="Commit Frequency"
        metricData={`On average, this repository has 
          a commit every ${commitFrequency} hours.`}
      />
      <Card
        metricName="Issues Close Time"
        metricData={`On average, this repository closes 
          Issues every ${issuesCloseTime} hours.`}
      />
      <Card
        metricName="Pulls Close Time"
        metricData={`On average, this repository closes 
          Pull Requests every ${pullsCloseTime} hours.`}
      />
      <Card
        metricName="Code Churn"
        metricData={`This repository has 
          ${codeChurn.additions} additions, 
          ${codeChurn.deletions} deletions, 
          totaling at ${codeChurn.total} line changes, 
          with a net of ${codeChurn.net} lines.`}
      />
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
