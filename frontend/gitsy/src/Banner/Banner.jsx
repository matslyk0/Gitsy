import gitsyLogoPic from "../assets/gitsyLogo.jpg";
import styles from "./Banner.module.css";

function GitsyLogo() {
  return (
    <button className={styles.gitsyLogo}>
      <img className={styles.gitsyLogoPic} src={gitsyLogoPic}></img>
    </button>
  );
}

function SignInButton() {
  return <button className={styles.signInButton}>Sign in</button>;
}

function SignUpButton() {
  return <button className={styles.signUpButton}>Sign up</button>;
}

export default function Banner() {
  return (
    <header>
      <nav className={styles.banner}>
        <GitsyLogo />
        <div className={styles.bannerRight}>
          <SignInButton />
          <SignUpButton />
        </div>
      </nav>
    </header>
  );
}
