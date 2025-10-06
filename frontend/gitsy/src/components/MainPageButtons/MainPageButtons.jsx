import { Link } from "react-router-dom";
import styles from "./MainPageButtons.module.css";

function GetStartedPageButton() {
  return (
    <Link to={"/get-started"} className={styles.getStartedPageButton}>
      Get Started
    </Link>
  );
}

function CreateReportPageButton() {
  return (
    <Link to={"/create-report"} className={styles.createReportPageButton}>
      Create Report
    </Link>
  );
}

export default function MainPageButtons() {
  return (
    <div className={styles.mainPageButtons}>
      <GetStartedPageButton />
      <CreateReportPageButton />
    </div>
  );
}
