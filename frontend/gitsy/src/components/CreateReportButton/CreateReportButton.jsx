import { Link } from "react-router-dom";
import styles from "./CreateReportButton.module.css";

export default function CreateReportButton() {
  return (
    <Link to={"/create-report"} className={styles.createReportButton}>
      Create Report
    </Link>
  );
}
