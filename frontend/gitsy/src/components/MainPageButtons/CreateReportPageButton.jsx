import { Link } from "react-router-dom";
import styles from "./MainPageButtons.module.css";

export default function CreateReportPageButton() {
  return (
    <Link to={"/create-report"} className={styles.createReportPageButton}>
      Create Report
    </Link>
  );
}
