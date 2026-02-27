import styles from "./Card.module.css";

export default function Card(props) {
  return (
    <div className={styles.card}>
      <h1>{props.title}</h1>
      <div>{props.content}</div>
    </div>
  );
}
