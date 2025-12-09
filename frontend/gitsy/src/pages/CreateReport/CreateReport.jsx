import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Card from "../../components/Card/Card.jsx";
import styles from "./CreateReport.module.css";
import loadingWheel from "../../assets/bars.svg";

import axios from "axios";
import { useState } from "react";

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
      {disabled && <img src={loadingWheel} />}
    </div>
  );
}

function ReportDisplay({ report, setReport, ownerAndName }) {
  if (!report) return null;

  const commitFrequency =
    report.commit_frequency.status_code === 200
      ? `On average, this repository 
        receives a commit every ${report.commit_frequency.data.toFixed(3)} hours.`
      : report.commit_frequency.error_message;

  const issuesCloseTime =
    report.issues_close_time.status_code === 200
      ? `On average, this repository 
        closes an Issue every ${report.issues_close_time.data.toFixed(3)} hours.`
      : report.issues_close_time.error_message;

  const pullsCloseTime =
    report.pulls_close_time.status_code === 200
      ? `On average, this repository 
        closes a Pull Request every ${report.pulls_close_time.data.toFixed(3)} hours.`
      : report.pulls_close_time.error_message;

  const codeChurn =
    report.code_churn.status_code === 200
      ? `This repository has 
          ${report.code_churn.data.additions} additions, 
          ${report.code_churn.data.deletions} deletions, 
          totaling at ${report.code_churn.data.total} line changes, 
          with a net of ${report.code_churn.data.net} lines.`
      : report.code_churn.error_message;

  return (
    <div className={styles.reportDisplay}>
      <div className={styles.reportHeader}>
        <h1>{ownerAndName} Activity Report</h1>
        <button onClick={() => setReport(null)}>Create Another</button>
      </div>

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
  const [ownerAndName, setOwnerAndName] = useState("owner/name");

  async function onAnalyse() {
    if (!url) return;

    setIsLoading(true);
    setOwnerAndName(url.replace("https://github.com/", ""));
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
        {!report && (
          <h1 className={styles.createReportHeader}>Create a Report Here</h1>
        )}

        {!report ? (
          <ReportForm
            url={url}
            setUrl={setUrl}
            onAnalyse={onAnalyse}
            disabled={isLoading}
          />
        ) : (
          <ReportDisplay
            report={report}
            setReport={setReport}
            ownerAndName={ownerAndName}
          />
        )}
      </main>
      <Footer />
    </>
  );
}
