import Banner from "../../components/Banner/Banner.jsx";
import GetStartedButton from "../../components/GetStartedButton/GetStartedButton.jsx";
import CreateReportButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import Footer from "../../components/Footer/Footer.jsx";

import styles from "./Home.module.css";

export default function Home() {
  return (
    <>
      <Banner />
      <main>
        <div className={styles.welcome}>
          <h1>Welcome to Gitsy!</h1>
        </div>
        <div className={styles.mainPageButtons}>
          <GetStartedButton />
          <CreateReportButton />
        </div>
      </main>
      <Footer />
    </>
  );
}
