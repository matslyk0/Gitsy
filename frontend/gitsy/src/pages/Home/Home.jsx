import Banner from "../../components/Banner/Banner.jsx";
import GetStartedButton from "../../components/GetStartedButton/GetStartedButton.jsx";
import CreateReportButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Report from "../../components/Report/Report.jsx";
import styles from "./Home.module.css";

const sampleReportData = {
  commit_frequency: { status_code: 200, data: 10.3 },
  issues_close_time: { status_code: 200, data: 265 },
  pulls_close_time: { status_code: 200, data: 0.1 },
  code_churn: { status_code: 200, data: { additions: 1000, deletions: 100 } },
};

export default function Home() {
  return (
    <>
      <Banner />
      <main className={styles.mainContent}>
        <div className={styles.welcomeBox}>
          <h1>GitHub Repository Analysis</h1>
          <p>Repository health at a glance, in a single click.</p>
          <div className={styles.mainButtons}>
            <GetStartedButton />
            <CreateReportButton />
          </div>
        </div>

        <div className={styles.sampleReportDiv}>
          <Report reportData={sampleReportData} ownerAndName="sample/repo" />
        </div>
      </main>
      <Footer />
    </>
  );
}
