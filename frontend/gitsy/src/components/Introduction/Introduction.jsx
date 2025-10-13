import styles from "./Introduction.module.css";
import CreateReportPageButton from "../MainPageButtons/CreateReportPageButton";

export default function Introduction() {
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

      <div className={styles.buttonDiv}>
        <CreateReportPageButton />
      </div>
    </>
  );
}
