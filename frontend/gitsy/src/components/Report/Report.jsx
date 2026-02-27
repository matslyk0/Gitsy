import styles from "./Report.module.css";
import Card from "../Card/Card.jsx";

export default function Report({ ownerAndName, reportData }) {
  const commitFrequencyContent =
    reportData.commit_frequency.status_code === 200
      ? `On average, this repository 
        receives a commit every ${reportData.commit_frequency.data.toFixed(3)} hours.`
      : reportData.commit_frequency.error_message;

  const issuesCloseTimeContent =
    reportData.issues_close_time.status_code === 200
      ? `On average, this repository 
        closes an Issue every ${reportData.issues_close_time.data.toFixed(3)} hours.`
      : reportData.issues_close_time.error_message;

  const pullsCloseTimeContent =
    reportData.pulls_close_time.status_code === 200
      ? `On average, this repository 
        closes a Pull Request every ${reportData.pulls_close_time.data.toFixed(3)} hours.`
      : reportData.pulls_close_time.error_message;

  const codeChurnContent =
    reportData.code_churn.status_code === 200
      ? `This repository has 
          ${reportData.code_churn.data.additions} additions, 
          ${reportData.code_churn.data.deletions} deletions, 
          totaling at ${reportData.code_churn.data.total} line changes, 
          with a net of ${reportData.code_churn.data.net} lines.`
      : reportData.code_churn.error_message;

  return (
    <div className={styles.reportDisplay}>
      <div className={styles.reportHeader}>
        <h1>{ownerAndName} Activity Report</h1>
      </div>

      <Card title="Commit Frequency" content={commitFrequencyContent} />
      <Card title="Issues Close Time" content={issuesCloseTimeContent} />
      <Card title="Pulls Close Time" content={pullsCloseTimeContent} />
      <Card title="Code Churn" content={codeChurnContent} />
    </div>
  );
}
