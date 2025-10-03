import styles from "./Footer.module.css";

export default function GitsyFooter() {
  return (
    <footer className={styles.footer}>
      <p>&copy; {new Date().getFullYear()} Gitsy</p>
    </footer>
  );
}
