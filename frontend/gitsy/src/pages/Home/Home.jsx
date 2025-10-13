import Banner from "../../components/Banner/Banner.jsx";
import Welcome from "../../components/Welcome/Welcome.jsx";
import GetStartedButton from "../../components/GetStartedButton/GetStartedButton.jsx";
import CreateReportButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import Footer from "../../components/Footer/Footer.jsx";

import styles from "./Home.module.css";

export default function Home() {
  return (
    <>
      <Banner />
      <main>
        <Welcome />
        <div className={styles.mainPageButtons}>
          <GetStartedButton />
          <CreateReportButton />
        </div>
      </main>
      <Footer />
    </>
  );
}
