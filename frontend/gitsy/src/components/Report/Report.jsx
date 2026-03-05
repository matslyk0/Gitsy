import styles from "./Report.module.css";
import Card from "../Card/Card.jsx";

function formatTitle(metric, messageBuilder) {
  if (metric.status_code !== 200) {
    return "No Data";
  }
  return messageBuilder(metric.data);
}

function formatContent(metric, message) {
  if (metric.status_code !== 200) {
    return metric.error_message;
  }
  return message;
}

export default function Report({ ownerAndName, reportData }) {
  const {
    commit_frequency: commitFrequency,
    issues_close_time: issuesCloseTime,
    pulls_close_time: pullsCloseTime,
    code_churn: codeChurn,
  } = reportData;

  return (
    <div className={styles.reportDisplay}>
      <div className={styles.reportHeader}>
        <h1>{ownerAndName}</h1>
      </div>

      <Card
        title={formatTitle(
          commitFrequency,
          (metricData) => `${metricData.toFixed(1)} hours`,
        )}
        content={formatContent(commitFrequency, "between Commits.")}
      />
      <Card
        title={formatTitle(
          issuesCloseTime,
          (metricData) => `${metricData.toFixed(1)} hours`,
        )}
        content={formatContent(issuesCloseTime, "between closed Issues.")}
      />
      <Card
        title={formatTitle(
          pullsCloseTime,
          (metricData) => `${metricData.toFixed(1)} hours`,
        )}
        content={formatContent(pullsCloseTime, "between closed Pull Requests.")}
      />
      <Card
        title={formatTitle(
          codeChurn,
          (metricData) => `${metricData.additions - metricData.deletions}`,
        )}
        content={formatContent(
          codeChurn,
          "line changes across the repository.",
        )}
      />
    </div>
  );
}
