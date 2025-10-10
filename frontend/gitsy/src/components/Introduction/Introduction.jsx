export default function Introduction() {
  return (
    <div>
      <h1 style={{ color: "white" }}>
        Welcome to Gitsy, the repository analysis tool.
      </h1>
      <h3 style={{ color: "white" }}>What does Gitsy do?</h3>
      <p style={{ color: "white" }}>
        Gitsy calculates four metrics about a public repository to help you
        understand its activity at a glance. The metrics are commit frequency,
        code churn, average issue close time, and average pull request close
        time.
      </p>
      <h3 style={{ color: "white" }}>How does Gitsy work?</h3>
      <p style={{ color: "white" }}>
        Gitsy uses the GitHub API to fetch data about the provided repository,
        extract information, and calculate metrics. Reports usually generate
        within a couple of minutes, depending on the repository size, and you
        don't need any accounts to generate reports.
      </p>
      <h3 style={{ color: "white" }}>How do I use it?</h3>
      <p style={{ color: "white" }}>
        Find any public repository, copy its URL, and enter it on the Create
        Report page. The button is right here, give it a go!
      </p>
    </div>
  );
}
