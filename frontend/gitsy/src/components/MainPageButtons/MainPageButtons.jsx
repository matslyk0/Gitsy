import GetStartedPageButton from "./GetStartedPageButton.jsx";
import CreateReportPageButton from "./CreateReportPageButton.jsx";
import styles from "./MainPageButtons.module.css";

export default function MainPageButtons() {
  return (
    <div className={styles.mainPageButtons}>
      <GetStartedPageButton />
      <CreateReportPageButton />
    </div>
  );
}
