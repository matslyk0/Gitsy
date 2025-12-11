import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import CreateReportPageButton from "../../components/CreateReportButton/CreateReportButton.jsx";
import styles from "./GetStarted.module.css";

export default function GetStarted() {
  return (
    <>
      <Banner />
      <main className={styles.main}>
        <div className={styles.getStarted}>
          <h1 className={styles.header}>
            Welcome to Gitsy, the repository analysis tool.
          </h1>

          <section>
            <h2 className={styles.question}>What does it do?</h2>
            <p className={styles.answer}>
              Gitsy calculates several metrics for any public GitHub repository
              so you can get a quick understanding of its activity.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>How does it work?</h2>
            <p className={styles.answer}>
              Gitsy uses the GitHub API to fetch repository data, calculates the
              metrics, and presents it to you in a report.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>How long does it take?</h2>
            <p className={styles.answer}>
              Reports usually generate within a couple of minutes, depending on
              the repository size, and if others are using the site.
            </p>
          </section>

          <section>
            <h2 className={styles.question}>Do I need an account?</h2>
            <p className={styles.answer}>
              You don't need any accounts to make a report. In the future,
              accounts will be the recommended way to use Gitsy.
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
