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

export default function Banner() {
  return (
    <header>
      <nav className={styles.banner}>
        <GitsyLogo />
      </nav>
    </header>
  );
}
