import styles from "./Footer.module.css";

export default function GitsyFooter() {
  return (
    <footer className={styles.footer}>
      <p>
        &copy; {new Date().getFullYear()} Gitsy ·{" "}
        <a
          href="https://github.com/matslyk0/Gitsy"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
      </p>
    </footer>
  );
}
