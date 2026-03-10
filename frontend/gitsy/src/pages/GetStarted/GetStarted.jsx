import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import CreateReportPageButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import styles from "./GetStarted.module.css";

export default function GetStarted() {
  return (
    <>
      <Banner />
      <main className={styles.mainConfig}>
        <div className={styles.getStarted}>
          <h1 className={styles.header}>
            Welcome to Gitsy, the repository analysis tool.
          </h1>

          <section>
            <h2 className={styles.question}>What does it do?</h2>
            <p className={styles.answer}>
              Gitsy calculates metrics for public GitHub repositories so you can
              get a concise summary of its activity.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>How does it work?</h2>
            <p className={styles.answer}>
              Gitsy uses the GitHub API to fetch repository data which is used
              to calculate the report metrics.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>How long does it take?</h2>
            <p className={styles.answer}>
              Please give up to 2 minutes for report generation.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>Do I need an account?</h2>
            <p className={styles.answer}>
              Not at the moment! In the future, accounts will be the recommended
              way to use Gitsy.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>How do I use it?</h2>
            <p className={styles.answer}>
              Find any public repository on GitHub, copy its URL, and enter it
              on the Create Report page.
            </p>
          </section>
        </div>
        <CreateReportPageButton />
      </main>
      <Footer />
    </>
  );
}
