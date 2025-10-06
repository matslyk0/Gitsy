import { Link } from "react-router-dom";
import gitsyLogoPic from "../../assets/gitsyLogo.jpg";
import styles from "./Banner.module.css";

function GitsyLogo() {
  return (
    <Link to={"/"} className={styles.gitsyLogo}>
      <img className={styles.gitsyLogoPic} src={gitsyLogoPic}></img>
    </Link>
  );
}

function LoginButton() {
  return (
    <Link to={"/login"} className={styles.loginButton}>
      Log in
    </Link>
  );
}

function SignUpButton() {
  return (
    <Link to={"/login"} className={styles.signUpButton}>
      Sign up
    </Link>
  );
}

export default function Banner() {
  return (
    <header>
      <nav className={styles.banner}>
        <GitsyLogo />
        {/* Here for when accounts get implemented        
        <div className={styles.bannerRight}>
          <LoginButton />
          <SignUpButton />
        </div>
        */}
      </nav>
    </header>
  );
}
