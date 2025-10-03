import styles from "./MainButtons.module.css";

function GetStartedButton() {
  return <button className={styles.getStartedButton}>Get Started</button>;
}

function CreateReportButton() {
  return <button className={styles.createReportButton}>Create Report</button>;
}

export default function MainButtons() {
  return (
    <div className={styles.mainButtons}>
      <GetStartedButton />
      <CreateReportButton />
    </div>
  );
}
