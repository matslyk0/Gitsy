import { Link } from "react-router-dom";
import styles from "./MainPageButtons.module.css";

export default function GetStartedPageButton() {
  return (
    <Link to={"/get-started"} className={styles.getStartedPageButton}>
      Get Started
    </Link>
  );
}
