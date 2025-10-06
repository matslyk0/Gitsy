import { Link } from "react-router-dom";
import styles from "./MainButtons.module.css";

function GetStartedButton() {
  return (
    <Link to={"/get-started"} className={styles.getStartedButton}>
      Get Started
    </Link>
  );
}

function CreateReportButton() {
  return (
    <Link to={"/create-report"} className={styles.createReportButton}>
      Create Report
    </Link>
  );
}

export default function MainButtons() {
  return (
    <div className={styles.mainButtons}>
      <GetStartedButton />
      <CreateReportButton />
    </div>
  );
}
