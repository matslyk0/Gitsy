import Banner from "../../components/Banner/Banner.jsx";
import GetStartedButton from "../../components/GetStartedButton/GetStartedButton.jsx";
import CreateReportButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import Footer from "../../components/Footer/Footer.jsx";

import styles from "./Home.module.css";

export default function Home() {
  const mainStyles = {
    justifyContent: "center",
    display: "flex",
    alignItems: "center",
    flex: "1",
    flexDirection: "column",
    border: "0px solid white" /* for debugging */,
  };

  return (
    <>
      <Banner />
      <main style={mainStyles}>
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
