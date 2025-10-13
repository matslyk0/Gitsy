import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import CreateReportPageButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import styles from "./GetStarted.module.css";

function Introduction() {
  return (
    <>
      <div className={styles.introduction}>
        <h1>Welcome to Gitsy, the repository analysis tool.</h1>

        <section>
          <h2>What does Gitsy do?</h2>
          <p>
            Gitsy calculates four metrics about a public repository to help you
            understand its activity at a glance. The metrics are commit
            frequency, code churn, average issue close time, and average pull
            request close time.
          </p>
        </section>

        <section>
          <h2>How does Gitsy work?</h2>
          <p>
            Gitsy uses the GitHub API to fetch data about the provided
            repository, extract information, and calculate metrics. Reports
            usually generate within a couple of minutes, depending on the
            repository size, and you don't need any accounts to generate
            reports.
          </p>
        </section>

        <section>
          <h2>How do I use it?</h2>
          <p>
            Find any public repository, copy its URL, and enter it on the Create
            Report page. The button is right here, give it a go!
          </p>
        </section>
      </div>
    </>
  );
}

export default function GetStarted() {
  const mainStyles = {
    justifyContent: "center",
    display: "flex",
    alignItems: "center",
    flex: "1",
    flexDirection: "column",
    border: "1px solid white" /* for debugging */,
  };

  return (
    <>
      <Banner />
      <main style={mainStyles}>
        <Introduction />
        <CreateReportPageButton />
      </main>
      <Footer />
    </>
  );
}
