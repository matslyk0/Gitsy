import Banner from "../../components/Banner/Banner.jsx";
import GetStartedButton from "../../components/GetStartedButton/GetStartedButton.jsx";
import CreateReportButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import Footer from "../../components/Footer/Footer.jsx";

import styles from "./Home.module.css";

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
        <div className={styles.sampleReport} />
      </main>
      <Footer />
    </>
  );
}
