import styles from "./Card.module.css";

export default function Card(props) {
  return (
    <div className={styles.card}>
      <h2>{props.metricName}</h2>
      <div>{props.metricData}</div>
    </div>
  );
}
