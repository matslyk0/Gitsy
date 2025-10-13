import { Link } from "react-router-dom";
import styles from "./GetStartedButton.module.css";

export default function GetStartedButton() {
  return (
    <Link to={"/get-started"} className={styles.getStartedButton}>
      Get Started
    </Link>
  );
}
