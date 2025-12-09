import styles from "./Card.module.css";

export default function Card(props) {
  return (
    <div className={styles.card}>
      <h1>{props.metricName}</h1>
      <div>{props.metricData}</div>
    </div>
  );
}
